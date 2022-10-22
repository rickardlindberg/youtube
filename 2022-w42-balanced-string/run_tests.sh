#!/usr/bin/env bash

set -e

python rlmeta/rlmeta.py --support --compile balanced.rlmeta > balanced_rlmeta.py

python balanced.py
