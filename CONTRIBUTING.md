# Contributing to TURBA

## Add or change a skill

1. Create `skills/turba-<topic>/` with two files:
   - `SKILL.md` in English, `SKILL.fr.md` in French, same content.
   - Front matter (both files):

     ```yaml
     ---
     name: turba-<topic>              # same as the folder
     description: What the skill does and when an agent should use it (max 1024 characters, no angle brackets).
     license: CC-BY-4.0
     metadata:
       collection: TURBA
       version: "0.1.0"               # same in both files
       domain: <foundations | retaining-structures | slopes | seismic | site-investigation | ground-improvement | ...>
       standards: "EN 1997-1, ..."
       tests: "PMT, CPT"              # optional
       language: en                   # fr in SKILL.fr.md
     ---
     ```
2. Body: start with `Load turba-core first.`, then workflow, methods with formulas and units, orders of magnitude, report outline, common pitfalls.
3. Scripts go in `skills/<name>/scripts/`, standard library only, with a reference test in `tests/` (hand calculation or published example).
4. Run `python tools/build_catalogue.py` and `pytest -q tests`, commit `catalogue.json` with your change.

## Rules for content

- Write your own text. Quote standards and papers by reference (title, year, clause), never copy pages of a standard or a paid course.
- No client names, project codes or confidential data.
- Every number has a unit and a source or is marked as an order of magnitude.
- Say what the method does not cover.
