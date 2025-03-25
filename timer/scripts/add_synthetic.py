import datetime
from timer.models import *
import random
import time

random.seed(time.time())

surgery_type_1 = "Sixth Finger Augmentation"
surgery_type_2 = "Total Knee"
surgery_type_3 = "Synthetic Femur Upgrade"


def new_knee(surgeon):
    print("creating new " + surgery_type_2)
    knee_step_list = ["block done", "tubed", "prepped/draped", "time-out", "incision", "parts in", "closure end", "out of room"]
    for s in knee_step_list:
        Step.objects.get_or_create(title=s)

    oi1 = OperationInstance(
        operation_type=OperationType.objects.get(operation_type=surgery_type_2),
        date=datetime.date(2025, 3, 13),
        detail="Today we gave Paul a fresh robo knee",
        surgeon=surgeon,
        ocs1 = True,
        complete = True,
    )
    oi1.save()
    # add timed steps where each step takes a random amount of time between 20 and 60 minutes 
    start_time = datetime.datetime(2025, 3, 13, 7, 30, 20)
    end_time = start_time + datetime.timedelta(minutes=random.randint(20, 60), seconds=random.randint(0, 59))

    for i, s in enumerate(knee_step_list):
        si = StepInstance(
            step=Step.objects.get(title=s),
            operation_instance=oi1,
            order=i+1,
            start_time = start_time.time(),
            end_time = end_time.time(),
        )
        si.save()
        start_time = end_time
        end_time += datetime.timedelta(minutes=random.randint(20,80), seconds=random.randint(0, 59))

    oi1.save()        

def new_femur(surgeon):
    print("creating new " + surgery_type_3)
    femur_step_list = ["patient hydrochloroformed", "beer shotgunned", "leg removed", "time-out", "new femur installed on leg", "leg re-appended", "closure end", "out of room"]
    for s in femur_step_list:
        Step.objects.get_or_create(title=s)

    oi1 = OperationInstance(
        operation_type=OperationType.objects.get(operation_type=surgery_type_3),
        date=datetime.date(2025, 3, 13),
        detail="Today we tested the experimental femur operation on Daniel Bubbaganoush",
        surgeon=surgeon,
        ocs1 = True,
        complete = True,
    )
    oi1.save()

    # add timed steps where each step takes a random amount of time between 20 and 60 minutes 
    start_time = datetime.datetime(2025, 3, 13, 7, 30, 20)
    end_time = start_time + datetime.timedelta(minutes=random.randint(20, 60), seconds=random.randint(0, 59))

    for i, s in enumerate(femur_step_list):
        si = StepInstance(
            step=Step.objects.get(title=s),
            operation_instance=oi1,
            order=i+1,
            start_time = start_time.time(),
            end_time = end_time.time(),
        )
        si.save()
        start_time = end_time
        end_time += datetime.timedelta(minutes=random.randint(20,80), seconds=random.randint(0, 59))

    oi1.save()        



def new_finger(surgeon):
    print("creating new " + surgery_type_1)
    finger_step_list = ["patient sedated", "finger identified", "beer shotgunned", "finger augmented", "qc approved", "closure end", "out of room"]
    for s in finger_step_list:
        Step.objects.get_or_create(title=s)

    oi1 = OperationInstance(
        operation_type=OperationType.objects.get(operation_type=surgery_type_1),
        date=datetime.date(2025, 3, 13),
        detail="You wouldn't believe how in-demand sixth fingers are these days",
        surgeon=surgeon,
        ocs1 = True,
        complete = True,
    )
    oi1.save()

    # add timed steps where each step takes a random amount of time between 20 and 60 minutes 
    start_time = datetime.datetime(2025, 3, 13, 7, 30, 20)
    end_time = start_time + datetime.timedelta(minutes=random.randint(20, 60), seconds=random.randint(0, 59))

    for i, s in enumerate(finger_step_list):
        si = StepInstance(
            step=Step.objects.get(title=s),
            operation_instance=oi1,
            order=i+1,
            start_time = start_time.time(),
            end_time = end_time.time(),
        )
        si.save()
        start_time = end_time
        end_time += datetime.timedelta(minutes=random.randint(20,80), seconds=random.randint(0, 59))

    oi1.save()        



def run():
    print("adding synthetic data!")

    surgeons = []
    operation_types = []
    surgeons.append(Surgeon.objects.get_or_create(first_name="Tom", last_name="Foolery", email="tom.foolery@lol.gov")[0])
    surgeons.append(Surgeon.objects.get_or_create(first_name="Darrin", last_name="Trask", email="dirtydog69@aol.com")[0])
    surgeons.append(Surgeon.objects.get_or_create(first_name="Katty", last_name="Wampus", email="inconsistent@gmail.xyz")[0])

    operation_types.append(OperationType.objects.get_or_create(operation_type=surgery_type_1)[0])
    operation_types.append(OperationType.objects.get_or_create(operation_type=surgery_type_3)[0])
    operation_types.append(OperationType.objects.get_or_create(operation_type=surgery_type_2)[0])

    # OperationInstance.objects.all().delete()

    for i in range(5):
        op = random.randint(0, 2)
        if op == 0:
            new_finger(surgeons[random.randint(0, 2)])
        elif op==1:
            new_knee(surgeons[random.randint(0, 2)])
        else:
            new_femur(surgeons[random.randint(0, 2)])
