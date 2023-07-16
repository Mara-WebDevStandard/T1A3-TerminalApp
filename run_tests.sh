#!/bin/bash

if ! [[ -x "$(command -v pytest)" ]] then
    echo 'Error:
    Pytest is required to run the tests for this program.
    Please ensure Pytest is installed and accessible in PATH.
    To install Pytest, please install it using a package manager like Pip' >&2
    exit 1
else
    pytest src/test_blackjack.py "$@"
fi