from copy import deepcopy

import yaml

input_file = open("resume.yaml", "r")
cv_data = yaml.load(input_file, Loader=yaml.Loader)

class MakeDocument():
    _preamble = ""
    _footer = ""
    _title = None

    def __init__(self, raw_data, callable):
        self._code = ""
        self._raw = deepcopy(raw_data)
        self._print = callable
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

    def _parse_snippet(self, snippet):
        if isinstance(snippet, dict):
            link_text = snippet.pop("text")
            link_url = snippet.pop("link")
            text = self._render_link(link_text, link_url)
        else:
            text = str(snippet)

        if text == self._title:
            self._print(self._render_bold(text))
            return
        self._print(self._render_text(text, None))
        return

    def _parse_item(self, item):
        item_text = ""
        seq = item.pop("period", "")

        for name, value in item.items():
            if isinstance(value, str):
                item_text += self._render_text(value, name)
            if isinstance(value, list):
                for element in value:
                    item_text += f"{str(element)}, "

        return item_text, seq

    def _parse_list(self, items):
        list_size = len(items)
        seq = ""
        for item_number, item in enumerate(items):
            if isinstance(item, (str, float, int)):
                item_text = self._print(self._parse_snippet(str(item)))
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
            self._parse_snippet(str(contents))

        if isinstance(contents, list):
            if all([self._is_section(item) for item in contents]):
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
        return f"{text}. "

    def _render_link(self, link_text, url):
        return f"[{link_text}]({url})"

    def _render_bold(self, text):
        return f"**{text}**"

    def _render_header(self, title, level):
        return f"{'#'*level} {title}\n"

    def _render_item(self, item_text, item_number, list_size, seq=""):
        line_break = "\n"
        return f" - {item_text.replace(line_break, ' ')}\n"



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

    def _render_text(self, text, name):
        return f"{text}. "

    def _render_link(self, link_text, url):
        return f"\\href{{{url}}}{{{link_text}}}"

    def _render_bold(self, text):
        return f"\\textbf{{{text}}}"

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

    _footer = u"""
        <p><a href="resume.pdf">Résumé in PDF</a></p>
        </div></body></html>
    """

    def _render_text(self, text, name):
        return f'<span class="{name}">{text}</span>. '

    def _render_link(self, link_text, url):
        return f'<a href="{url}">{link_text}</a>'

    def _render_bold(self, text):
        return f"<strong>{text}</strong>"

    def _render_header(self, title, level):
        return f"<h{level}>{title}</h{level}>\n"

    def _render_item(self, item_text, item_number, list_size, seq=""):
        if seq == "":
            seq = f'seq="•"'
        else:
            seq = f'seq="{seq}:"'

        if list_size == 1:
            return f"<ul> <li {seq}> {item_text}</li> </ul>\n"
        if item_number == 1:
            return f"<ul> <li {seq}> {item_text}</li>\n"
        if item_number == list_size:
            return f"<li {seq}> {item_text}</li></ul>\n"
        return f"<li {seq}> {item_text}</li>\n"


markdown_output = open("../README.md", "w")
make_document = MakeDocument(cv_data, markdown_output.write)
make_document.write()

tex_output = open("resume.tex", "w")
make_tex = MakeTeX(cv_data, tex_output.write)
make_tex.write()

html_output = open("../index.html", "w")
make_html = MakeHTML(cv_data, html_output.write)
make_html.write()
