# simple script to generate the website

import tomllib
from pathlib import Path

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



if __name__=="__main__":
    with open("config.toml", "rb") as fp:
        config = tomllib.load(fp)

    data_dir = Path(config["data_dir"])

    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(config["templates_dir"]),
        autoescape=False,
    )

    index_template = template_env.get_template("index.jinja2")
    cv_template = template_env.get_template("cv.jinja2")

    cv = {}

    locations = {}
    with open(data_dir / config["locations"], "rb") as fp:
        data = tomllib.load(fp)
        for key, location in data.items():
            locations[key] = Location.from_dict(location)

    with open(data_dir / config["contact"], "rb") as fp:
        contact = tomllib.load(fp)

    with open(data_dir / config["authors"], "rb") as fp:
        authors = {
            key: Author.from_dict(author) for key, author in tomllib.load(fp).items()
        }

    with open(data_dir / config["posters"], "rb") as fp:
        posters = {
            key: Poster.from_dict(poster, authors) for key, poster in tomllib.load(fp).items()
        }

    with open(data_dir / config["grants"], "rb") as fp:
        grants = {
            key: Grant.from_dict(grant) for key, grant in tomllib.load(fp).items()
        }

    with open(data_dir / config["theses"], "rb") as fp:
        theses = {
            key: Thesis.from_dict(thesis, authors) for key, thesis in tomllib.load(fp).items()
        }

    with open(data_dir / config["talks"], "rb") as fp:
        talks = {
            key: Talk.from_dict(talk, authors) for key, talk in tomllib.load(fp).items()
        }

    with open(data_dir / config["jobs"], "rb") as fp:
        cv["jobs"] = [
            Job.from_dict(job, locations).render()
            for job in tomllib.load(fp).values()
        ]

    with open(data_dir / config["degrees"], "rb") as fp:
        cv["degrees"] = [
            Degree.from_dict(degree, locations=locations, grants=grants, theses=theses).render()
            for degree in tomllib.load(fp).values()
        ]

    with open(data_dir / config["papers"], "rb") as fp:
        cv["papers"] = [
            Paper.from_dict(paper, authors).render()
            for paper in tomllib.load(fp).values()
        ]

    with open(data_dir / config["conferences"], "rb") as fp:
        cv["conferences"] = [
            Conference.from_dict(conference, locations=locations, posters=posters, talks=talks).render()
            for conference in tomllib.load(fp).values()
        ]

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
        fp.write(
            cv_template.render(config=config, data=cv)
        )

    with open(output_path / "style.css", "w") as fp:
        fp.write(sass.compile(string=scss))
