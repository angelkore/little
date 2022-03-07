#!/bin/bash

# Activate local env
source app/env/bin/activate

# Run tests
python -m unittest discover app/tests