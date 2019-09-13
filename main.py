


import os
import cherrypy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin
import json
from jinja2 import Template

from pyfit.app import App



Base = declarative_base()
HERE = os.path.dirname(os.path.abspath(__file__))
MOD_DIR = os.path.join(HERE, 'pyfit')
f_pull_up_def  = os.path.join(MOD_DIR,'defs','pull_up.json')
with open(f_pull_up_def, 'r') as f:
    pull_up_def = json.load(f)



def run():
    cherrypy.tools.db = SQLAlchemyTool()
    auto_reload = True
    app_config = {
        'global': {
        'engine.autoreload.on' : auto_reload
        },
        '/': {
            'tools.db.on': True
        },
        '/css':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': os.path.join(MOD_DIR,'css')
        },
    }
    cherrypy.config.update({'engine.autoreload.on' : auto_reload})
    cherrypy.tree.mount(App(os.path.join(MOD_DIR, "defs")), '/', config=app_config)
    #cherrypy.config.update({'server.socket_host': '192.168.0.27'})
    dbfile = os.path.join(MOD_DIR, 'log.db')

    if not os.path.exists(dbfile):
        open(dbfile, 'w+').close()

    sqlalchemy_plugin = SQLAlchemyPlugin(
        cherrypy.engine, Base, 'sqlite:///%s' % (dbfile),
        echo=True
    )
    sqlalchemy_plugin.subscribe()
    sqlalchemy_plugin.create()
    cherrypy.engine.start()
    import webbrowser
    webbrowser.open('http://localhost:8080')
    cherrypy.engine.block()


if __name__ == '__main__':
    run()
