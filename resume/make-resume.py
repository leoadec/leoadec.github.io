from copy import deepcopy

import yaml

input_file = open("resume.yaml", "r")
cv_data = yaml.load(input_file, Loader=yaml.Loader)

class MakeDocument():
    def __init__(self):
        self._code = ""

    def _finish(self):
        return

    def _render_text(self, text):
        self._code += str(text)
        return

    def _render_list(self, data_list, callable):
        for element in data_list:
            self._code += "- "
            callable(element)
            self._code += "\n"
        return

    def _render_header(self, section, level):
        self._code += f"{'#'*level} {section}\n"
        return 

    def _render_dict(self, seq, dictionary, callable):
        self._code += f" {seq}:"
        for element in dictionary.values():
            self._code += " " 
            callable(element)
            self._code += "."
        return

    def _render(self, data, level):
        if isinstance(data, (float, int, str)):
            self._render_text(data)
        if isinstance(data, list):
            if level<=2:
                for element in data:
                    self._render(element, level)
            if level>2:
                self._render_list(data, lambda x: self._render(x, level))
        if isinstance(data, dict):
            if ("section" in data) and ("content" in data):
                self._render_header(data["section"], level)
                self._render(data["content"], level+1)
            else:
                seq = data.pop("period", "")
                self._render_dict(
                    seq,
                    data,
                    lambda x: self._render(x, level)
                )
        return 

    def render(self, data):
        self._render(data, level=1)
        self._finish()
        return self._code

class MakeTeX(MakeDocument):
    def __init__(self):
        self._code = r"""
\documentclass[a4paper]{article}                                            
                                                                            
\usepackage{hyperref}                                                       
\usepackage[utf8]{inputenc}                                                 
\usepackage[margin=2cm]{geometry}                                           
                                                                            
\renewcommand{\familydefault}{\sfdefault}                                   
                                                                            
\begin{document}
"""

    def _finish(self):
        self._code += "\end{document}"

    def _render_list(self, data_list, callable):
        self._code += r"\begin{itemize}"
        for element in data_list:
            self._code += "\item{ "
            callable(element)
            self._code += "}\n"
        self._code += r"\end{itemize}"
        return

    def _render_header(self, section, level):
        self._code += f"\section*{{{section}}}\n"
        return 

    def _render_dict(self, seq, dictionary, callable):
        self._code += f"\\textbf{{{seq}}}:"
        for element in dictionary.values():
            self._code += " " 
            callable(element)
            self._code += "."
        self._code += "\n"
        return

class MakeHTML(MakeDocument):
    def __init__(self):
        self._code = u"""
        <!DOCTYPE html>
        <html lang="en">

        <head>
        <meta charset="utf-8">
        <title>Leonardo Andreta de Castro &ndash; LeoAdeC</title>
        <link rel="stylesheet" type="text/css" href="style.css" />
        </head>

        <body>
        <div class="box">
"""

    def _finish(self):
        self._code += u"""
        <p><a href="resume.pdf">Résumé in PDF</a></p>
"""
        self._code += "</div></body></html>"

    def _render_list(self, data_list, callable):
        self._code += "<ul>\n"
        for element in data_list:
            callable(element)
        self._code += "</ul>\n"
        return

    def _render_header(self, section, level):
        self._code += f"<h{level}>{section}</h{level}>\n"
        return 

    def _render_dict(self, seq, dictionary, callable):
        self._code += f"<li seq=\"{seq}\">"
        counter = 0
        for name, element in dictionary.items():
            self._code += f" <span class=\"{name}\">" 
            callable(element)
            self._code += ".</span>"
            counter += 1
            if counter%2==0:
                self._code += "<br/>"
        self._code += "</li>\n"
        return


markdown_output = open("../README.md", "w")
make_document = MakeDocument()
markdown_output.write(make_document.render(deepcopy(cv_data)))

tex_output = open("resume.tex", "w")
make_tex = MakeTeX()
tex_output.write(make_tex.render(deepcopy(cv_data)))

html_output = open("../index.html", "w")
make_html = MakeHTML()
html_output.write(make_html.render(deepcopy(cv_data)))
