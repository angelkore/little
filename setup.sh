#!/bin/bash

# Setup Virtual Env if it doesn't exist already
if [ ! -d "app/env" ]
then
  python3 -m venv app/env
fi