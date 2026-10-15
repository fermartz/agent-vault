#!/usr/bin/env python3
"""Pre-review checks for a repo of skills, principles and workflows.

    check_skills.py ROOT [--deny WORD ...] [--deny-file PATH]

1. Links: every inline relative link in a markdown file resolves to a file inside ROOT. Supported
   forms: [text](path), [text](path "title"), [text](path 'title'), [text](<path with spaces>);
   any other inline form is reported as unsupported. Fenced code blocks are skipped. Reference-style
   links and #anchors are not checked.
2. Skills: every folder in skills/ is a real folder (not a symlink) with a regular SKILL.md whose
   only top-level keys are `name` (equal to its folder), `description` (non-empty text) and
   `metadata` (frontmatter parsed as YAML), with `version` (X.Y.Z) and `maturity`
   (experimental | working | battle-tested) directly under `metadata:`. battle-tested needs
   1.0.0+; anything else stays 0.x.
3. Privacy: no denied word appears in a shipped file. Matching ignores case, accent encoding and
   straight vs curly apostrophes. Hits are reported as file:line only, never the line itself.
   Keep the word list outside the repo.

Skips dot-folders (.git, .agent, ...), node_modules, __pycache__ and symlinks. Needs PyYAML. Exit 1 on any
problem, 2 if ROOT has no skills/ folder.
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml  # PyYAML: frontmatter is parsed as real YAML, never by regex
except ImportError:
    sys.exit("check_skills.py needs PyYAML: pip install pyyaml")

SKIP = {"node_modules", "__pycache__"}
MATURITY = {"experimental", "working", "battle-tested"}
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
# Supported: [text](path), [text](path "title"), [text](path 'title'), [text](<path with spaces>).
# Paths containing parentheses must use the <...> form.
INLINE = re.compile(r"\]\(\s*(<[^>]*>|[^()\s]+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
LOOSE = re.compile(r"\]\((?:<[^>]*>|[^)])*\)")


def shipped(root: Path):
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).parts
        if any(part in SKIP or part.startswith(".") for part in rel):
            continue
        if p.is_symlink() or not p.is_file():
            continue
        yield p


def without_fences(text: str) -> str:
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return "\n".join(out)


def check_links(root: Path, files) -> list[str]:
    bad = []
    for p in files:
        if p.suffix != ".md":
            continue
        text = without_fences(p.read_text(errors="ignore"))
        for m in LOOSE.finditer(text):
            if not INLINE.fullmatch(m.group(0)):
                bad.append(f"unsupported link form: {p.relative_to(root)} -> {m.group(0)[2:-1]}")
        for m in INLINE.finditer(text):
            target = m.group(1).strip("<>").split("#")[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            dest = (p.parent / target).resolve()
            if not dest.is_relative_to(root):
                bad.append(f"link leaves the repo: {p.relative_to(root)} -> {target}")
            elif not dest.exists():
                bad.append(f"broken link: {p.relative_to(root)} -> {target}")
    return bad


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, "no frontmatter"
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return None, f"frontmatter is not valid YAML ({e.__class__.__name__})"
    if not isinstance(data, dict):
        return None, "frontmatter is not a mapping"
    return data, None


def check_skill(root: Path, p: Path) -> list[str]:
    where = p.relative_to(root)
    top, err = parse_frontmatter(p.read_text())
    if err:
        return [f"{where}: {err}"]
    meta = top.get("metadata")
    if not isinstance(meta, dict):
        return [f"{where}: metadata must be a mapping"]
    out = []
    extra = sorted(set(top) - {"name", "description", "metadata"})
    if extra:
        out.append(f"{where}: unexpected top-level keys {extra} (put them under metadata:)")
    if top.get("name") != p.parent.name:
        out.append(f"{where}: name must equal the folder name '{p.parent.name}'")
    desc = top.get("description")
    if not isinstance(desc, str) or not desc.strip():
        out.append(f"{where}: description must be non-empty text")
    version, maturity = str(meta.get("version", "")), str(meta.get("maturity", ""))
    v = SEMVER.match(version)
    if not v:
        out.append(f"{where}: metadata.version must be X.Y.Z, found '{version}'")
    if maturity not in MATURITY:
        out.append(f"{where}: metadata.maturity must be one of {sorted(MATURITY)}, found '{maturity}'")
    if v and maturity in MATURITY:
        major = int(v.group(1))
        if maturity == "battle-tested" and major < 1:
            out.append(f"{where}: battle-tested must be 1.0.0+, found {version}")
        if maturity != "battle-tested" and major != 0:
            out.append(f"{where}: {maturity} stays 0.x, found {version}")
    return out


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    return s.replace("’", "'").replace("‘", "'").casefold()


def check_denied(root: Path, files, words) -> list[str]:
    words = [normalize(w) for w in words if w.strip()]
    if not words:
        return []
    pat = re.compile(r"(?<!\w)(" + "|".join(re.escape(w) for w in words) + r")(?!\w)")
    hits = []
    for p in files:
        try:
            text = p.read_text()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if pat.search(normalize(line)):
                hits.append(f"denied word at {p.relative_to(root)}:{n}")
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--deny", nargs="*", default=[], help="words that must not appear")
    ap.add_argument("--deny-file", help="file with one denied word per line (keep it outside the repo)")
    a = ap.parse_args()

    root = Path(a.root).resolve()
    if not (root / "skills").is_dir():
        print(f"{root} has no skills/ folder; nothing checked")
        sys.exit(2)
    words = list(a.deny)
    if a.deny_file:
        words += Path(a.deny_file).read_text().splitlines()
    files = list(shipped(root))

    problems = check_links(root, files)
    skills = root / "skills"
    if skills.is_symlink():
        problems.append("skills/ is a symlink; not followed")
    else:
        for d in sorted(skills.iterdir()):
            where = d.relative_to(root)
            if d.is_symlink():
                problems.append(f"{where}: symlinked skill folder; not followed")
                continue
            if not d.is_dir() or d.name.startswith("."):
                continue
            p = d / "SKILL.md"
            if p.is_symlink() or not p.is_file():
                problems.append(f"{where}: needs a regular SKILL.md file")
                continue
            problems += check_skill(root, p)
    problems += check_denied(root, files, words)

    for line in problems:
        print(line)
    print(f"{len(problems)} problem(s) in {len(files)} files")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
