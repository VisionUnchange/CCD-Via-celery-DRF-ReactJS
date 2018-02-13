from crispy_forms.bootstrap import StrictButton
from django import forms
from .models import Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout , Field
#from rest_framework.renderers import

class TaskForm(forms.ModelForm):
    #default_renderer = HTMLFormRenderer
    class Meta:
        model = Task
        fields = ['name','curdate','period']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'capfore_tasknew'
        self.helper.add_input(Submit('submit', '创建任务'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'name',
            Field('curdate' , css_class='datepicker',data_provide='datepicker',data_date_format='yyyy-mm-dd', data_date_start_date = '2016-01-01'),
            'period',
        )

class TaskInfoForm(forms.ModelForm):
    #default_renderer = HTMLFormRenderer
    class Meta:
        model = Task
        fields = ['id','name','curdate','period','progress','status']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'



