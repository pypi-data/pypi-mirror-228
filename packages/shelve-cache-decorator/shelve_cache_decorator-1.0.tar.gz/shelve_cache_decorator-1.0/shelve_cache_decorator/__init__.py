import datetime
import decorator
import shelve
from hashlib import md5

__all__ =["shelvecached"]

def shelvecached(cache_file, expiry):

    def scached_closure(func, *args, **kw):
        prekey = ':'.join([func.__name__, str(args), str(kw)])
        key = md5(prekey.encode('utf8')).hexdigest()
        d = shelve.open(cache_file)
        if key in d:
            if d[key]['expires_on'] < datetime.datetime.now():
                del d[key]
        if key not in d:
            data = func(*args, **kw)
            d[key] = {
                'expires_on' : datetime.datetime.now() + expiry,
                'data': data,
            }
        result = d[key]['data']
        d.close()
        return result
    return decorator.decorator(scached_closure)
