from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder import SimpleFormView, expose
from app import appbuilder

class MyForm(DynamicForm):
    field1 = StringField(('Field1'),
        description=('Your field number one!'),
        validators = [DataRequired()], widget=BS3TextFieldWidget())
    field2 = StringField(('Field2'),
        description=('Your field number two!'), widget=BS3TextFieldWidget())


class MyFormView(SimpleFormView):
    form = MyForm
    form_title = 'Robot job runner'
    message = 'Run was started'
    route_base = "/"

    @expose('/run')
    def form_get(self, form):
        form.field1.data = 'This was prefilled'

    def form_post(self, form):
        # post process form
        print(self.message, 'info')


appbuilder.add_view(MyFormView, "My form View", icon="fa-group", label=_('Robot job runner'),
                    category="Robot", category_icon="fa-cogs")
