import random
import string
from django import forms
from django.utils import timezone

from .models import Surgeon, OperationType, OperationInstance, Step, StepInstance

class TimeWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        cs = string.ascii_letters + string.digits
        randId = ''.join(random.choice(cs) for _ in range(10))
        js2 = f"""document.getElementById('{randId}-field').value=new Date().toTimeString().split(' ')[0]"""        
        return f'<input type="time" step="1" name="{name}" id="{randId}-field" required=""> <a href="#" onclick="{js2}">Now</a>'





class DateWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        cs = string.ascii_letters + string.digits
        randId = ''.join(random.choice(cs) for _ in range(10))
        js2 = f"""document.getElementById('{randId}-date').valueAsDate = new Date()"""
        return f'<input type="date" name="{name}" id="{randId}-date" required=""> <a href="#" onclick="{js2}">Today</a>'



class OperationTypeForm(forms.ModelForm):
    class Meta:
        model = OperationType
        fields = ['operation_type']

class SurgeonForm(forms.ModelForm):
    class Meta:
        model = Surgeon
        fields = ['first_name', 'last_name', 'email']


class DateInput(forms.DateTimeInput, forms.Widget):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('format', '%H:%M:%S')
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if not value:
            context['widget']['value'] = timezone.localtime().strftime('%H:%M:%S')
        return context

    input_type='time'


class OperationInstanceForm(forms.ModelForm):
    class Meta:
        model = OperationInstance
        fields = ['operation_type', 'date', 'surgeon', 'detail']

        widgets = {
            'date' : DateWidget()
        }

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['title',]


# self.attrs is set within the form widget init
# the variable 'step_name' is hardcoded in there
class TimeWidgetWithStepName(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        cs = string.ascii_letters + string.digits
        randId = ''.join(random.choice(cs) for _ in range(10))
        js2 = f"""document.getElementById('{randId}-field').value=new Date().toTimeString().split(' ')[0]"""        
        return f'<label>{self.attrs["step_name"]}:</label><input type="time" step="1" name="{name}" id="{randId}-field" required=""> <a href="#" onclick="{js2}">Now</a>'

# we're only filling out one additional field with the form
class StepInstanceForm(forms.ModelForm):
    class Meta:
        model = StepInstance
        fields = ['end_time',]
        widgets = {
            'end_time' : TimeWidgetWithStepName(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.instance refers to this model instance
        if self.instance:
            self.fields['end_time'].widget.attrs['step_name'] = self.instance.step.title




"""
class TimerEntryForm(forms.ModelForm):
    class Meta:
        model = TimerEntry
        fields = ['date', 'title', 'start_time', 'end_time', 'detail', 'surgeon', 'operation']
        widgets = {
            #'date' : DateInput(),
            'date' : DateWidget(),
            'start_time' : TimeWidget(),
            'end_time' : TimeWidget(),
        }

"""