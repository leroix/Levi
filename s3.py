from boto.s3.connection import S3Connection
from boto.s3.key import Key

import config

_conn = S3Connection(config.S3_KEY, config.S3_SECRET)
_bucket = _conn.get_bucket(config.S3_BUCKET)

def get(key_name):
    k = Key(_bucket)
    k.key = key_name
    return k.get_contents_as_string()

def set(key_name, value):
    k = Key(_bucket)
    k.key = key_name
    return k.set_contents_from_string(value)

def get_all_keys():
    return _bucket.list()
