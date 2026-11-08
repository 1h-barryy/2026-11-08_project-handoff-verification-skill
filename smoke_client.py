"""Call the local server over real stdio without registering it in a host."""

import argparse
import asyncio
import json
from pathlib import Path
import sys

from mcp import Client
from mcp.client.stdio import StdioServerParameters


async def inspect_over_stdio(root: Path, task: str) -> dict:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-B", str(Path(__file__).with_name("server.py")), "--project-root", str(root.resolve())],
    )
    async with Client(params, read_timeout_seconds=30) as client:
        listing = await client.list_tools()
        assert [tool.name for tool in listing.tools] == ["inspect_project_context"]
        assert set(listing.tools[0].input_schema["properties"]) == {"task"}
        result = await client.call_tool("inspect_project_context", {"task": task})
        if result.is_error:
            raise RuntimeError(str(result.content))
        if not isinstance(result.structured_content, dict):
            raise RuntimeError("Server did not return a structured context object")
        return result.structured_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--task", required=True)
    args = parser.parse_args()
    print(json.dumps(asyncio.run(inspect_over_stdio(args.project_root, args.task)), indent=2))
