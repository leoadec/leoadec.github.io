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

    with open("data/jobs.toml", "rb") as fp:
        jobs = [
            Job.from_dict(job, locations) for job in tomllib.load(fp).values()
        ]

    with open("data/contact.toml", "rb") as fp:
        contact = tomllib.load(fp)

    with open("data/authors.toml", "rb") as fp:
        authors = {
            key: Author.from_dict(author) for key, author in tomllib.load(fp).items()
        }

    with open("data/posters.toml", "rb") as fp:
        posters = {
            key: Poster.from_dict(poster, authors) for key, poster in tomllib.load(fp).items()
        }

    with open("data/grants.toml", "rb") as fp:
        grants = {
            key: Grant.from_dict(grant) for key, grant in tomllib.load(fp).items()
        }

    with open("data/theses.toml", "rb") as fp:
        theses = {
            key: Thesis.from_dict(thesis, authors) for key, thesis in tomllib.load(fp).items()
        }

    with open("data/talks.toml", "rb") as fp:
        talks = {
            key: Talk.from_dict(talk, authors) for key, talk in tomllib.load(fp).items()
        }

    with open("data/conferences.toml", "rb") as fp:
        conferences = [
            Conference.from_dict(conference, locations=locations, posters=posters, talks=talks)
            for conference in tomllib.load(fp).values()
        ]

    with open("data/papers.toml", "rb") as fp:
        papers = [
            Paper.from_dict(paper, authors) for paper in tomllib.load(fp).values()
        ]

    with open("data/degrees.toml", "rb") as fp:
        degrees = [
            Degree.from_dict(degree, locations=locations, grants=grants, theses=theses)
            for degree in tomllib.load(fp).values()
        ]

    cv = {
        "jobs": [job.render() for job in jobs],
        "conferences": [conference.render() for conference in conferences],
        "papers": [paper.render() for paper in papers],
        "degrees": [degree.render() for degree in degrees],
    }

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
