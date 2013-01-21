#!/usr/bin/env python
import sys
import subprocess


cmd = ['heroku', 'config:add', '--app', sys.argv[1]] + sys.argv[2:]
subprocess.Popen(cmd)

