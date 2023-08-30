"""The CLI of nytid"""

import typer
from nytid.cli import courses
import typerconf as config
from nytid.cli import schedule
from nytid.cli import signupsheets

import logging
import sys

logging.basicConfig(format=f"nytid: %(levelname)s: %(message)s")

cli = typer.Typer()

cli.add_typer(courses.cli, name="courses")
config.add_config_cmd(cli)
cli.add_typer(schedule.cli, name="schedule")
cli.add_typer(signupsheets.cli, name="signupsheets")

if __name__ == "__main__":
    cli()
