# simple script to generate the website

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import jinja2
import markdown
import sass


if __name__=="__main__":
    with open("config.toml", "rb") as fp:
        config = tomllib.load(fp)

    contents_dir = Path(config["contents_dir"])
    data_dir = Path(config["data_dir"])

    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(config["templates_dir"]),
        autoescape=False,
    )

    index_template = template_env.get_template("index.jinja2")
    cv_template = template_env.get_template("cv.jinja2")

    cv = {}
    data = config["data"]

    with open(data_dir / data["contact"], "rb") as fp:
        contact = tomllib.load(fp)

    content = ""
    for element in config["contents"]:
        with open(contents_dir / element["file"], "r", encoding="utf-8") as fp:
            content += f"\n<h2>{element['title']}</h2>\n\n"
            content += markdown.markdown(fp.read())

    with open("sass/style.scss", "r", encoding="utf-8") as fp:
        scss = fp.read()

    output_path = Path("_site")
    output_path.mkdir(parents=True, exist_ok=True)

    with open(output_path / "index.html", "w") as fp:
        fp.write(
            index_template.render(
                config=config, contact=contact, content=content
            )
        )

    with open(output_path / "style.css", "w") as fp:
        fp.write(sass.compile(string=scss))
