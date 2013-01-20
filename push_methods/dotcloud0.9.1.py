#!/usr/bin/env python
import sys
import subprocess


def push(app_name, params):
    subprocess.Popen(['ls', '-l'])


if __name__ == "__main__":
    push(sys.argv[1], sys.argv[2:])
