from . import FreePractice
from . import Qualifying
from . import Sprint
from . import Race

# TODO : Functions to create the different objects


def get_fp(year, gp):
    # TODO : verify if year and gp are legit
    return FreePractice.FreePractice(year, gp)


def get_quali(year, gp):
    # TODO : verify if year and gp are legit
    return Qualifying.Qualifying(year, gp)


def get_sprint(year, gp, format):
    return Sprint.Sprint(year, gp, format)


def get_race(year, gp):
    return Race.Race(year, gp)
