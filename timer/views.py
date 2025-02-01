from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.views.generic.edit import UpdateView
# Create your views here.
from .models import TimerEntry, SurgeonEntry, OperationEntry
from .forms import TimerEntryForm, SurgeonEntryForm, OperationEntryForm
from .tables import TimerEntryTable, SurgeonEntryTable, OperationEntryTable, SurgeonEntryTableMinimal



def index(request):

    latest_timer_list = TimerEntry.objects.all().order_by('-pk')[:5]
    surgeon_list = SurgeonEntry.objects.all().order_by('-pk')[:5]
    operation_list = OperationEntry.objects.all()

    if request.method == "POST":
        # determine which entry form was clicked
        isBool = True 
        for fieldName in TimerEntryForm().fields.keys():
             if fieldName not in request.POST:
                 isBool = False
                 break
        if isBool:
            timerEntryForm = TimerEntryForm(request.POST)
        else:
            timerEntryForm = TimerEntryForm()
        

        # do the same as above for surgeon and operation
        surgeonEntryForm = SurgeonEntryForm(request.POST)
        operationEntryForm = OperationEntryForm(request.POST)
        if timerEntryForm.is_valid():
            newTimerEntry = timerEntryForm.save()
            return redirect('timer:timer_entry_detail', question_id=newTimerEntry.id)
        elif surgeonEntryForm.is_valid() and operationEntryForm.is_valid():
            newSurgeonEntry = surgeonEntryForm.save()
            newOperationEntry = operationEntryForm.save()
            return redirect('timer:index')
        elif operationEntryForm.is_valid():
            newOperationEntry = operationEntryForm.save()
            return redirect('timer:index')
        elif surgeonEntryForm.is_valid():
            newSurgeonEntry = surgeonEntryForm.save()
            return redirect('timer:index')
    else:
        timerEntryForm = TimerEntryForm()
        surgeonEntryForm = SurgeonEntryForm()
        operationEntryForm = OperationEntryForm()

    context = {
        "latest_time_list": latest_timer_list,
        "surgeon_list" : surgeon_list,
        "operation_list" : operation_list,
        "timerEntryForm" : timerEntryForm,
        "surgeonEntryForm" : surgeonEntryForm,
        "operationEntryForm" : operationEntryForm,
        "timerEntryTable" : TimerEntryTable(latest_timer_list),
        "surgeonEntryTableMinimal" : SurgeonEntryTableMinimal(surgeon_list),
    }

    return render(request, "timer/index.html", context)





def surgeons(request):
    surgeon_list = SurgeonEntry.objects.all()

    if request.method == "POST":
        surgeonEntryForm = SurgeonEntryForm(request.POST)
        if surgeonEntryForm.is_valid():
            newSurgeonEntry = surgeonEntryForm.save()
            return redirect('timer:surgeon_entry_detail', surgeon_id=newSurgeonEntry.id)
    else:
        surgeonEntryForm = SurgeonEntryForm()


    context = {
        "surgeon_list" : surgeon_list,
        "surgeonEntryForm" : surgeonEntryForm,
        "surgeonEntryTable" : SurgeonEntryTable(surgeon_list)
    }
    return render(request, "timer/surgeons.html", context)





def surgeon_entry_detail(request, surgeon_id):
    thing = get_object_or_404(SurgeonEntry, pk=surgeon_id)
    if request.method == "POST":
        surgeonEntryForm = SurgeonEntryForm(request.POST)
        if surgeonEntryForm.is_valid():
            newSurgeonEntry = surgeonEntryForm.save()
            return redirect('timer:surgeon_detail', surgeon_id=newSurgeonEntry.id)
    else:
        surgeonEntryForm = SurgeonEntryForm()
    
    qs = TimerEntry.objects.filter(surgeon__id=surgeon_id)
    if qs:
        qs_nums = qs.values_list("elapsed_time", flat=True)
        avg = sum(qs_nums) / len(qs_nums)
        for entry in qs:
            percentage_str = f"{(((entry.elapsed_time - avg) / avg)*100):.2f}%"
            entry.dist_from_average = percentage_str

    context = {
        "surgeonEntry" : thing, 
        "surgeonEntryForm" : surgeonEntryForm,
        "surgeonTimerEntries" : TimerEntry.objects.filter(surgeon__id=surgeon_id),
        "timerEntryTable" : TimerEntryTable(qs)
    }

    return render(request, "timer/entry_details/surgeon_entry_detail.html", context)



def operations(request):
    operation_list = OperationEntry.objects.all()
    if request.method == "POST":
        operationEntryForm = OperationEntryForm(request.POST)
        if operationEntryForm.is_valid():
            newOperationEntry = operationEntryForm.save()
            return redirect('timer:operation_detail', surgeon_id=newOperationEntry.id)
    else:
        operationEntryForm = OperationEntryForm()
    
    operationEntryTable = OperationEntryTable(operation_list)
    context = {
        "operation_list" : operation_list,
        "operationEntryForm" : operationEntryForm,
        "operationEntryTable" :  operationEntryTable   }
    return render(request, "timer/operations.html", context)

def operation_entry_detail(request, operation_id):
    thing = get_object_or_404(OperationEntry, pk=operation_id)

    if request.method == "POST":
        operationEntryForm = OperationEntryForm(request.POST)
        if operationEntryForm.is_valid():
            newOperationEntry = operationEntryForm.save()
            return redirect('timer:operation_detail', operation_id=newOperationEntry.id)
    else:
        operationEntryForm = OperationEntryForm()


    qs = TimerEntry.objects.filter(operation__id=operation_id)
    if qs:
        qs_nums = qs.values_list("elapsed_time", flat=True)
        avg = sum(qs_nums) / len(qs_nums)
        for entry in qs:
            percentage_str = f"{(((entry.elapsed_time - avg) / avg)*100):.2f}%"
            entry.dist_from_average = percentage_str
    

    context = {
        "operationEntry" : thing, 
        "operationEntryForm" : operationEntryForm,
        "operationTimerEntries" : TimerEntry.objects.filter(operation__id=operation_id),
        "timerEntryTable" : TimerEntryTable(qs)
    }

    return render(request, "timer/entry_details/operation_entry_detail.html", context)

def timer_entry_detail(request, question_id):
    # the key in the dictionary is the variable name of what's in the HTML
    # return render(request, "timer/detail.html", {"TimerEntry" : thing})

    thing = get_object_or_404(TimerEntry, pk=question_id)

    if request.method == "POST":
        timerEntryForm = TimerEntryForm(request.POST)
        if timerEntryForm.is_valid():
            newTimerEntry = timerEntryForm.save()
            return redirect('timer:timer_entry_detail', question_id=newTimerEntry.id)
    else:
        timerEntryForm = TimerEntryForm()
    context = {
        "TimerEntry": thing, 
        "timerEntryForm" : timerEntryForm,
        "timerEntryTable" : TimerEntryTable(TimerEntry.objects.filter(pk=thing.pk))
        }
    return render(request, "timer/entry_details/timer_entry_detail.html", context)

class TimerUpdateView(UpdateView):
    model = TimerEntry
    fields = ['date', 'title', 'start_time', 'end_time', 'detail', 'surgeon', 'operation']
    #form_class = TimerEntryForm
    template_name = "timer/update_templates/TimerEntry_update_form.html"

def redirect_to_timer(request):
    return redirect("timer:index")

def results(request, question_id):
    return HttpResponse("results -- you're looking at whatever %s is." % question_id)

def vote(request, question_id):
    return HttpResponse("vote -- you're looking at whatever %s is." % question_id)



# helper methods