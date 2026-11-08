"""Coordinator-only evidence capture; exclusive writes preserve earlier evidence."""
import hashlib
import difflib
import json
import re
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def save(name, content):
    with (OUT / name).open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def snapshot(label):
    hashes = {}
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if any(part in {".git", ".venv", "__pycache__"} for part in rel.parts) or path.is_relative_to(OUT):
            continue
        if path.is_file():
            hashes[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    save(label + ".hashes.json", json.dumps(hashes, indent=2) + "\n")


def export(thread, label, first=False):
    candidates = list((Path.home() / ".codex/sessions").rglob("*" + thread + ".jsonl"))
    if len(candidates) != 1:
        raise RuntimeError(f"Expected one rollout, found {len(candidates)}")
    rows = []
    for line in candidates[0].read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        payload = row.get("payload", {})
        if row["type"] == "response_item":
            kind = payload.get("type")
            if kind in {"function_call", "function_call_output", "custom_tool_call", "custom_tool_call_output"} or (kind == "message" and payload.get("role") in {"user", "assistant"} and payload.get("channel") != "analysis"):
                rows.append(row)
        if first and row["type"] == "event_msg" and payload.get("type") == "task_complete":
            break
    save(label + ".transcript.jsonl", "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    save(label + ".provenance.json", json.dumps({"thread_id": thread, "source": str(candidates[0]),
         "export": "Verbatim response items: user/assistant visible messages and tool calls/results; system context and reasoning omitted.",
         "first_completed_turn_only": first, "items": len(rows)}, indent=2) + "\n")
    extract_final(rows, label)
    print(f"Exported {len(rows)} response items for {thread}")


def extract_final(rows, label):
    finals = [row["payload"] for row in rows if row["payload"].get("type") == "message" and row["payload"].get("role") == "assistant" and (row["payload"].get("channel") == "final" or row["payload"].get("phase") == "final_answer")]
    if finals:
        save(label + ".result.md", "\n\n".join(part.get("text", "") for final in finals for part in final.get("content", [])) + "\n")


if __name__ == "__main__":
    if sys.argv[1] == "snapshot":
        snapshot(sys.argv[2])
    elif sys.argv[1] == "export":
        export(sys.argv[2], sys.argv[3], "--first" in sys.argv[4:])
    elif sys.argv[1] == "final":
        extract_final([json.loads(line) for line in (OUT / (sys.argv[2] + ".transcript.jsonl")).read_text(encoding="utf-8").splitlines()], sys.argv[2])
    elif sys.argv[1] == "diff":
        before, after, label = sys.argv[2:5]
        save(label, "".join(difflib.unified_diff((ROOT / before).read_text(encoding="utf-8").splitlines(True),
             (ROOT / after).read_text(encoding="utf-8").splitlines(True), fromfile=before, tofile=after)))
    elif sys.argv[1] == "patch":
        label = sys.argv[2]
        rows = [json.loads(line) for line in (OUT / (label + ".transcript.jsonl")).read_text(encoding="utf-8").splitlines()]
        patches = []
        for row in rows:
            content = row["payload"].get("input", "")
            patches.extend(json.loads(match) for match in re.findall(r'tools.apply_patch\(("(?:\\.|[^"\\])*")\)', content))
        save(label + ".patch", "\n".join(patches) + "\n")
    elif sys.argv[1] == "run":
        label, command = sys.argv[2], sys.argv[3:]
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
        save(label + ".log", result.stdout)
        save(label + ".command.json", json.dumps({"command": command, "cwd": str(ROOT), "exit_code": result.returncode,
             "python": sys.version}, indent=2) + "\n")
        print(result.stdout)
        print("Exit code:", result.returncode)
        sys.exit(result.returncode)
