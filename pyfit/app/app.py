


import os
import cherrypy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer
import json
from jinja2 import Template


from .. input_form_from_specs import input_form_from_specs


Base = declarative_base()
HERE = os.path.dirname(os.path.abspath(__file__))
f_pull_up_def  = os.path.join(HERE,'..','defs','pull_up.json')
with open(f_pull_up_def, 'r') as f:
    pull_up_def = json.load(f)

print(pull_up_def)

class ExerciseDefintions(Base):

    __tablename__ = 'exercise_definition'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    definition = Column(String)

class LogMessage(Base):

    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    value = Column(String)


class App(object):

    def __init__(self, json_folder):
      self.json_folder = json_folder
    @property
    def db(self):
        return cherrypy.request.db


    def make_page(self, edef):
      return input_form_from_specs(edef)



    @cherrypy.expose
    def index(self):
      html = """
      <html>
      <head>
        <title> Select </title>
        <link rel="stylesheet"  href="/css/mystyle.css">
      </head>
      <body>
        <form action='/exercise_selected' method='post'>
            <div class="grid-container">
               <div class="grid-item"> 
                   <select name="exercise_name"  onchange="this.form.submit()">
                        <option value="PullUps">PullUps</option>
                        <option value="PushUps">PushUps</option>
                        <option value="Dips">Dips</option>                    
                  </select> 
               </div>
            </div> 
        </form>
        <p id="demo"></p>

        <script>
        function myFunction() {
          var x = document.getElementById("exercise_name").value;
          document.getElementById("demo").innerHTML = "You selected: " + x;
        }
        </script>


      </body>
    <html>

      """
      return html


    @cherrypy.expose
    def exercise_selected(self, exercise_name):
        return "exercise selected: {}".format(exercise_name)


    @cherrypy.expose
    def index2(self, message=None, submit=None):
        if message:
            self.db.add(LogMessage(value=message))
            self.db.commit()
            raise cherrypy.HTTPRedirect('/')


        page = self.make_page(pull_up_def)

        ol = ['<ol>']
        for msg in self.db.query(LogMessage).all():
            ol.append('<li>%s</li>' % msg.value)
        ol.append('</ol>')

        return page % ('\n'.join(ol))
