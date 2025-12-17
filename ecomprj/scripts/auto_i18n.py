import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"

# map of phrase -> regex pattern to replace
PHRASES = [
    "Add to cart",
    "Add",
    "View cart",
    "Cart",
    "Sign In",
    "Sign out",
    "Login",
    "Register",
    "Price",
    "Total",
    "Quantity",
    "Unit Price",
    "Track Your Order",
    "Best Prices & Offers",
    "Save to 50%",
    "Search for items...",
    "Search",
    "Submit & Register",
]

# Patterns to find text nodes: captures leading tag open through the phrase and closing tag
TAG_ENDS = [
    "</a>",
    "</button>",
    "</span>",
    "</h1>",
    "</h2>",
    "</h3>",
    "</td>",
    "</th>",
    "</label>",
]
EXTRA_PATTERNS = [
    (r"(<i[^>]*></i>\s*)Add\b", r"\1{% trans \"Add\" %}"),
    (r">\s*Add\s*(?=<)", r">{% trans \"Add\" %}"),
]


def ensure_load_i18n(text: str) -> str:
    if "{% load i18n %}" in text:
        return text
    # insert after first line if it's a template tag or at top
    lines = text.splitlines()
    insert_at = 0
    for i, line in enumerate(lines[:5]):
        if line.strip().startswith("{%") or line.strip().startswith("<!"):
            insert_at = i + 1
    lines.insert(insert_at, "{% load i18n %}")
    return "\n".join(lines)


def wrap_phrase_in_text(text: str, phrase: str) -> (str, int):
    count = 0
    for end in TAG_ENDS:
        # match > optional spaces phrase optional spaces then end
        pattern = rf">\s*{re.escape(phrase)}\s*(?={re.escape(end)})"
        repl = rf">{{% trans \"{phrase}\" %}}"
        new_text, n = re.subn(pattern, repl, text)
        if n:
            text = new_text
            count += n
    return text, count


def process_file(path: Path) -> int:
    if path.suffix != ".html":
        return 0
    text = path.read_text(encoding="utf-8")
    original = text
    text = ensure_load_i18n(text)
    total = 0
    for phrase in PHRASES:
        text, c = wrap_phrase_in_text(text, phrase)
        total += c
    # extra generic patterns
    for pat, repl in EXTRA_PATTERNS:
        new_text, n = re.subn(pat, repl, text)
        if n:
            text = new_text
            total += n
    if text != original:
        backup = path.with_suffix(path.suffix + ".bak")
        backup.write_text(original, encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path} ({total} replacements)")
    return total


if __name__ == "__main__":
    total = 0
    for p in TEMPLATE_DIR.rglob("*.html"):
        # skip admin static templates
        if "admin" in p.parts or "staticfiles" in p.parts:
            continue
        total += process_file(p)
    print("Done. Total replacements:", total)
