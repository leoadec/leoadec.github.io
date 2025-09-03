# simple script to generate the website

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import jinja2
import markdown
import sass

from authors import Author
from conferences import Conference
from degrees import Degree
from grants import Grant
from jobs import Job
from locations import Location
from papers import Paper
from posters import Poster
from talks import Talk
from theses import Thesis


@dataclass
class KeyCache:
    authors: dict[str, Author]
    locations: dict[str, Location]

    @classmethod
    def from_config(cls, config: dict) -> Self:
        data_dir = Path(config["data_dir"])

        locations = {}
        with open(data_dir / config["data"]["locations"], "rb") as fp:
            data = tomllib.load(fp)
            for key, location in data.items():
                locations[key] = Location.from_dict(location)

        with open(data_dir / config["data"]["authors"], "rb") as fp:
            authors = {
                key: Author.from_dict(author) for key, author in tomllib.load(fp).items()
            }

        return cls(authors=authors, locations=locations)

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

    cache = KeyCache.from_config(config)

    with open(data_dir / data["contact"], "rb") as fp:
        contact = tomllib.load(fp)

    with open(data_dir / data["posters"], "rb") as fp:
        posters = {
            key: Poster.from_dict(poster, cache.authors) for key, poster in tomllib.load(fp).items()
        }

    with open(data_dir / data["grants"], "rb") as fp:
        grants = {
            key: Grant.from_dict(grant) for key, grant in tomllib.load(fp).items()
        }

    with open(data_dir / data["theses"], "rb") as fp:
        theses = {
            key: Thesis.from_dict(thesis, cache.authors) for key, thesis in tomllib.load(fp).items()
        }

    with open(data_dir / data["talks"], "rb") as fp:
        talks = {
            key: Talk.from_dict(talk, cache.authors) for key, talk in tomllib.load(fp).items()
        }

    with open(data_dir / data["jobs"], "rb") as fp:
        cv["jobs"] = [
            Job.from_dict(job, cache.locations).render()
            for job in tomllib.load(fp).values()
        ]

    with open(data_dir / data["degrees"], "rb") as fp:
        cv["degrees"] = [
            Degree.from_dict(degree, locations=cache.locations, grants=grants, theses=theses).render()
            for degree in tomllib.load(fp).values()
        ]

    with open(data_dir / data["papers"], "rb") as fp:
        cv["papers"] = [
            Paper.from_dict(paper, cache.authors).render()
            for paper in tomllib.load(fp).values()
        ]

    with open(data_dir / data["conferences"], "rb") as fp:
        cv["conferences"] = [
            Conference.from_dict(conference, locations=cache.locations, posters=posters, talks=talks).render()
            for conference in tomllib.load(fp).values()
        ]

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

    with open(output_path / "cv.html", "w") as fp:
        fp.write(
            cv_template.render(config=config, data=cv)
        )

    with open(output_path / "style.css", "w") as fp:
        fp.write(sass.compile(string=scss))
