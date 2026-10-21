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
html = bh.render_stack({"languages": [("Python", 50), ("TypeScript", 30), ("HTML", 10), ("Shell", 5), ("CSS", 3), ("Other", 2)]}) + bh.render_latest({"date": "2026-10-01", "headline": "Shipped the thing"})
with tempfile.TemporaryDirectory() as d:
    (pathlib.Path(d) / "page.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>t</title></head><body>' + html + "</body></html>")
    rc = subprocess.run([sys.executable, str(gate), d], capture_output=True).returncode
if rc != 0: failed.append("build-highlights.py output violates the design system")
print(f"{len(list((here/'bad').glob('*.html')))} bad + {len(list((here/'good').glob('*.html')))} good fixtures")
print("\n".join(failed) or "all gate tests pass")
sys.exit(1 if failed else 0)
