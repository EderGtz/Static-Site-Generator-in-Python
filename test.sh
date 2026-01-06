#!/usr/bin/env bash
#Script used to run all tests created to verify the units of the code works as expected

#runs all the tests that find in src dir using unittest testing framework
python3 -m unittest discover -s src
