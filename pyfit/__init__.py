


def input_form_from_specs(specs):

    # make individual inputs
    parameters = specs['parameters']
    parameters_html = []
    for pname, specs in parameters.items():
        ptype = specs['type'] 
        if ptype == "categorical":
            template = Template("""
            <select name="{{pname}}">
                {% for val in values %}
                    <option value="{{val}}">{{val}}</option>
                {% endfor %}
            </select> 
            """)
            phtml = template.render(pname=pname, values=specs['values'])
            parameters_html.append((pname,phtml))
        else:
            raise NotImplementedError()

    template =  Template('''
    <html>
      <head>
        <title> {{title}} </title>
        <link rel="stylesheet"  href="/css/mystyle.css">
      </head>
      <body>
        <form action='/' method='post'>
            <div class="grid-container">
                {% for phtml in parameters_html %}
                     <div class="grid-item"> {{phtml[0]}} </div>
                     <div class="grid-item"> {{phtml[1]}} </div>
                {% endfor %}
                <div class="grid-item"> <input type="submit">  </div>
                 
            </div> 
        </form>
        %s
      </body>
    <html>
    ''')
    html = template.render(title=specs['name'], parameters_html=parameters_html)
    return html


