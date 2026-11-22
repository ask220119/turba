#!/usr/bin/env python3
"""Validate every TURBA skill and write catalogue.json.

    python tools/build_catalogue.py           # validate and write catalogue.json
    python tools/build_catalogue.py --check   # validate and fail if catalogue.json is out of date

Rules checked for each skills/<name>/ folder:
- SKILL.md (English) and SKILL.fr.md (French) exist, with front matter;
- name equals the folder name, lowercase letters, digits and hyphens, at most 64 characters;
- description present, at most 1024 characters, no angle brackets;
- license and metadata (collection, version, domain, standards, language) present, same version in both files;
- every scripts/... path quoted in the text exists.
Standard library only.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
OUT = ROOT / "catalogue.json"
REPO = "ask220119/turba"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_META = ("collection", "version", "domain", "standards", "language")


def parse_front_matter(text: str, where: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{where}: missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{where}: unterminated front matter")
    data: dict = {}
    current: dict | None = None
    for raw in text[4:end].splitlines():
        if not raw.strip():
            continue
        indented = raw.startswith("  ")
        key, sep, value = raw.strip().partition(":")
        if not sep:
            raise ValueError(f"{where}: cannot read line {raw!r}")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if indented:
            if current is None:
                raise ValueError(f"{where}: indented key outside a block")
            current[key] = value
        elif value == "":
            current = data.setdefault(key, {})
        else:
            data[key] = value
            current = None
    return data, text[end + 5:]


def check_skill(folder: pathlib.Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    out: dict = {}
    docs = {}
    for lang, fname in (("en", "SKILL.md"), ("fr", "SKILL.fr.md")):
        f = folder / fname
        if not f.exists():
            errors.append(f"{folder.name}: {fname} missing")
            continue
        try:
            fm, body = parse_front_matter(f.read_text(encoding="utf-8"), f"{folder.name}/{fname}")
        except ValueError as e:
            errors.append(str(e))
            continue
        docs[lang] = (fm, body)
        where = f"{folder.name}/{fname}"
        name = fm.get("name", "")
        if name != folder.name:
            errors.append(f"{where}: name {name!r} differs from folder")
        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{where}: invalid name {name!r}")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{where}: description missing")
        if len(desc) > 1024:
            errors.append(f"{where}: description longer than 1024 characters")
        if "<" in desc or ">" in desc:
            errors.append(f"{where}: no angle brackets in description")
        if not fm.get("license"):
            errors.append(f"{where}: license missing")
        meta = fm.get("metadata", {})
        for k in REQUIRED_META:
            if not meta.get(k):
                errors.append(f"{where}: metadata.{k} missing")
        if meta.get("language") and meta["language"] != lang:
            errors.append(f"{where}: metadata.language should be {lang}")
        for ref in set(re.findall(r"`(scripts/[\w./-]+)`", body)):
            if not (folder / ref).exists():
                errors.append(f"{where}: {ref} does not exist")
    if len(docs) == 2:
        (en, en_body), (fr, _) = docs["en"], docs["fr"]
        if en.get("metadata", {}).get("version") != fr.get("metadata", {}).get("version"):
            errors.append(f"{folder.name}: English and French versions differ")
        meta = en.get("metadata", {})
        title = re.search(r"^# (.+)$", en_body, re.M)
        title_fr = re.search(r"^# (.+)$", docs["fr"][1], re.M)
        out = {
            "name": en["name"],
            "title": {"en": title.group(1) if title else en["name"], "fr": title_fr.group(1) if title_fr else en["name"]},
            "description": {"en": en.get("description", ""), "fr": fr.get("description", "")},
            "domain": meta.get("domain", ""),
            "version": meta.get("version", ""),
            "standards": [s.strip() for s in meta.get("standards", "").split(",") if s.strip()],
            "tests": [s.strip() for s in meta.get("tests", "").split(",") if s.strip()],
            "license": en.get("license", ""),
            "scripts": sorted(p.name for p in (folder / "scripts").glob("*.py")) if (folder / "scripts").exists() else [],
            "path": f"skills/{folder.name}",
            "url": f"https://github.com/{REPO}/tree/main/skills/{folder.name}",
        }
    return out, errors


def build() -> tuple[dict, list[str]]:
    skills, errors = [], []
    for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        entry, errs = check_skill(folder)
        errors += errs
        if entry:
            skills.append(entry)
    # core first, then alphabetical
    skills.sort(key=lambda s: (s["name"] != "turba-core", s["name"]))
    version = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"]
    catalogue = {
        "collection": "TURBA",
        "version": version,
        "repository": f"https://github.com/{REPO}",
        "install": {"skills_cli": f"npx skills add {REPO}", "claude_code": f"/plugin marketplace add {REPO}"},
        "skills": skills,
    }
    return catalogue, errors


def main() -> int:
    catalogue, errors = build()
    for e in errors:
        print("ERROR", e)
    if errors:
        return 1
    text = json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n"
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("catalogue.json is out of date: run python tools/build_catalogue.py")
            return 1
        print(f"{len(catalogue['skills'])} skills valid, catalogue up to date")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"{len(catalogue['skills'])} skills valid, catalogue.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
