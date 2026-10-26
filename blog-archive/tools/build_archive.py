"""Build the blog archive from masharpe.wordpress.com via the public WordPress.com API.

Usage: python build_archive.py <archive_dir> <post_list.txt>

post_list.txt holds one post URL per line, optionally followed by " extra"
to mark a post as related-but-peripheral. For each post this writes:
  posts/<date>-<slug>.md     Markdown conversion (with YAML front matter)
  html/<date>-<slug>.html    the post's original HTML content, unmodified
  media/<date>-<slug>/...    full-resolution copies of embedded images
and finally an index at posts/INDEX.md.

Requires: requests, beautifulsoup4, markdownify.
"""

import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

API = "https://public-api.wordpress.com/rest/v1.1/sites/masharpe.wordpress.com/posts/slug:{}"
POST_URL_RE = re.compile(r"^https?://masharpe\.wordpress\.com/(\d{4})/(\d{2})/(\d{2})/([^/#?]+)/?(#.*)?$")

# PDFs attached to posts whose LaTeX sources are archived under tex/ instead.
PDF_SOURCES = {
    "mrc_ref_rough_draft_2024_10_15.pdf": "../tex/mrc_ref_2024_10_15/mrc_ref.tex",
    "ptcrn_le_ptoc.pdf": "../tex/ptcrn_le_ptoc/ptcrn_le_ptoc.tex",
    "coupling_example.pdf": "../tex/coupling_example/coupling_example.tex",
}


def name_for(url):
    m = POST_URL_RE.match(url)
    y, mo, d, slug, _ = m.groups()
    return f"{y}-{mo}-{d}-{slug}"


class Converter(MarkdownConverter):
    def convert_pre(self, el, text, parent_tags):
        # WordPress syntaxhighlighter blocks: keep text verbatim in a fenced block.
        body = el.get_text().strip("\n")
        return f"\n\n```\n{body}\n```\n\n"

    def convert_object(self, el, text, parent_tags):
        # PDF embeds (wp-block-file) duplicate the adjacent download link.
        return ""


def convert(content_html, archived, media_dir, media_rel):
    soup = BeautifulSoup(content_html, "html.parser")

    for block in soup.select("div.wp-block-file"):
        a = block.find("a", href=True)
        fname = Path(urlparse(a["href"]).path).name
        note = soup.new_tag("p")
        note.string = f"Attached PDF: {a['href']} (not archived; its LaTeX source is archived at {PDF_SOURCES[fname]})"
        block.replace_with(note)

    for a in soup.find_all("a", href=True):
        href = a["href"]
        m = POST_URL_RE.match(href)
        if m and name_for(href) in archived:
            a["href"] = f"{name_for(href)}.md" + (m.group(5) or "")
        else:
            fname = Path(urlparse(href).path).name
            if fname in PDF_SOURCES:
                a["href"] = PDF_SOURCES[fname]

    for img in soup.find_all("img"):
        src = img.get("src", "")
        full = src.split("?")[0]
        fname = Path(urlparse(full).path).name
        media_dir.mkdir(parents=True, exist_ok=True)
        r = requests.get(full, timeout=60)
        r.raise_for_status()
        (media_dir / fname).write_bytes(r.content)
        img["src"] = f"{media_rel}/{fname}"
        for attr in ("srcset", "sizes", "data-attachment-id", "data-orig-file"):
            img.attrs.pop(attr, None)

    # Literal pipes inside table cells would break Markdown tables.
    for cell in soup.find_all(["td", "th"]):
        for s in cell.find_all(string=True):
            if "|" in s:
                s.replace_with(s.replace("|", "\\|"))

    # Demote headings by one level: the post title becomes the only H1.
    for level in range(5, 0, -1):
        for h in soup.find_all(f"h{level}"):
            h.name = f"h{level + 1}"

    md = Converter(heading_style="ATX", bullets="-", escape_underscores=False).convert_soup(soup)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    return md


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def main():
    root = Path(sys.argv[1])
    entries = []
    for line in Path(sys.argv[2]).read_text().splitlines():
        parts = line.split()
        if parts:
            entries.append((parts[0], len(parts) > 1 and parts[1] == "extra"))
    archived = {name_for(u) for u, _ in entries}

    for sub in ("posts", "html", "media"):
        (root / sub).mkdir(parents=True, exist_ok=True)

    index_rows = []
    for url, extra in entries:
        name = name_for(url)
        slug = POST_URL_RE.match(url).group(4)
        r = requests.get(API.format(slug), timeout=60)
        r.raise_for_status()
        post = r.json()
        assert post["URL"].rstrip("/") == url.rstrip("/"), (post["URL"], url)
        title = html.unescape(post["title"])

        (root / "html" / f"{name}.html").write_text(post["content"])
        body = convert(post["content"], archived, root / "media" / name, f"../media/{name}")
        front = [
            "---",
            f"title: {yaml_str(title)}",
            f"date: {post['date']}",
            f"modified: {post['modified']}",
            f"url: {post['URL']}",
            f"tags: {json.dumps(sorted(post['tags']), ensure_ascii=False)}",
            f"categories: {json.dumps(sorted(post['categories']), ensure_ascii=False)}",
        ]
        if extra:
            front.append("archive_note: related post not in the author's core list")
        front.append("---")
        (root / "posts" / f"{name}.md").write_text("\n".join(front) + f"\n\n# {title}\n\n" + body)
        index_rows.append((post["date"][:10], title, name, extra))
        print("ok", name)

    index_rows.sort(reverse=True)
    lines = ["# Post index (newest first)", "", "| Date | Title | |", "|---|---|---|"]
    for date, title, name, extra in index_rows:
        lines.append(f"| {date} | [{title.replace('|', '\\|')}]({name}.md) | {'extra' if extra else ''} |")
    (root / "posts" / "INDEX.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
