#!/usr/bin/env python
import sys, subprocess

import s3, crypto, util

import config


# ~~~script inputs
subcmd = sys.argv[1]
params = sys.argv[2:]


# ~~~Utils
gen_param_str = lambda k: '%s=%s' % (k.key, crypto.decrypt(k.get_contents_as_string()))


# ~~~CLI interface
if subcmd == 'set':
    for param in params:
        key,val = param.split('=')
        s3.set(key, crypto.encrypt(val))
    print 'Ik hoorde je. Here is what we have stored:'
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

    is_proceed = util.query_yes_no('Would you like to proceed?')

    if is_proceed:
        ps = []
        pipe = subprocess.PIPE
        for svc in config.SERVICES:
            args = [util.method2script(svc['method'])]
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

if subcmd == 'help':
    print "Levi watches over the community and "
    print "makes sure everyone's following the rules.\n"

    print "./levi.py set apples=good pears=meh oranges=delicious"
    print "\tSet configuration variables."
    print "\tThis just stores them in S3."

    print "./levi.py list"
    print "\tList the configuration variables stored in S3."

    print "./levi.py push"
    print "\tPush the configuration variables out to all services"
    print "\tlisted in config.py"
