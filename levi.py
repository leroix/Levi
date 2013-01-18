#!/usr/bin/env python
import sys

import s3, crypto


subcmd = sys.argv[1]
params = sys.argv[2:]


if subcmd == 'set':
    for param in params:
        key,val = param.split('=')
        s3.set(key, crypto.encrypt(val))
    print 'Roger that.'

if subcmd == 'list':
    for k in s3.get_all_keys():
        print '%s=%s' % (k.key, 
                           crypto.decrypt(k.get_contents_as_string()))

if subcmd == 'push':
    pass


