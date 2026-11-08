Added bounded Python constant-definition evidence with names, paths, line numbers, and excerpts. The MCP now locates all four scan limits at `server.py:27–30`.

- Scan limits, boundaries, and existing matching behavior remain unchanged.
- All 8 tests passed, including real stdio MCP verification.
- The initial project-context MCP call is visible in this session.
- Updated only `server.py`, `tests/test_server.py`, and README documentation. Checker skill untouched; no commit or push.
