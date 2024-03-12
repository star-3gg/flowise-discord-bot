# Flowise API Client Discord Bot

Python implementation of a discord bot for Flowise queries that supports slash commands

## For Users that want to Make Use of this Bot

### Installation

1. Create a `.env` from the provided `.env.example` and update it accordingly

2. Start the docker container using docker-compose:

```sh
docker-compose up
```

3. All Done.

### Usage

The following slash-commands can be used in your discord server, developers can always add new ones or create an issue on this repository:

- `/ace <your question...>` Takes in a text question and responds with text
- `/echo` Responds with text `delta`. This is used for testing purposes during development

All commands are automatically completed, once you start typing `/`.

## For Developers

### Virtual environment

Install the `python-venv` package for virtual environment support:

```sh
sudo pacman -Sy python python-venv
```

Create a virtual environment using the command:

```sh
python -m venv .venv
```

Activate the created virtual environment using the command:

```sh
source .venv/bin/Activate
```

Install the dependencies in your virtual environment:
```sh
pip install -r requirements.txt
```
