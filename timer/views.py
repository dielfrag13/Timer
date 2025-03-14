from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.forms import modelformset_factory

# Create your views here.    
from django.core.exceptions import ValidationError

from .models import Surgeon, OperationType
from .forms import *
from .tables import *

from datetime import datetime, date

def index(request):

    surgeon_list = Surgeon.objects.all().order_by('-pk')[:5]
    operation_list = OperationType.objects.all().order_by('-pk')[:5]

    if request.method == "POST":
        isSurgeon = False
        isOperation = False
        for fieldName in SurgeonForm().fields.keys():
            if fieldName not in request.POST:
                isSurgeon = False
                break
            isSurgeon = True
            newSurgeonForm = SurgeonForm(request.POST)
            if newSurgeonForm.is_valid():
                newSurgeonEntry = newSurgeonForm.save()
                return redirect('timer:index')
        if not isSurgeon:
            # check to see if it's an Operation
            for fieldName in OperationInstanceForm().fields.keys():
                if fieldName not in request.POST:
                    isOperation = False
                    break
                isOperation = True
                newOperationInstanceForm = OperationInstanceForm(request.POST)
                if newOperationInstanceForm.is_valid():
                    newOperationInstanceEntry = newOperationInstanceForm.save()
                    return redirect("timer:ocs1", operation_instance_id=newOperationInstanceEntry.pk)
        if not (isSurgeon or isOperation):
            # it's an OperationForm
            newOperationTypeForm = OperationTypeForm(request.POST)
            if newOperationTypeForm.is_valid():
                newOperationType = newOperationTypeForm.save()
                return redirect('timer:index')


    else:
        surgeonForm = SurgeonForm()
        operationTypeForm = OperationTypeForm()
        operationInstanceForm = OperationInstanceForm()

    context = {
        "surgeon_list" : surgeon_list,
        "operation_list" : operation_list,
        "operation_type_form" : operationTypeForm,
        "surgeon_form" : surgeonForm,
        "operation_instance_form" : operationInstanceForm,

    }
    return render(request, "timer/index.html", context)


def surgeons(request):
    surgeon_list = Surgeon.objects.all()

    if request.method == "POST":
        surgeonForm = SurgeonForm(request.POST)
        if surgeonForm.is_valid():
            newSurgeon = surgeonForm.save()
            return redirect('timer:surgeon_detail', surgeon_id=newSurgeon.id)
    else:
        surgeonForm = SurgeonForm()


    context = {
        "surgeon_list" : surgeon_list,
        "surgeon_form" : surgeonForm,
        "surgeon_table" : SurgeonTable(surgeon_list)
    }
    return render(request, "timer/surgeons.html", context)


def operations(request):
    operation_list = OperationType.objects.all()
    if request.method == "POST":
        operation_type_form = OperationTypeForm(request.POST)
        if operation_type_form.is_valid():
            newOperationType = operation_type_form.save()
            return redirect('timer:operation_type_detail', surgeon_id=newOperationType.id)
    else:
        operation_type_form = OperationTypeForm()
    
    operation_type_table = OperationTypeTable(operation_list)
    context = {
        "operation_list" : operation_list,
        "operation_type_form" : operation_type_form,
        "operation_type_table" :  operation_type_table,
        }
    return render(request, "timer/operations.html", context)




def surgeon_detail(request, surgeon_id):
    thing = get_object_or_404(Surgeon, pk=surgeon_id)
    context = {'surgeonEntry' : thing}
    if request.method == "POST":
        surgeonEntryForm = SurgeonForm(request.POST)
        if surgeonEntryForm.is_valid():
            newSurgeon = surgeonEntryForm.save()
            return redirect('timer:surgeon_detail', surgeon_id=newSurgeon.id)
    else:
        surgeonEntryForm = SurgeonForm()
    context['surgeonEntryForm'] = surgeonEntryForm

    complete_surgeries = OperationInstance.objects.filter(surgeon__id=surgeon_id, complete=True)
    if complete_surgeries:
        context["complete_surgeon_operation_entries"] = OperationInstanceTable(complete_surgeries)

    incomplete_surgeries = OperationInstance.objects.filter(surgeon__id=surgeon_id, complete=False)
    if incomplete_surgeries:
        context["incomplete_surgeon_operation_entries"] = OperationInstanceTable(incomplete_surgeries)
    

    """
    if qs:
        qs_nums = qs.values_list("elapsed_time", flat=True)
        avg = sum(qs_nums) / len(qs_nums)
        for entry in qs:
            percentage_str = f"{(((entry.elapsed_time - avg) / avg)*100):.2f}%"
            entry.dist_from_average = percentage_str
    """

    return render(request, "timer/entry_details/surgeon_entry_detail.html", context)


def operation_type_detail(request, operation_id):
    this_operation_type = get_object_or_404(OperationType, pk=operation_id)
    if request.method == "POST":
        operation_type_form = OperationTypeForm(request.POST)
        if operation_type_form.is_valid():
            newOperationType = operation_type_form.save()
            return redirect('timer:operation_type_detail', operation_id=newOperationType.id)
    else:
        operation_type_form = OperationTypeForm()
    
    operation_instance_entries = OperationInstance.objects.filter(operation_type=this_operation_type)
    """
    qs = TimerEntry.objects.filter(operation__id=operation_id)
    if qs:
        qs_nums = qs.values_list("elapsed_time", flat=True)
        avg = sum(qs_nums) / len(qs_nums)
        for entry in qs:
            percentage_str = f"{(((entry.elapsed_time - avg) / avg)*100):.2f}%"
            entry.dist_from_average = percentage_str
    """

    context = {
        "this_operation_type" : this_operation_type,
        #"operation_type_form" : operation_type_form,
        "operation_instance_entries_table" : OperationInstanceTable(operation_instance_entries),

    }
    return render(request, "timer/entry_details/operation_entry_detail.html", context)


def operation_instance_detail(request, operation_instance_id):
    op_inst = get_object_or_404(OperationInstance, pk=operation_instance_id)

    # redirect to a creation step if this op_inst isn't coplete
    if op_inst.complete == False:
        if op_inst.ocs1 == True:
            return redirect('timer:ocs2', operation_instance_id=operation_instance_id)
        else:
            return redirect('timer:ocs1', operation_instance_id=operation_instance_id)

    # calculate the distance from average from the perspective of each individual step instance
    for step_instance in op_inst.steps.all():
        # get all step instances of this step type
        # can get all step instances for this type, or just the ones referring to this individual surgeon
        # ask darrin which

        # option: ALL step instances, from all surgeries (and all surgeons)
        #all_step_instances = StepInstance.objects.filter(step=step_instance.step)

        # option: step instances associated solely with this operation's surgeon
        all_step_instances = StepInstance.objects.filter(step=step_instance.step, operation_instance__surgeon=op_inst.surgeon)

        if all_step_instances:
            asi_nums = all_step_instances.values_list("elapsed_time", flat=True)
            avg = sum(asi_nums) / len(asi_nums)
            percentage_str = f"{(((step_instance.elapsed_time - avg) / avg)*100):.2f}%"
            step_instance.dist_from_average = percentage_str
            step_instance.save()
    
    context = {
        "operation_instance" : op_inst,
        "operation_instance_table" : OperationInstanceTable(OperationInstance.objects.filter(pk=op_inst.pk)),
        "step_instance_table" : StepInstanceTable(op_inst.steps.all()),
    }
    return render(request, "timer/entry_details/operation_instance_detail.html", context)

def operation_creation_step_one(request, operation_instance_id):


    op_inst = get_object_or_404(OperationInstance, pk=operation_instance_id)

    # ensure we're on the right page and aren't repeating a step
    if op_inst.complete == True:
        return redirect('timer:operation_instance_detail', operation_instance_id=operation_instance_id)
    elif op_inst.ocs1 == True:
        return redirect('timer:ocs2', operation_instance_id=operation_instance_id)

    # if there are steps associated with this operation instance type, we want no extra elements.
    if StepInstance.objects.filter(operation_instance__operation_type=op_inst.operation_type).count() > 0:
        StepFormSet = modelformset_factory(Step, form=StepForm, formset=CustomStepFormSet, extra=0)
        print("extra is 0")
    else:
        StepFormSet = modelformset_factory(Step, form=StepForm, formset=CustomStepFormSet, extra=1)
        print("extra is 1")
    #StepFormSet = modelformset_factory(Step, fields=["title",], extra=0)

    # TODO bug: if you delete one step and then add a new step, double bug. 
    if request.method == "POST":
        formset = StepFormSet(request.POST)
        # clear out prior errors or errors set not as part of custom formset field validation
        for form in formset:
            if 'title' in form.errors:
                del form.errors['title']
            if 'id' in form.errors:
                del form.errors['id']
        
        if formset.is_valid():
            form_order = 1
            for form in formset:
                if form.has_changed():
                    new_model = Step(title=form.cleaned_data['title'])
                    new_model.save()
                    step = new_model
                else:
                    if form.is_valid():
                        form.save()
                    
                    step = form.cleaned_data['id']

                # create new StepInstances and link them to this OperationInstance                
                si = StepInstance.objects.create(step=step, order=form_order, operation_instance=op_inst)
                form_order += 1
            op_inst.ocs1 = True
            op_inst.save()
            return redirect("timer:ocs2", operation_instance_id=operation_instance_id)
        else:
            print("formset is not valid -- ocs1!")
            #import code
            #code.interact(local=locals())
    else:
        most_recent_op = OperationInstance.objects.filter(surgeon=op_inst.surgeon, operation_type=op_inst.operation_type, complete=True).exclude(id=op_inst.id).last()
        if most_recent_op:
            formset = StepFormSet(queryset=Step.objects.filter(instances__in=most_recent_op.steps.all()))
        else:
            formset=StepFormSet(queryset=Step.objects.none())
    context = {
        "formset" : formset,
        "operation_instance" : op_inst,

    }
    return render(request, 'timer/add_templates/add_operation_steps.html', context)


def operation_creation_step_two(request, operation_instance_id):

    """continue via creating a new ModelForm form for StepInstances using existing queryset info"""
    op_inst = get_object_or_404(OperationInstance, pk=operation_instance_id)

    # if this is not the right page, redirect accordingly
    if op_inst.ocs1 == False:
        return redirect("timer:ocs1", operation_instance_id=operation_instance_id)
    elif op_inst.complete == True:
        return redirect('timer:operation_instance_detail', operation_instance_id=operation_instance_id)


    StepInstanceFormSet = modelformset_factory(StepInstance, form=StepInstanceForm, formset=CustomStepInstanceFormSet, extra=0)
    steps = op_inst.steps.all()
    saved_data = {}

    if request.method == "POST":
        formset = StepInstanceFormSet(request.POST)
        if formset.is_valid():
            # low priority potential bug:
            # if the user clicks 'start' and then manually sets the first time to be before when the operation started,
            # then the first step's time calculation will be off. 
            # formset validation will ensure every step is greater in value than every following step. 
            # do we want to be able to manually edit the start time?
            start_time = datetime.strptime(request.POST['start-time'], "%H:%M:%S").time()
            current_start_time = start_time
            for form in formset:
                form.instance.start_time = current_start_time
                form.save()
                # set current_start_time for next iteration of this formset
                current_start_time = form.instance.end_time
            
            st = datetime.combine(date.today(), op_inst.steps.first().start_time)
            et = datetime.combine(date.today(), op_inst.steps.last().end_time)
            op_inst.elapsed_time = (et - st).seconds
            op_inst.complete = True
            op_inst.save()
            return redirect('timer:operation_instance_detail', operation_instance_id=operation_instance_id)
        else:
            print("formset is not valid -- ocs2") 
            # re-render with the data from the POST request
            # can't figure out how to do with django, so we write some javascript to do it from saved data
            # "09:43:44" should be what it looks like
            for index, data in enumerate(formset):
                saved_data[index] = data.cleaned_data['end_time'].strftime("%H:%M:%S") if 'end_time' in data.cleaned_data else None
            saved_data['start-time'] = formset.data['start-time']
            #import code
            #code.interact(local=locals())
    else:
        formset = StepInstanceFormSet(queryset=steps)

    context = {
        "formset" : formset,
        "operation_instance" : op_inst,
        "saved_data" : saved_data,
    }

    # figure out how to print a part of the formset queryset data in HTML

    return render(request, 'timer/add_templates/time_steps.html', context)

def TestView(request):

    context = {}
    single_form = StepForm()
    context['single_form'] = single_form
    StepFormSet = modelformset_factory(Step, form=StepForm, formset=CustomStepFormSet, extra=1)


    if request.method == "POST":
        step_formset = StepFormSet(request.POST)

        if step_formset.is_valid():
            print("step formset is valid")
            step_formset = StepFormSet(queryset=Step.objects.none())
        else:
            print("step formset is not valid-- testview")
        #code.interact(local=locals())
        # reset step formset
    
    else:
        step_formset = StepFormSet(queryset=Step.objects.none())

    context['step_formset'] = step_formset 
    return render(request, 'timer/test.html', context)




#####################
# class based views #
#####################
class DeleteSurgeonView(DeleteView):
    model = Surgeon
    success_url=reverse_lazy("timer:surgeons")
    template_name="timer/confirm_delete.html"

class DeleteOperationView(DeleteView):
    model = OperationType
    success_url=reverse_lazy("timer:operation_types")
    template_name="timer/confirm_delete.html"

# Update views
"""
class TimerUpdateView(UpdateView):
    model = TimerEntry
    fields = ['date', 'title', 'start_time', 'end_time', 'detail', 'surgeon', 'operation']
    #form_class = TimerEntryForm
    template_name = "timer/update_templates/update_form.html"
"""
class SurgeonUpdateView(UpdateView):
    model = Surgeon
    fields = ['first_name', 'last_name', 'email']
    #form_class = TimerEntryForm
    template_name = "timer/update_templates/update_form.html"

class OperationUpdateView(UpdateView):
    model = OperationType
    fields = ['operation_type', ]
    #form_class = TimerEntryForm
    template_name = "timer/update_templates/update_form.html"


def redirect_to_timer(request):
    return redirect("timer:index")


