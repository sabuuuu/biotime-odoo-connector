"""Scrape the ZKBioTime API docs into Markdown files."""
import os
import re
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

BASE = os.environ.get("BIOTIME_URL", "http://localhost:8083")
PAGES = [
    "",
    "request_and_response.html",
    "get_auth_token.html",
    "use_auth_token.html",
    "api_example.html",
    "area_api.html",
    "department_api.html",
    "position_api.html",
    "employee_api.html",
    "resign_api.html",
    "terminal_api.html",
    "transaction_api.html",
    "att_report.html",
]
OUT = Path(__file__).parent / "zkbiotime_api_docs"


class Converter(MarkdownConverter):
    def convert_pre(self, el, text, parent_tags):
        # Preserve code block language tags
        lang = ""
        wrapper = el.find_parent("div", class_=re.compile(r"language-"))
        if wrapper:
            m = re.search(r"language-(\w+)", " ".join(wrapper.get("class", [])))
            if m:
                lang = m.group(1)
        code = el.get_text()
        return f"\n```{lang}\n{code.rstrip()}\n```\n"


def fetch(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read().decode("utf-8")


def to_md(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one(".theme-default-content")
    for a in content.select("a.header-anchor"):
        a.unwrap()
    for junk in content.select(".line-numbers, .copy-code-button"):
        junk.decompose()
    md = Converter(heading_style="ATX", bullets="-", escape_underscores=False, escape_asterisks=False).convert_soup(content)
    return re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"


def main():
    OUT.mkdir(exist_ok=True)
    combined = ["# ZKBioTime 8.0 API Documentation\n",
                f"Source: {BASE}/docs/api-docs/\n"]
    for i, page in enumerate(PAGES):
        url = f"{BASE}/docs/api-docs/{page}"
        try:
            md = to_md(fetch(url))
        except Exception as e:
            print(f"SKIP {url}: {e}")
            continue
        name = f"{i:02d}_{(page or 'index.html').replace('.html', '')}.md"
        (OUT / name).write_text(md, encoding="utf-8")
        combined.append(f"\n---\n\n<!-- {url} -->\n\n{md}")
        print(f"OK   {name} ({len(md)} chars)")
    (OUT / "ALL_ZKBioTime_API_docs.md").write_text("\n".join(combined), encoding="utf-8")


if __name__ == "__main__":
    main()
