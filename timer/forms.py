import random
import string
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

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

# TODO: make this thing error in a way that the formset does, when required=False.
# basically, server side validation instead of client side. 
class StepForm(forms.ModelForm):

    #title = forms.CharField(required=True)

    class Meta:
        model = Step
        fields = ['title',]
    """
    def clean_title(self):
        print("StepForm clean title method")
        value = self.cleaned_data.get('title', '').strip()
        if not value:
            raise forms.ValidationError("This field must not be empty.")
        return value

    def clean(self):
        print("clean method in stepfrm")
        self.clean_title()
        return super().clean()
    """

# TODO bug:
# have like 7 steps generated, delete a step and then it'll still say you need it
# need to fix that -- i think we just need to clear errors somehow befor each validation call?
"""
    def clean(self):
        #Checks that no form in the formset is empty and marks them invalid individually.
        if any(self.errors):  # Skip validation if there are already errors
            return
        ...
        ...
"""
class CustomStepFormSet(forms.BaseModelFormSet):
    def clean(self):
        has_error = False
        step_values = []
        for form in self.forms:

            # check for duplicate step names
            if form.cleaned_data.get('title') in step_values:
                form.add_error('title', f"field {form.cleaned_data.get('title')} already in step list")
                has_error = True
            
            # now check to see if there are empty fields
            elif not form.cleaned_data.get('title'):
                if len(form.errors) == 0:
                    # something else might have added an error to this already... kinda weird
                    form.add_error('title', "this field cannot be empty")
                has_error = True
            else:
                step_values.append(form.cleaned_data.get('title'))
            
        if has_error:
            print("raising validation error in customstepformset")
            raise forms.ValidationError("Validation errors found in step list.")


class CustomStepInstanceFormSet(forms.BaseModelFormSet):
    def clean(self):
        has_error = False
        step_values = []
        for form in self.forms:

            # ensure all time entries follow sequentially and each step's time is before the next step's time
            """
            if form.cleaned_data.get('end_time') in step_values:
                form.add_error('title', f"field {form.cleaned_data.get('title')} already in step list")
                has_error = True
            """
            # now check to see if there are empty fields
            if not form.cleaned_data.get('end_time'):
                if len(form.errors) == 0:
                    # something else might have added an error to this already... kinda weird
                    form.add_error('end_time', "this field cannot be empty")
                has_error = True
            else:
                step_values.append(form.cleaned_data.get('end_time'))
            
        if has_error:
            print("raising validation error in customstepformset")
            raise forms.ValidationError("Validation errors found in step list.")
        


# self.attrs is set within the form widget init
# the variable 'step_name' is hardcoded in there
class TimeWidgetWithStepName(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        cs = string.ascii_letters + string.digits
        randId = ''.join(random.choice(cs) for _ in range(10))
        js2 = f"""if (!(document.getElementById('{randId}-field').disabled)) document.getElementById('{randId}-field').value=new Date().toTimeString().split(' ')[0]"""        
        return f'<label>{self.attrs["step_name"]}:</label><input type="time" step="1" name="{name}" id="{randId}-field" required="" disabled> <a href="#" onclick="{js2}">Now</a>'

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