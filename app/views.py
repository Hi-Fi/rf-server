from flask import render_template, make_response, request
from flask_appbuilder import BaseView, expose
from app import appbuilder, db
from robot import run
import os.path
from datetime import datetime
import uuid
import networkx as nx
import xml.etree.ElementTree
from app.forms import ArgumentForm


"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()


class MyView(BaseView):
    route_base = "/robot"
    output_dir = os.path.dirname(__file__) + '/../work/'

    @expose('/arguments', methods=['GET', 'POST'])
    def set_robot_arguments(self):
        form = ArgumentForm()
        if request.method == 'POST':
            resp = make_response(self.render_template("arguments.html", title="Set arguments", form=form))
            resp.set_cookie("argument1", form.argument1.data)
            resp.set_cookie("argument2", form.argument2.data)
            resp.set_cookie("secret_argument", form.secret_argument.data)
        else:
            form.argument1.default = self.cookie_or_default(request, "argument1", "argument1")
            form.argument2.default = self.cookie_or_default(request, "argument2", "argument2")
            form.secret_argument.default = self.cookie_or_default(request, "secret_argument", "secret_argument")
            resp = make_response(self.render_template("arguments.html", title="Set arguments", form=form))
        return resp

    def cookie_or_default(self, incoming_request, cookie_key, default_value):
        return  incoming_request.cookies.get(cookie_key) if incoming_request.cookies.get(cookie_key) else default_value

    @expose('/runs')
    def list_robot_runs(self):
        # do something with param1
        # and return it
        self.update_redirect()
        directories = os.listdir(self.output_dir)
        directory_list = []
        for directory in directories:
            directory_list.append({"name": directory,
                                   "completed": datetime.fromtimestamp(os.path.getctime(self.output_dir + directory)).strftime("%d.%m.%Y %H:%M:%S")})
        return self.render_template('robot_runs.html', runs=directory_list)

    @expose('/run/<string:param1>')
    def robot_run_results(self, param1):
        # do something with param1
        # and return it
        output = xml.etree.ElementTree.parse(self.output_dir+param1+'/output.xml')
        nodes = []
        edges = []
        for elem in output.findall(".//suite") + output.findall(".//test"):
            if elem.attrib.get('id'):
                bg_color = "green" if elem.tag == "suite" else "yellow"
                doc = " - "+elem.find('doc').text if elem.find("doc") is not None else ''
                label = elem.attrib.get('name') if elem.tag != "test" else elem.attrib.get('name')+doc
                nodes.append({"id": elem.attrib.get('id'), "value": {"label": label, "labelStyle": "fill:#000;", "style": "fill:"+bg_color+";" }})
                parent = output.find(".//*[@id='"+elem.attrib.get('id')+"']/...")
                if parent and parent.attrib.get('id'):
                    if elem.tag == "test" and not elem.attrib.get("id").endswith("t1"):
                        parent_id = elem.attrib.get("id").split("-").pop().replace('t', '')
                        parent_id = elem.attrib.get("id")[:-int(len(parent_id))]+str(int(parent_id)-1)
                        edges.append({"u": parent_id, "v": elem.attrib.get('id')})
                    else:
                        edges.append({"u": parent.attrib.get('id'), "v": elem.attrib.get('id')})
                if elem.tag == "test":
                    parent_id = elem.attrib.get("id")
                    self.handle_keyword_calls(nodes, edges, parent_id, elem)
        run_id = param1
        print(run_id)
        return self.render_template('robot_run.html', run_id=run_id, nodes=nodes, edges=edges)

    def handle_keyword_calls(self, nodes, edges, parent_id, elem):
        for kw in elem.findall("./kw"):
            kw_id = str(uuid.uuid4())
            nodes.append({"id": kw_id,
                          "value": {"label": kw.attrib.get('name'), "labelStyle": "fill:#000;",
                                    "style": "fill:grey;"}})
            edges.append({"u": parent_id, "v": kw_id})
            parent_id = kw_id
            self.handle_keyword_calls(nodes, edges, parent_id, kw)

    @expose('/run')
    def run_robot(self):
        # do something with param1
        # and return it
        run_id = str(uuid.uuid4())
        run_output_dir = self.output_dir + run_id
        os.mkdir(run_output_dir)
        argument1 = self.cookie_or_default(request, "argument1", "argument1")
        argument2 = self.cookie_or_default(request, "argument2", "argument2")
        argument3 = self.cookie_or_default(request, "secret_argument", "secret_argument")
        with open(run_output_dir+'/run.log', 'w') as logfile:
            result = run(os.path.dirname(__file__) + '/../tests', outputdir=run_output_dir, report=None, log=None, stdout=logfile, stderr=logfile, variable=["argument1:"+argument1, "argument2:"+argument2, "secret_argument:"+argument3] )
        json_results = open(run_output_dir+'/output.xml', 'r').read()
        self.update_redirect()
        resp = make_response(self.render_template('robot_run.html', outputdir=run_output_dir, run_id=run_id, result=json_results))
        return resp


appbuilder.add_view(MyView(), name='Robot')


