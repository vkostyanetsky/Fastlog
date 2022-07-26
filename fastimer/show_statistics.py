#!/usr/bin/env python3

import datetime

# noinspection PyPackageRequirements
from consolemenu import PromptUtils

from .fasts_file import read_fasts
from .utils import get_active_fast, get_time_difference, print_with_alignment


def show_statistics(prompt_utils: PromptUtils) -> None:

    fasts = read_fasts()

    __print_completed_fasts(fasts)
    __print_total_fasting_time(fasts)
    __print_average_fast_length(fasts)

    print()
    prompt_utils.enter_to_continue()


def __print_completed_fasts(fasts: list) -> None:

    value = __get_completed_fasts(fasts)
    value = str(value)

    __print_with_alignment("Completed Fasts", value)


def __print_total_fasting_time(fasts: list) -> None:

    total_hours, total_minutes = __get_total_hours_and_minutes(fasts)

    value = "{hours}h {minutes}m".format(
        hours=int(total_hours), minutes=int(total_minutes)
    )

    __print_with_alignment("Total Fasting Time", value)


def __print_average_fast_length(fasts: list) -> None:

    hours_total, minutes_total = __get_total_hours_and_minutes(fasts)

    minutes_per_hour = 60
    completed_fasts = __get_completed_fasts(fasts)


    avg_fast_length = (
        (hours_total * 60 + minutes_total) / completed_fasts // minutes_per_hour
    )

    value = "{hours}h".format(hours=int(avg_fast_length))

    __print_with_alignment("Average Fast Length", value)


def __print_with_alignment(title: str, value: str):

    print_with_alignment(title, value, 22)


def __get_completed_fasts(fasts: list) -> int:

    completed_fasts = len(fasts)

    return completed_fasts if get_active_fast(fasts) is None else completed_fasts - 1


def __get_total_hours_and_minutes(fasts: list) -> tuple:

    total_hours = 0
    total_minutes = 0

    for fast in fasts:
        started = fast["started"]
        stopped = (
            fast.get("stopped")
            if fast.get("stopped") is not None
            else datetime.datetime.now()
        )

        hours, minutes = get_time_difference(started, stopped)

        total_hours += hours
        total_minutes += minutes

    minutes_per_hour = 60

    if total_minutes >= minutes_per_hour:
        hours = total_minutes // minutes_per_hour
        total_minutes = total_minutes % minutes_per_hour
        total_hours += hours

    return total_hours, total_minutes
