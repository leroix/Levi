#!/usr/bin/env python
import sys, subprocess

import s3, crypto

import config


# ~~~script inputs
subcmd = sys.argv[1]
params = sys.argv[2:]


# ~~~Utils
gen_param_str = lambda k: '%s=%s' % (k.key, crypto.decrypt(k.get_contents_as_string()))

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def method2script(name):
    builtins = {'dotcloud': './push_methods/dotcloud0.9.1.py',
                'dotcloud0.4.7': './push_methods/dotcloud0.4.7.py',
                'heroku': './push_methods/heroku.py',}
    return builtins.get(name, name)


# ~~~CLI interface
if subcmd == 'set':
    for param in params:
        key,val = param.split('=')
        s3.set(key, crypto.encrypt(val))
    print 'Roger that. Here is what we have stored:'
    for k in s3.get_all_keys():
        print gen_param_str(k)

if subcmd == 'list':
    for k in s3.get_all_keys():
        print gen_param_str(k)

if subcmd == 'push':
    params = []
    print 'Configuration settings to be pushed:'
    for k in s3.get_all_keys():
        paramstr = gen_param_str(k)
        params.append(paramstr)
        print '\t' + paramstr

    print '\nServices they will be pushed to:'
    for svc in config.SERVICES:
        print '\t' + str(svc) + '\n'

    is_proceed = query_yes_no('Would you like to proceed?')

    if is_proceed:
        ps = []
        pipe = subprocess.PIPE
        for svc in config.SERVICES:
            args = [method2script(svc['method'])]
            args.extend(svc['args'])
            args.extend(params)
            p = subprocess.Popen(args, stdin=pipe, stdout=pipe, stderr=pipe)
            ps.append(p)
        
        while ps:
            p = ps.pop()
            if p.poll() is not None:
                stdouttext, stderrtext = p.communicate()
                print '----------------------------------'
                print stdouttext
                print stderrtext
            else:
                ps.append(p)
