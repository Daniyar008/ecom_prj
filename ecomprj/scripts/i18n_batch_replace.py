import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"

REPLACEMENTS = [
    (re.compile(r"(<i[^>]*></i>\s*)Add\b"), r"\1{% trans \"Add\" %}"),
    (re.compile(r">\s*Add\s*(?=</a>)"), r">{% trans \"Add\" %}"),
    (re.compile(r">\s*Add\s*(?=</button>)"), r">{% trans \"Add\" %}"),
    (
        re.compile(r">\s*Add to cart\s*(?=</button>|</a>)"),
        r">{% trans \"Add to cart\" %}",
    ),
]


def process_file(path: Path) -> int:
    if path.suffix != ".html":
        return 0
    text = path.read_text(encoding="utf-8")
    original = text
    changed = 0
    for pat, repl in REPLACEMENTS:
        text, n = pat.subn(repl, text)
        changed += n
    if changed:
        backup = path.with_suffix(path.suffix + ".bak2")
        backup.write_text(original, encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path} ({changed} replacements)")
    return changed


if __name__ == "__main__":
    total = 0
    for p in TEMPLATE_DIR.rglob("*.html"):
        if "admin" in p.parts or "staticfiles" in p.parts:
            continue
        total += process_file(p)
    print("Done. total:", total)
