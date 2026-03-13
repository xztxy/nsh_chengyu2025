 * Serving Flask app 'app'

 * Debug mode: off

INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.

 * Running on all addresses (0.0.0.0)

 * Running on http://127.0.0.1:8666

 * Running on http://172.30.0.2:8666

INFO:werkzeug:Press CTRL+C to quit

ERROR:app:Exception on / [GET]

Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 392, in decorated_function

    rv = self.cache.get(cache_key)

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 191, in cache

    return app.extensions["cache"][self]

KeyError: 'cache'



During handling of the above exception, another exception occurred:



Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1511, in wsgi_app

    response = self.full_dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 919, in full_dispatch_request

    rv = self.handle_user_exception(e)

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 917, in full_dispatch_request

    rv = self.dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 902, in dispatch_request

    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 410, in decorated_function

    if self.app.debug:

AttributeError: 'Cache' object has no attribute 'app'

INFO:werkzeug:127.0.0.1 - - [13/Mar/2026 02:37:49] "GET / HTTP/1.1" 500 -

ERROR:app:Exception on / [GET]

Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 392, in decorated_function

    rv = self.cache.get(cache_key)

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 191, in cache

    return app.extensions["cache"][self]

KeyError: 'cache'



During handling of the above exception, another exception occurred:



Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1511, in wsgi_app

    response = self.full_dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 919, in full_dispatch_request

    rv = self.handle_user_exception(e)

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 917, in full_dispatch_request

    rv = self.dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 902, in dispatch_request

    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 410, in decorated_function

    if self.app.debug:

AttributeError: 'Cache' object has no attribute 'app'

INFO:werkzeug:127.0.0.1 - - [13/Mar/2026 02:38:19] "GET / HTTP/1.1" 500 -

ERROR:app:Exception on / [GET]

Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 392, in decorated_function

    rv = self.cache.get(cache_key)

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 191, in cache

    return app.extensions["cache"][self]

KeyError: 'cache'



During handling of the above exception, another exception occurred:



Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1511, in wsgi_app

    response = self.full_dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 919, in full_dispatch_request

    rv = self.handle_user_exception(e)

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 917, in full_dispatch_request

    rv = self.dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 902, in dispatch_request

    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 410, in decorated_function

    if self.app.debug:

AttributeError: 'Cache' object has no attribute 'app'

INFO:werkzeug:192.168.15.105 - - [13/Mar/2026 02:38:23] "GET / HTTP/1.1" 500 -

ERROR:app:Exception on / [GET]

Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 392, in decorated_function

    rv = self.cache.get(cache_key)

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 191, in cache

    return app.extensions["cache"][self]

KeyError: 'cache'



During handling of the above exception, another exception occurred:



Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1511, in wsgi_app

    response = self.full_dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 919, in full_dispatch_request

    rv = self.handle_user_exception(e)

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 917, in full_dispatch_request

    rv = self.dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 902, in dispatch_request

    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 410, in decorated_function

    if self.app.debug:

AttributeError: 'Cache' object has no attribute 'app'

INFO:werkzeug:192.168.15.105 - - [13/Mar/2026 02:38:24] "GET / HTTP/1.1" 500 -

ERROR:app:Exception on / [GET]

Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 392, in decorated_function

    rv = self.cache.get(cache_key)

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 191, in cache

    return app.extensions["cache"][self]

KeyError: 'cache'



During handling of the above exception, another exception occurred:



Traceback (most recent call last):

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 1511, in wsgi_app

    response = self.full_dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 919, in full_dispatch_request

    rv = self.handle_user_exception(e)

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 917, in full_dispatch_request

    rv = self.dispatch_request()

  File "/usr/local/lib/python3.9/site-packages/flask/app.py", line 902, in dispatch_request

    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]

  File "/usr/local/lib/python3.9/site-packages/flask_caching/__init__.py", line 410, in decorated_function

    if self.app.debug:

AttributeError: 'Cache' object has no attribute 'app'

INFO:werkzeug:192.168.15.105 - - [13/Mar/2026 02:38:25] "GET / HTTP/1.1" 500 -