# How to Contribute

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and you always earn credits.

You can contribute on the code side in many ways:

* submit feedback,
* add new features,
* report bugs,
* fix bugs,
* write documentation

## Code

### Linting and pre-commit

For every code contribution, the [pre-commit](https://pre-commit.com/index.html) utility should be executed.
This will lint, format and check your code contributions against our guidelines to ensure code quality and consistency
(e.g. we use [Black](https://github.com/psf/black) as code style
and aim for [REUSE compliance](https://reuse.software/)):

1. Installation `conda install -c conda-forge pre-commit` or `pip install pre-commit`
2. Usage:

    * To automatically activate `pre-commit` on every `git commit`: Run `pre-commit install`
    * To manually run it: `pre-commit run --all`

## Documentation

### How to docs?

We add the documentation continuously while the project grows, which makes it easier to understand and maintain for you and the whole community.
We rely on [MkDocs](https://www.mkdocs.org/) and its plugin
[mkdocstrings](https://mkdocstrings.github.io/) to document our scripts and generate the documentation website you are reading.

Feel free to check it yourself by starting to contribute. Every typo counts!

### Structure and Syntax example

The documentation is fully stored in our `doc` folder. Most files are written in Markdown (`.md`), which is very popular and easy to use.

You could differentiate between two elements:

1. Non-automated doc elements. They simply make the text appealing. Example in `installation.md` in our doc folder. To write these requires some knowledge on writing the text which is quite easy to learn having this [cheat sheet](https://www.markdownguide.org/cheat-sheet/) in close reach.
2. Automated doc elements using `mkdocstrings`. What they do is basically to link the code script with the doc texts, for instance, compare the python script [add_electricity.py](https://github.com/pypsa-meets-earth/pypsa-earth/blob/main/scripts/add_electricity.py) with the `api-reference/index.md` documentation. To write these kind of automation, get inspiration from our `api-reference` documentation. Further, to help understanding how things work the official [mkdocstrings documentation](https://mkdocstrings.github.io/) might help too.

We found three important files/file groups for the documentation:

1. `mkdocs.yml`. This is the configuration file for MkDocs and defines the navigation structure.
2. The `.py` script with the actual code documentation (docstrings).

The images for documentation should be placed into [documentation](https://github.com/pypsa-meets-earth/documentation) repository to the folder "doc/img". The content of the folder "documentation/doc/img/" is copied into "pypsa-earth/doc/img/" during building PyPSA-Earth documentation.

Please, if you have problems with the documentation create an issue and let us know.

### How to build it locally

To create the documentation locally, you need [mkdocs](https://www.mkdocs.org/). It can be installed using specifications
from `doc/requirements.txt`. First, we recommend creating a fresh conda environment and activate it:

```bash
.../pypsa-earth-status % conda create --name pypsa-earth-docs python
```

```bash
.../pypsa-earth-status % conda activate pypsa-earth-docs
```

Next, install the packages specified in `doc/requirements.txt` using `pip`:

```bash
.../pypsa-earth-status % pip install -r doc/requirements.txt
```

Once installation is completed, the following commands allow you to create the documentation locally:

```bash
.../pypsa-earth-status (pypsa-earth-docs) % cd doc
```

```bash
.../pypsa-earth-status/doc (pypsa-earth-docs) % mkdocs serve
```

This will start a local server, usually at `http://127.0.0.1:8000/`.
VScode provides a so called Liveserver extension such that the html file can be opened locally on your computer.

The documentation is built automatically by the CI for every pull request. The documentation is hosted on [ReadTheDocs](https://pypsa-earth-status.readthedocs.io/en/latest/).

## No-Code

Instead of contributing code there are alternatives to support the PyPSA-Earth-Status goals.
You can provide reference data, share suggestions and insights, help fellow modellers asking for assistance in [Discord](https://discord.gg/AnuJBk23FU) Support channel, contribute into outreach activities and events, and fund projects.

Feel free to use [this form](https://docs.google.com/forms/d/1udHf6W34YI0UNg3iwQs_-oeKsyj-dzJOtETZ_-RSUhw/edit) to share
your insights and check out our [website](https://pypsa-meets-earth.github.io)
for more details on ways to engage.

## Join us and get involved

Any person/group is welcome to join us. Be it research leader, researcher, undergraduate, or industry professional.
A simple way to explore opportunities for collaboration is to join our meetings. All of them are **OPEN**.

* PyPSA-Earth-Status periodic meeting: Every two weeks on Monday at 16:00 CET/CEST. If interested in joining, we can add you to the calendar invite; just reach out on [Discord](https://discord.gg/AnuJBk23FU) or via email to any of the core developers.
* [List of initiative meetings](https://pypsa-earth.readthedocs.io/en/latest/#get-involved)
* **Discord**

    * Chat with the community, team up on features, exchange with developers, code in voice channels
    * [Discord invitation link](https://discord.gg/AnuJBk23FU)
