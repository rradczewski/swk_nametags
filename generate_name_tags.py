#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import json
from pprint import pprint


try:
    # Please do not use 'from scribus import *' . If you must use a 'from import',
    # Do so _after_ the 'import scribus' and only import the names you need, such
    # as commonly used constants.
    import scribus
except ImportError,err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

#########################
# YOUR IMPORTS GO HERE  #
#########################

EVENT_NAME = "SoCraMOB OpenSpace 2015.1"
EVENT_LOCATION = "Münster, 21.03.2015"

STYLE_FIRST_NAME = "FirstName"
STYLE_LAST_NAME = "LastName"
STYLE_META = "Meta"

LOGO_WIDTH = 17.0
LOGO_HEIGHT = 17.0

OFFSETS = [
    {"x": 17.5, "y": 13.5},
    {"x": 112.500, "y": 13.5},

    {"x": 17.5, "y": 68.5},
    {"x": 112.500, "y": 68.5},

    {"x": 17.5, "y": 123.5},
    {"x": 112.500, "y": 123.5},

    {"x": 17.5, "y": 178.5},
    {"x": 112.500, "y": 178.5},

    {"x": 17.5, "y": 233.5},
    {"x": 112.500, "y": 233.5}
]

def drawNameTag(xOff, yOff, participant):
    firstNamePos = {"x": xOff+5.0, "y": yOff+12.5}
    lastNamePos = {"x": xOff+5.0, "y": yOff+21.5}

    firstName = scribus.createText(firstNamePos["x"], firstNamePos["y"], 52, 9)
    scribus.setText(participant["Vorname"], firstName)
    scribus.setStyle(STYLE_FIRST_NAME, firstName)

    lastName = scribus.createText(lastNamePos["x"], lastNamePos["y"], 52, 9)
    scribus.setText(participant["Nachname"], lastName)
    scribus.setStyle(STYLE_LAST_NAME, lastName)
    drawNameTagBox(xOff, yOff)

def drawNameTagBox(xOff, yOff):
    logoPos = {"x": xOff+75.0-LOGO_WIDTH, "y": yOff+11.5}
    metaEventPos = {"x": xOff+5.0, "y": yOff+40.795}
    metaLocationPos = {"x": xOff+5.0, "y": yOff+45.6}

    metaEvent = scribus.createText(metaEventPos["x"], metaEventPos["y"], 70, 9)
    scribus.setText(EVENT_NAME, metaEvent)
    scribus.setStyle(STYLE_META, metaEvent)

    metaLocation = scribus.createText(metaLocationPos["x"], metaLocationPos["y"], 70, 9)
    scribus.setText(EVENT_LOCATION, metaLocation)
    scribus.setStyle(STYLE_META, metaLocation)

def drawLines():
    scribus.createLine(0, 49.767, 210.0, 49.767)
    scribus.createLine(0, 104.678, 210.0, 104.678)
    scribus.createLine(0, 159.678, 210.0, 159.678)
    scribus.createLine(0, 214.678, 210.0, 214.678)
    scribus.createLine(0, 269.678, 210.0, 269.678)

def main(argv):
    with open('participants.json') as data_file:    
        participants = json.load(data_file)

    numOfParticipant = 0
    drawLines()
    for participant in participants:
        relOffset = OFFSETS[numOfParticipant % 10]
        drawNameTag(relOffset["x"], relOffset["y"], participant)
        numOfParticipant = numOfParticipant+1
        if numOfParticipant % 10 == 0:
            scribus.newPage(-1)
            drawLines()

    while numOfParticipant % 10 != 0:
        relOffset = OFFSETS[numOfParticipant % 10]
        drawNameTagBox(relOffset["x"], relOffset["y"])
        numOfParticipant = numOfParticipant + 1

def main_wrapper(argv):
    """The main_wrapper() function disables redrawing, sets a sensible generic
    status bar message, and optionally sets up the progress bar. It then runs
    the main() function. Once everything finishes it cleans up after the main()
    function, making sure everything is sane before the script terminates."""
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)
