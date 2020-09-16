from copy import deepcopy

import yaml

input_file = open("resume.yaml", "r")
cv_data = yaml.load(input_file, Loader=yaml.Loader)

class MakeDocument():
    _preamble = ""
    _footer = ""
    _title = None

    def __init__(self, raw_data, callable, language):
        self._raw = deepcopy(raw_data)
        self._print = callable
        self._language = str(language)
        return

    def write(self):
        self._print(self._preamble)
        if self._is_section(self._raw):
            self._parse_section(self._raw, 1)
        self._print(self._footer)
        return

    def _is_section(self, item):
        if not isinstance(item, dict):
            return False
        if ("section" not in item) or ("content" not in item):
            return False
        return True

    def _parse_header(self, title, level):
        title = str(title)
        level = int(level)
        if level == 1:
            self._title = title
        self._print(self._render_header(title, level))
        return

    def _parse_snippet(self, snippet, name):
        link_url = None
        raw_text = None

        if isinstance(snippet, dict):
            raw_text = snippet.pop("text", None)
            raw_text = snippet.pop(self._language, raw_text)
            link_url = snippet.pop("link", None)
            if raw_text is None:
                raw_text = ""
                for key, value in snippet.items():
                    if (len(raw_text) > 0) and (key != "volume") and (key !="year"):
                        raw_text += ","
                    raw_text += f" {self._parse_snippet(value, key)}"
        else:
            raw_text = str(snippet)

        if (name == "location") or (name == "year"):
            raw_text = f"({raw_text})"
        if name == "title":
            raw_text = self._render_italic(raw_text)
        if (name == "job-title") or (name == "degree") or (name == "volume"):
            raw_text = self._render_bold(raw_text)

        if name == "paragraph-title":
            raw_text = f"{self._render_bold(raw_text)}: "

        if name == "arXiv":
            link_url = f"https://arxiv.org/abs/{raw_text}"
            raw_text = f"arXiv:{raw_text}"
        if name == "doi":
            link_url = f"https://doi.org/{raw_text}"
            raw_text = f"DOI:{raw_text}"

        if link_url is not None:
            raw_text = self._render_link(raw_text, link_url)

        if self._title in raw_text:
            raw_text = self._render_bold(raw_text)

      #  if (name == "university") or (name == "employer"):
      #      raw_text = self._render_linebreak(raw_text) 
        if name == "dissertation":
            raw_text = f'Dissertation: {self._render_italic(f"“{raw_text}”")}'
        if name == "thesis":
            raw_text = f'Thesis: {self._render_italic(f"“{raw_text}”")}'
        if (name == "dissertation") or (name == "thesis"):
            raw_text = self._render_linebreak(raw_text) 

        return self._render_text(raw_text, name)

    def _parse_paragraph(self, text):
        all_text = ""

        if isinstance(text, list):
            for snippet in text:
                all_text += f"{self._parse_snippet(snippet, None)} "
        else:
            all_text = f"{self._parse_snippet(text, None)} "

        self._print(self._render_paragraph(f"{all_text} "))
        return

    def _parse_item(self, item):
        item_text = ""
        seq = item.pop("period", "")

        for name, value in item.items():
            if isinstance(value, (str, int, float)):
                item_text += f'{self._parse_snippet(f"{value}", name)}. '
            if isinstance(value, dict):
                item_text += f'{self._parse_snippet(value, name)}. '
            if isinstance(value, list):
                for element in value[:-1]:
                    item_text += f"{self._parse_snippet(element, name)}, "
                item_text += f"{self._parse_snippet(value[-1], name)}. "

        return f"{item_text} ", seq

    def _parse_list(self, items):
        list_size = len(items)
        seq = ""
        for item_number, item in enumerate(items):
            if isinstance(item, (str, float, int)):
                item_text = self._parse_snippet(str(item), None)
            if isinstance(item, dict):
                item_text, seq = self._parse_item(item)
            self._print(
                self._render_item(item_text, item_number+1, list_size, seq)
            )
        return

    def _parse_section(self, section, level):
        title = section["section"]
        contents = section["content"]

        self._parse_header(title, level)

        if isinstance(contents, (float, int, str)):
            text = self._parse_snippet(str(contents), None)
            self._parse_paragraph(text)

        if isinstance(contents, list) and (level == 1):
            for item in contents:
                if self._is_section(item):
                    self._parse_section(item, level+1)
                else:
                    for block in item.values():
                        self._parse_paragraph(block)

        if isinstance(contents, list) and (level > 1):
            if all([self._is_section (item) for item in contents]):
                for item in contents:
                    self._parse_section(item, level+1)
            else:
                self._parse_list(contents)

        if isinstance(contents, dict):
            if self._is_section(contents):
                self._parse_section(contents, level+1)
            else:
                self._parse_item(contents)
        return

    def _render_text(self, text, name):
        return f"{text}"

    def _render_link(self, link_text, url):
        return f"[{link_text}]({url})"

    def _render_italic(self, text):
        return f"*{text}*"

    def _render_bold(self, text):
        return f"**{text}**"

    def _render_linebreak(self, text):
        return f"\n   {text}"

    def _render_paragraph(self, text):
        return f"\n{text}\n"

    def _render_header(self, title, level):
        return f"\n{'#'*level} {title}\n"

    def _render_item(self, item_text, item_number, list_size, seq=""):
        if seq != "":
            seq = f"**{seq}**:"

        broken_text = item_text.split()
        mended_text = ""
        buffer = ""
        
        for word in broken_text:
            buffer += f"{word} "
            if len(buffer) > 75:
                if mended_text == "":
                    mended_text += buffer
                else:
                    mended_text += self._render_linebreak(buffer)
                buffer = ""

        if mended_text == "":
            mended_text = buffer
        elif buffer != "":
            mended_text += self._render_linebreak(buffer)

        return f"\n - {seq} {mended_text}\n"



class MakeTeX(MakeDocument):
    _preamble = r"""
\documentclass[a4paper]{article}

\usepackage{hyperref}
\usepackage[utf8]{inputenc}
\usepackage[margin=2cm]{geometry}

\renewcommand{\familydefault}{\sfdefault}

\begin{document}
"""
    _footer = "\end{document}"

    def _render_link(self, link_text, url):
        return f"\\href{{{url}}}{{{link_text}}}"

    def _render_italic(self, text):
        return f"\\textit{{{text}}}"

    def _render_bold(self, text):
        return f"\\textbf{{{text}}}"

    def _render_linebreak(self, text):
        broken_text = text.split()
        mended_text = ""
        buffer = ""
        
        for word in broken_text:
            buffer += f"{word} "
            if len(buffer) > 80:
                if mended_text == "":
                    mended_text += buffer
                else:
                    mended_text += self._render_linebreak(buffer)
                buffer = ""

        if mended_text == "":
            mended_text = buffer
        elif buffer != "":
            mended_text += self._render_linebreak(buffer)

        return f"\n \\\\ \\makebox[2cm]{{}} {mended_text}"

    def _render_paragraph(self, text):
        return f"\n\\begin{{center}} {text} \\end{{center}}\n"

    def _render_header(self, title, level):
        if level == 1:
            return f"\\begin{{center}}\\bf\\huge {title}\\end{{center}}\n"
        if level == 2:
            return f"\\section*{{{title}}}\n"
        return f"\\subsection*{{{title}}}\n"

    def _render_item(self, item_text, item_number, list_size, seq=""):
        if seq != "":
            seq = f" \makebox[2cm]{{\\bf {seq}}}"

        if list_size == 1:
            return f"\\begin{{itemize}} \\item[] {seq} {item_text} \\end{{itemize}}\n"
        if item_number == 1:
            return f"\\begin{{itemize}} \\item[] {seq} {item_text}\n"
        if item_number == list_size:
            return f"\\item[] {seq} {item_text}\n \\end{{itemize}}"
        return f"\\item[] {seq} {item_text}\n"


class MakeHTML(MakeDocument):
    _preamble = u"""
        <!DOCTYPE html>
        <html lang="en">

        <head>
        <meta charset="utf-8">
        <title>Leonardo Andreta de Castro &ndash; LeoAdeC</title>
        <link rel="stylesheet" type="text/css" href="style.css" />
        </head>

        <body>
        <div id="contents">
    """

    _footer = "\n</div></body></html>\n"

    def _render_text(self, text, name):
        return f'<span class="{name}">{text}</span>'

    def _render_link(self, link_text, url):
        return f'<a href="{url}">{link_text}</a>'

    def _render_bold(self, text):
        return f"<strong>{text}</strong>"

    def _render_italic(self, text):
        return f"<em>{text}</em>"

    def _render_linebreak(self, text):
        return f"<br/>{text}"

    def _render_paragraph(self, text):
        return f"<p>{text}</p>\n"

    def _render_header(self, title, level):
        return f"<h{level}>{title}</h{level}>\n"

    def _render_item(self, item_text, item_number, list_size, seq=""):
        if seq != "":
            seq = f'seq="{seq}:"'

        if list_size == 1:
            return f"<ul> <li {seq}> {item_text}</li> </ul>\n"
        if item_number == 1:
            return f"<ul> <li {seq}> {item_text}</li>\n"
        if item_number == list_size:
            return f"<li {seq}> {item_text}</li></ul>\n"
        return f"<li {seq}> {item_text}</li>\n"


markdown_output = open("../README.md", "w")
make_document = MakeDocument(cv_data, markdown_output.write, "en")
make_document.write()

tex_output = open("resume.tex", "w")
make_tex = MakeTeX(cv_data, tex_output.write, "en")
make_tex.write()

html_output = open("../index.html", "w")
make_html = MakeHTML(cv_data, html_output.write, "en")
make_html.write()
