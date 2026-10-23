#!/usr/bin/env python3
"""Tests for the conformance gate itself: every file in bad/ must fail, good/ must pass.
Run: python3 scripts/tests/run_tests.py"""
import subprocess, sys, pathlib, tempfile, shutil
here = pathlib.Path(__file__).resolve().parent
gate = here.parent / "check-design-conformance.py"
failed = []
for kind, want in (("bad", 1), ("good", 0)):
    for f in sorted((here / kind).glob("*.html")):
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(f, pathlib.Path(d) / "page.html")
            rc = subprocess.run([sys.executable, str(gate), d], capture_output=True).returncode
        if rc != want:
            failed.append(f"{kind}/{f.name}: exit {rc}, wanted {want}")
# the daily highlights generator must emit HTML that passes the gate
import importlib.util
spec = importlib.util.spec_from_file_location("bh", here.parent / "build-highlights.py"); bh = importlib.util.module_from_spec(spec); spec.loader.exec_module(bh)
M = {"commits": 1044, "pr": 389, "ai": 647, "conv": 940, "dates": [__import__("datetime").date(2026, 3, 21).__add__(__import__("datetime").timedelta(days=i)).isoformat() for i in range(0, 215, 2)] + ["2026-10-22"], "projects": 5, "skills": 3, "commands": 5, "agents": 3,
     "hooks": 11, "evals": 175, "notes": 50, "concepts": 58, "learnings": 545, "changelog": 115, "md": 150, "html": 152, "files": 1074,
     "languages": [("TypeScript", 44), ("JSON", 21)], "gh_contributions": 1505}
CFG = {"repos": [], "options": {}, "insights": [{"key": k, "enabled": True, "primary": k in ("github_contributions", "ai_assisted")} for k in ("github_contributions", "commits", "pr_driven", "ai_assisted", "evals")]}
block, _ = bh.render(CFG, M)
assert "stat-lead" in block and "stat-ctx" not in block, "generator must emit one reference lead and no restating tile lines"
assert "stat-trend" in block and "<svg" in block and "Last 30 days" in block, "generator must emit the weekly trend chart and the 30-day comparison"
assert "stat-more" in block and "stat-grid" in block, "generator must split primary tiles from the collapsed rest"
html = block + bh.render_stack({"languages": [("Python", 50), ("TypeScript", 30), ("HTML", 10), ("Shell", 5), ("CSS", 3), ("Other", 2)]}) + bh.render_latest({"date": "2026-10-01", "headline": "Shipped the thing"})
with tempfile.TemporaryDirectory() as d:
    (pathlib.Path(d) / "page.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>t</title></head><body>' + html + "</body></html>")
    rc = subprocess.run([sys.executable, str(gate), d], capture_output=True).returncode
if rc != 0: failed.append("build-highlights.py output violates the design system")
print(f"{len(list((here/'bad').glob('*.html')))} bad + {len(list((here/'good').glob('*.html')))} good fixtures")
print("\n".join(failed) or "all gate tests pass")
sys.exit(1 if failed else 0)
