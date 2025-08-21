# simple script to generate the website

import tomllib
from pathlib import Path

import jinja2
import markdown
import sass
import yaml

from locations import Location

if __name__=="__main__":
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("./templates"),
        autoescape=False,
    )

    index_template = template_env.get_template("index.jinja2")
    cv_template = template_env.get_template("cv.jinja2")

    with open("config.toml", "rb") as fp:
        config = tomllib.load(fp)

    locations = {}
    with open("data/locations.toml", "rb") as fp:
        data = tomllib.load(fp)
        for key, location in data.items():
            locations[key] = Location.from_dict(location)

    with open("data/contact.toml", "rb") as fp:
        contact = tomllib.load(fp)

    with open("data/cv.yaml", "rb") as fp:
        cv = yaml.safe_load(fp)

    for job in cv["jobs"]:
        location_key = job["location"]
        job["location"] = locations[location_key].render()

    for degree in cv["degrees"]:
        location_key = degree["location"]
        degree["location"] = locations[location_key].render()

    with open("content/2025_about.md", "r", encoding="utf-8") as fp:
        content = markdown.markdown(fp.read())

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

    with open(output_path / "cv.html", "w") as fp:
        fp.write(cv_template.render(config=config, data=cv))

    with open(output_path / "style.css", "w") as fp:
        fp.write(sass.compile(string=scss))
