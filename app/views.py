from flask import render_template, make_response, request
from flask_appbuilder import BaseView, expose
from app import appbuilder, db, storage, tasks
from robot import run, rebot
from os import path, mkdir, system, listdir, rename
import uuid
import xml.etree.ElementTree
from app.forms import ArgumentForm
from app import models
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
    output_dir = '/tmp/'
    try:
        mkdir(output_dir)
    except:
        pass

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
        directory_list = models.get_executions()
        return self.render_template('robot_runs.html', runs=directory_list)

    @expose('/run/<string:param1>')
    def robot_run_results(self, param1):
        # do something with param1
        # and return it
        storage.get_file(param1, 'output.xml')
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
                if parent is not None and parent.attrib.get('id'):
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
        argument1 = self.cookie_or_default(request, "argument1", "argument1")
        argument2 = self.cookie_or_default(request, "argument2", "argument2")
        argument3 = self.cookie_or_default(request, "secret_argument", "secret_argument")
        tasks.create_execution_task(run_id,
                                    {"argument1": argument1},
                                    {"argument2": argument2},
                                    {"secret_argument": argument3})
        models.create_execution(run_id)
        resp = make_response(self.render_template('robot_run.html', outputdir=self.output_dir + run_id, run_id=run_id))
        return resp

    @expose('/execute', methods=["POST"])
    def execute_robot(self):
        payload = request.get_json()
        print('Printed task payload: {}'.format(payload))
        run_id = payload['run_id']
        run_output_dir = self.output_dir + run_id
        try:
            mkdir(run_output_dir)
        except:
            pass
        variable_list = []
        for variable in payload['variables']:
            for key, value in variable.items():
                variable_list.append(key+":"+value)
        with open(run_output_dir+'/run.log', 'w') as logfile:
            run(path.dirname(__file__) + '/../tests',
                outputdir=run_output_dir,
                report=None,
                log=None,
                stdout=logfile,
                stderr=logfile,
                variable=variable_list
               )
        models.update_execution(run_id=run_id, status="executed")
        storage.upload_file(run_id, 'output.xml')
        storage.upload_file(run_id, 'run.log')
        tasks.create_metrics_task(run_id)
        tasks.create_parsing_task(run_id)
        return 'Printed task payload: {}'.format(payload)

    @expose('/generate/reports', methods=['POST'])
    def parse_output_xml(self):
        payload = request.get_json()
        run_id = payload['run_id']
        run_output_dir = self.output_dir + run_id
        storage.get_file(run_id, 'output.xml')
        with open(run_output_dir+'/rebot.log', 'w') as stdout:
            rebot(self.output_dir+run_id+'/output.xml',
                  outputdir=run_output_dir,
                  stdout=stdout)
        storage.upload_file(run_id, "rebot.log")
        report_link = storage.upload_file(run_id, "report.html")
        log_link = storage.upload_file(run_id, "log.html")
        models.add_storage_link(run_id, "report", report_link)
        models.add_storage_link(run_id, "log", log_link)
        return "Parsed log files"

    @expose('/generate/metrics', methods=['POST'])
    def parse_to_metrics(self):
        payload = request.get_json()
        run_id = payload['run_id']
        storage.get_file(run_id, 'output.xml')
        run_output_dir = self.output_dir+run_id+'/'
        generate_metrics = "robotmetrics --inputpath {} -E False".format(run_output_dir)
        system(generate_metrics)
        metrics_file = [f for f in listdir(run_output_dir) if f.startswith('metrics')][0]
        rename(run_output_dir+metrics_file, run_output_dir+'metrics.html')
        metrics_link = storage.upload_file(run_id, "metrics.html")
        models.add_storage_link(run_id, "metrics", metrics_link)
        return "Generated RF metrics"


appbuilder.add_view(MyView(), name='Robot')


