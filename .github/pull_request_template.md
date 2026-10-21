## What changed

## Design system checklist
- [ ] `python3 scripts/check-design-conformance.py -v` exits 0
- [ ] `python3 scripts/tests/run_tests.py` passes
- [ ] No hex, px font sizes or spacing literals; no coloured edge stripes
- [ ] New tokens added to `design-system/tokens.json` with a usage note, then `python3 scripts/build-design-tokens.py`
- [ ] Looked at the changed pages at desktop and 390px width
