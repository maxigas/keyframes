#!/usr/bin/python3
# Extract keyframes from movie
#
# Usage:
# ./keyframes.py input.mov
#
# The heavy lifting is done by ffmpeg, this script mainly adjusts the scene cutoff:
#    ffmpeg -i input.mp4 -vf "select='gt(scene,0.5)'" -vsync 0 frames/frame-%2d.jpg

# === Dependencies === 

import argparse
import os
from subprocess import run

# === Arguments === 

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str,
                    help="Input: file name")
parser.add_argument("-o", "--output", type=str,
                    help="Output directory: keyframes saved here as JPG files")
parser.add_argument("-f", "--filename", type=str,
                    help="Output filename: keyframes file name template")
parser.add_argument("-c", "--cutoff", type=float, default=0.4,
                    help="Cutoff for detecting keyframes: float between 0 and 1 (%)")
parser.add_argument("-s", "--step", type=float, default=0.8,
                    help="Steps changing the cutoff value, between 0 and 1 (%)")
parser.add_argument("-i", "--iterations", type=int, default=24,
                    help="Iterations: how many times to try running the detection")
parser.add_argument("-v", "--verbose", action='store_true',
                    help="Verbose mode on: print more info") # not implemented
parser.add_argument("-l", "--log", type=str, 
                    help="Log: log operations to this file") # not implemented
parser.add_argument("-a", "--min", type=int, default=2,
                    help="From/minimum: Minimum acceptable number of keyframes")
parser.add_argument("-z", "--max", type=int, default=12,
                    help="To/maximum: Maximum acceptable number of keyframes")
args=parser.parse_args()

# === Diagnostics === 

if not os.path.isfile(args.input):
    print("ERROR EX_NOINPUT: Cannot open input")
    raise SystemExit(66) # from systexits.h, EX_NOINPUT aka "cannot open input"

# Set a default value for the output directory, based on input file name
args.output = args.output or f"{args.input}-keyframes/"
# Delete output directory if it exists
if os.path.isdir(args.output):
    for f in os.listdir(args.output): os.unlink(f"{args.output}/{f}")
    os.rmdir(args.output)
# Create output directory
os.makedirs(args.output) 
if args.filename is None:
    print("Setting default value for output filename...")
    args.filename = f"{args.input}".split('.')[:-1][0]
# Set a default value for the filename, based on input file name
args.filename = args.filename or f"{args.input}".split('.')[0]

# === Functions ===

def keyframes():
    if args.iterations == 0:
        print("ERROR: Stopped trying: increase --iterations parameter to try more!")
        raise SystemExit(128)
    command = f"""ffmpeg -i {args.input} -vf "select='gt(scene,{args.cutoff})'" -vsync 0 {args.output}{args.filename}-%2d.jpg"""
    print(f"Running {command}")
    result = run(command, shell=True, capture_output=True) 
    if result.returncode: # Command failed
        print(f"No keyframes found, trying {args.iterations} more times")
        args.cutoff *= args.step
        args.iterations -= 1
        keyframes()
    else:
        countcontrol()

def countcontrol():
    n = len(os.listdir(args.output)) # Number of keyframes found
    print(f"Found {n} keyframes.")
    if n < args.min:
        print("Too few keyframes, let's try again!")
        args.cutoff *= args.step
        keyframes()
    elif n > args.max:
        print("Too many keyframes, let's try again!")
        args.cutoff *= 1+args.step
        keyframes()
    else:
        print(f"Solution found! Check {args.output} directory!")
        striphorizontal()

def striphorizontal():
    command = f"""magick convert +append {args.output}*.jpg {args.output}{args.filename}-keyframes.jpg"""
    print(command)
    result = run(command, shell=True, capture_output=False)
    if not result.returncode: # Command succeeded
        print(f"Keyframes have been saved in a single file under {args.output}{args.filename}-keyframes.jpg")

# === Main ===

keyframes()

