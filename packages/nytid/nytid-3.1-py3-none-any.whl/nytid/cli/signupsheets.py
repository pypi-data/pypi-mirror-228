import datetime
from enum import Enum
import ics.icalendar
import logging
import pathlib
import sys
import typer
from typing_extensions import Annotated

from nytid.cli import courses as coursescli
from nytid import courses as courseutils
from nytid import schedules as schedutils
from nytid.signup import hr
from nytid.signup import sheets

from nytid.signup import sheets
from nytid.signup import utils
import os, platform, subprocess
from nytid.signup import sheets
from nytid.signup import utils
from nytid.signup import hr

SIGNUPSHEET_URL_PATH = "signupsheet.url"

cli = typer.Typer(name="signupsheets", help="Manage sign-up sheets for teaching")


def to_hours(td):
    return td.total_seconds() / 60 / 60


outpath_opt = typer.Option(
    help="Path where to write the sign-up sheet "
    "files. Default is in each course's "
    "data path."
)
edit_opt = typer.Option(help="If specified, opens each generated sheet " "for editing.")
url_arg = typer.Argument(
    help="The URL for the sign-up sheet. "
    "For Google Sheets, it's the same URL as the "
    "one shared with TAs to sign up. "
    "For others, it's a URL to a CSV file."
)


@cli.command(name="generate")
def generate_signup_sheet(
    course: Annotated[str, coursescli.course_arg_regex],
    register: Annotated[str, coursescli.register_opt_regex] = coursescli.MINE,
    outpath: Annotated[pathlib.Path, outpath_opt] = None,
    edit: Annotated[bool, edit_opt] = False,
):
    """
    Generates a sign-up sheet to be used with Google Sheets or similar for TAs to
    sign up.
    """
    registers = coursescli.registers_regex(register)
    courses = {
        course_reg: courseutils.get_course_config(*course_reg)
        for course_reg in coursescli.courses_regex(course, registers)
    }
    if not courses:
        sys.exit(1)

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M")
    for (course, register), course_conf in courses.items():
        num_students = course_conf.get("num_students")
        num_groups = course_conf.get("num_groups")

        group_size = round(num_students / num_groups)

        def needed_TAs(event):
            return utils.needed_TAs(event, group_size=group_size)

        if not outpath:
            data_root = courseutils.get_course_data(course, register)
            outfile = data_root.path / f"signup-{course}-{timestamp}.csv"
        else:
            outfile = outpath / f"signup-{course}-{timestamp}.csv"

        url = course_conf.get("ics")
        sheets.generate_signup_sheet(outfile, url, needed_TAs)
        if edit:
            the_os = platform.system()
            if the_os == "Darwin":
                subprocess.call(["open", outfile])
            elif the_os == "Windows":
                os.startfile(outfile)
            else:
                subprocess.call(["xdg-open", outfile])


@cli.command()
def set_url(
    course: Annotated[str, coursescli.course_arg_regex],
    url: Annotated[str, url_arg],
    register: Annotated[str, coursescli.register_opt_regex] = coursescli.MINE,
):
    """
    Sets the URL of the sign-up sheet for the course(s).
    """
    registers = coursescli.registers_regex(register)
    courses = {
        course_reg: courseutils.get_course_config(*course_reg)
        for course_reg in coursescli.courses_regex(course, registers)
    }
    if not courses:
        sys.exit(1)
    for _, conf in courses.items():
        conf.set(SIGNUPSHEET_URL_PATH, url)


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
