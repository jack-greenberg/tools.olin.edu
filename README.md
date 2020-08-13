<img src="./docs/images/logo.png" width="40%" alt="Tools.Olin" />

Flask app with React frontend for maintaining machine shop trainings @ [Olin College](http://olin.edu).

---

<p align="center">
  <a href="https://travis-ci.org/jack-greenberg/tools.olin.edu">
    <img src="https://img.shields.io/travis/jack-greenberg/tools.olin.edu.svg?logo=travis" alt="Build Status" />
  </a>
  <a href="https://codecov.io/gh/jack-greenberg/tools.olin.edu">
    <img src="https://codecov.io/gh/jack-greenberg/tools.olin.edu/branch/main/graph/badge.svg" alt="Code Coverage" />
  </a>
</p>

#### 🔗 Quick Links

[tools.olin.edu](https://tools.olin.edu) | [proposal.md](./docs/proposal.md)



## 🧰 How it works?

The backend is built with Python's Flask web framework, which is essentially used as a middleware for the database. The bulk of database transactions and queries occur via GraphQL.



### 🔄 Routes `tools.routes`

GraphQL is used for queries on the three main datatypes. Queries are used to fetch data, mutations are used to modify and delete data. This is a departure from the standard REST API that handles CRUD (create, read, update, delete) operations.



### 📃 Database Schemas `tools.database`

There are 3 main schema types defined:

* User
* Tool
* Training

Trainings are generic objects, for example "Beginning Lathe Training" or "Green Machine Training", which link to a list of tools. Users are linked to Trainings by so-called UserTrainings, which would be an instance of a user working on a Training. UserTrainings have `status`es, like `STARTED`, `READING`, and `COMPLETE` which are used to indicate the stage of the training.

Database schemas and models can be seen in the `/tools/database` folder.



### 👤 Authentication `tools.auth`

User login uses single sign-on with AzureAD via Python's msal library. The user clicks a link that takes them to a Microsoft page and prompts them to login with their Olin credentials, and upon success, Microsoft makes a callback request to `/auth/token` returning a secret user code that can be used to fetch JSON web tokens (JWTs).



## Extras

### Building

Builds are handled with **Docker**. I chose Docker because it makes things easy for deployment and allows for high control over development environment. The Dockerfile uses two build stages, one for dependencies which can be cached, and one that includes the actual source code of the platform. The base image is one that I built that is just an Ubuntu 18.04 image that has some basic necessities installed along with Poetry (see below).

Continuous integration happens with **Travis**. You can check out the travis configuration file for more details.

### Backend

Python dependencies are managed with [**Poetry**](https://python-poetry.org/), and can be installed using `poetry install`. The database is a **PostgreSQL** docker image that uses [**alembic**](https://alembic.sqlalchemy.org/en/latest/) to manage migrations.

I decided to use [**Nox**](https://nox.thea.codes/en/stable/) to manage testing automation. Unittests are located in the `/tests` folder. Linting happens with [**Flake8**](https://flake8.pycqa.org/en/latest/#), and code style is [**Black**](https://github.com/psf/black). See **Running Locally** below for getting it all working.

### Frontend

The frontend of the platform uses **ReactJS**. Styles are all written with **SCSS**.



## Running Locally

### Prerequisites

You must be have [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04) and [docker-compose](https://docs.docker.com/compose/install/) installed on your computer (the links take you to installation guides). It helps to have Python3.7 running locally, but it shouldn't matter since everything will be run in a Docker container.

### Installation

The quickest way to build the docker images is to run

```bash
$ docker-compose build
```

Once that is finished, run

```bash
$ docker-compose up -d
```

to setup the containers.

### Testing

To run tests, there are a couple options. You can `exec` into the container (if you aren't familiar with docker, think about it like `ssh`ing into another computer with a new environment) and run tests manually like so:

```
$ docker exec -ti tools-backend bash

/tools # pytest -svra tests/ --cov
```

Alternatively, if you want to run the entire suite of tools (pytest, safety, flake8) without leaving your local environment, you can run

```
$ docker exec -ti tools-backend nox
```



## Collaborating

If you want to collaborate, I invite you to get in touch with me and we can discuss what needs doing, and you can submit a pull request. Also feel free to open issues for bugs or feature requests (although features are generally dictated by the machine shop staff).



## Thank yous

Big thanks to Daniela and Lucas in the machine shop who let me work on this project.
