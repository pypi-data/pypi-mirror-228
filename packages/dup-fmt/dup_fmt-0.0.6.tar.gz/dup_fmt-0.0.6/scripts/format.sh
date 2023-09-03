#!/bin/sh -e
set -x

ruff dup_fmt tests scripts --fix
black dup_fmt tests scripts
mypy dup_fmt
