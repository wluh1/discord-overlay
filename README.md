# discord-overlay

A discord overlay that can be enabled outside of games.

Takes pictures of the desired area and removes the background before displaying
it as an overlay.

Uses template matching to find the up-most voice-channel.

## Installation

The dependencies for the project can be installed with pip using the command:
`pip install -r requirements.txt`

## Build

The program can be built to an executable using pyinstaller with the `build.bat`
batch script.

## Running the program

The program can be run without building by navigating to the `src` directory and
running:
`python app.py`

If the program is built the executable file can be run.

## How it works

## Usage

When starting the program the overlay will be visible and the settings menu will
be minimized in the 'hidden icons' menu.

The settingsmenu can change the placement on the screen, the width of the
overlay and how it calculates height.
