import datetime
from enum import Enum
import ics.icalendar
import logging
import pathlib
import sys
import typer
from typing_extensions import Annotated

from nytid.cli import courses as coursescli
from nytid.cli.signupsheets import SIGNUPSHEET_URL_PATH
from nytid import courses as courseutils
from nytid import schedules as schedutils
from nytid.signup import hr
from nytid.signup import sheets

import os
from nytid.signup import sheets
from nytid.signup import utils
from nytid.signup import hr

cli = typer.Typer(name="hr", help="Manage sign-up sheets for teaching")


def to_hours(td):
    return td.total_seconds() / 60 / 60


try:
    default_username = os.environ["USER"]
except KeyError:
    default_username = None

username_opt = typer.Option(
    help="Username to filter sign-up sheet for, "
    "defaults to logged in user's username."
)


@cli.command()
def time(
    course: Annotated[str, coursescli.course_arg_regex],
    register: Annotated[str, coursescli.register_opt_regex] = coursescli.MINE,
):
    """
    Summarizes the time spent on teaching the course(s).
    """
    registers = coursescli.registers_regex(register)
    courses = {
        course_reg: courseutils.get_course_config(*course_reg)
        for course_reg in coursescli.courses_regex(course, registers)
    }
    if not courses:
        sys.exit(1)

    booked = []
    for (course, register), config in courses.items():
        url = config.get(SIGNUPSHEET_URL_PATH)
        if "docs.google.com" in url:
            url = sheets.google_sheet_to_csv_url(url)
        booked += sheets.read_signup_sheet_from_url(url)

    h_per_student = hr.hours_per_student(booked)

    for event, hours in h_per_student.items():
        print(f"{event}: {to_hours(hours):.2f} h/student")

    print(
        f"Booked: {to_hours(hr.total_hours(booked)):.2f} h "
        f"({to_hours(hr.max_hours(booked)):.2f} h)\n"
    )

    print("# Amanuenser")

    amanuensis = hr.compute_amanuensis_data(booked)

    for user, data in amanuensis.items():
        if not user:
            continue
        print(
            f"{user}: {data[2]:.2f} h, "
            f"{100*hr.compute_percentage(*data):.1f}%: "
            f"{data[0].format('YYYY-MM-DD')}--{data[1].format('YYYY-MM-DD')}"
        )

    print()
    print("# Hourly")

    for user, hours in hr.hours_per_TA(booked).items():
        if not user or user in amanuensis:
            continue
        print(f"{user}: {to_hours(hours):.2f} h")


@cli.command()
def users(
    course: Annotated[str, coursescli.course_arg_regex],
    register: Annotated[str, coursescli.register_opt_regex] = coursescli.MINE,
):
    """
    Prints the list of all usernames booked on the course.
    """
    registers = coursescli.registers_regex(register)
    courses = {
        course_reg: courseutils.get_course_config(*course_reg)
        for course_reg in coursescli.courses_regex(course, registers)
    }
    if not courses:
        sys.exit(1)

    booked = []
    for (course, register), config in courses.items():
        url = config.get(SIGNUPSHEET_URL_PATH)
        if "docs.google.com" in url:
            url = sheets.google_sheet_to_csv_url(url)
        booked += sheets.read_signup_sheet_from_url(url)

    for user in hr.hours_per_TA(booked):
        print(user)
