#!/usr/bin/env python
import sys

import tornado
import tornado.wsgi

import django.core.wsgi
import os


"""
settings
"""
production = {
    'DJANGO_SETTINGS_MODULE': 'django_base.settings_prod',
    'DEBUG': False,
    'PORT': 80,
}

development = {
    'DJANGO_SETTINGS_MODULE': 'django_base.settings',
    'DEBUG': True,
    'PORT': 8000,
}


"""
Usage: python tornadoserver.py <production>
"""
conf = development
if len(sys.argv) > 1 and sys.argv[1] == 'production':
    conf = production


"""
Create the django app that sits in a wsgi container. Environment can
be set like this since we'll always stay in this process.
"""
os.environ['DJANGO_SETTINGS_MODULE'] = conf['DJANGO_SETTINGS_MODULE']
django_app = tornado.wsgi.WSGIContainer(
                 django.core.wsgi.get_wsgi_application())


if __name__ == '__main__':
    """
    The tornado server routes urls as follows:
    ================  =================
    /static/*         StaticFileHandler
    eeverything else  django_app
    ================  =================
    """
    server = tornado.web.Application(
        [
            (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'}),
            ('.*', tornado.web.FallbackHandler, {'fallback': django_app}),
        ],
        debug=conf['DEBUG']
    )
    if conf['DEBUG'] == True:
        print "Listening on port {} ...".format(conf['PORT'])

    server.listen(conf['PORT'])

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
