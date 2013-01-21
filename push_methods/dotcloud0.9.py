#!/usr/bin/env python
import sys
import subprocess


cmd = ['dotcloud', 'env', 'set', '-A', sys.argv[1]] + sys.argv[2:]
subprocess.Popen(cmd)
