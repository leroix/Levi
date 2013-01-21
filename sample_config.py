## ~~~S3 settings
## Levi stores all the global settings that you store in S3
S3_KEY      = 'XXXXXXXXXXXXXXXXXXXX'
S3_SECRET   = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
S3_BUCKET   = 'global-settings'

## ~~~Encryption settings
## Levi encrypts each settings before sending it to S3 for extra security
CRYPTO_KEY = """{
    "hmacKey": {
        "hmacKeyString": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
        "size": 256
    }, 
    "aesKeyString": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
    "mode": "CBC", 
    "size": 256
}"""

## ~~~Service settings
## Levi sends your settings to your services using the specified "method".
## The "method" can be a builtin method (i.e. dotcloud, dotcloud0.4, heroku)
## or it can be a user-created script in any language. "args" is a list of 
## command-line arguments that will be submitted to the "method" script. 
## For instance, fakesvc requires one command-line argument. So, facesvc
## will be invoked as follows: 
## /home/lebanonlevi/fakesvc.py fakeservice var1=something var2=somethingelse ...
SERVICES = [
        {'args': ['rbetachinook'], 'method': 'dotcloud'},
        {'args': ['rbetatophat'], 'method': 'heroku'},
        {'args': ['fakeservice'], 'method': '/home/lebanonlevi/fakesvc.py'},
        {'args': [], 'method': 'test'},
]

