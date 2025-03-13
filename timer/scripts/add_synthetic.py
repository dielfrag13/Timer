import datetime
from timer.models import *
import random



def run():
    print("adding synthetic data!")
    s1, _ = Surgeon.objects.get_or_create(first_name="Tom", last_name="Foolery", email="tom.foolery@lol.gov")
    s2, _ = Surgeon.objects.get_or_create(first_name="Darrin", last_name="Trask", email="dirtydog69@aol.com")
    s3, _ = Surgeon.objects.get_or_create(first_name="Katty", last_name="Wampus", email="inconsistent@gmail.xyz")

    o1, _ = OperationType.objects.get_or_create(operation_type="Sixth Finger Augmentation")
    o2, _ = OperationType.objects.get_or_create(operation_type="Synthetic Femur Upgrade")
    o3, _ = OperationType.objects.get_or_create(operation_type="Total Knee")

    # create steps
    step_list = ["in-room", "block done", "tubed", "prepped/draped", "time-out", "incision", "parts in", "closure end", "out of room"]
    for s in step_list:
        Step.objects.get_or_create(title=s)
    
    OperationInstance.objects.all().delete()
    print("created steps!")
    import code
    code.interact(local=locals())
    oi1 = OperationInstance(
        operation_type=o3,
        date=datetime.date(2025, 3, 13),
        detail="Today we gave Paul a fresh robo knee",
        surgeon=s2,
        ocs1 = True,
        complete = True,
    )
    oi1.save()
    # add timed steps where each step takes a random amount of time between 20 and 60 minutes 
    start_time = datetime.datetime(2025, 3, 13, 7, 30, 20)
    end_time = start_time + datetime.timedelta(minutes=random.randint(20, 60))

    print("created operation instance")
    import code
    code.interact(local=locals())
    for i, s in enumerate(step_list):
        si = StepInstance(
            step=Step.objects.get(title=s),
            operation_instance=oi1,
            order=i+1,
            start_time = start_time.time(),
            end_time = end_time.time(),
        )
        si.save()
        start_time = end_time
        end_time += datetime.timedelta(minutes=random.randint(20,60))

    oi1.save()        
    """
    start_time=datetime.time(7, 30, 20),
    end_time=datetime.time(9, 12, 26),
    OperationInstance.objects.get_or_create(
        title="Paul's Second Sixth Finger", 
        operation=o1,
        date=datetime.date(2025, 1, 17),
        start_time=datetime.time(12, 16, 35),
        end_time=datetime.time(17, 12, 26),
        detail="Today we gave Paul a sixth finger on his left hand.",
        surgeon=s2,
    )

    OperationInstance.objects.get_or_create(
        title="Paul's new SmartFemur", 
        operation=o2,
        date=datetime.date(2025, 1, 5),
        start_time=datetime.time(10, 00, 35),
        end_time=datetime.time(13, 12, 26),
        detail="Today we successfully replaced Paul's natural femur with our propritary new SmartFemur",
        surgeon=s1,
    )

    OperationInstance.objects.get_or_create(
        title="Lisa's new SmartFemur", 
        operation=o2,
        date=datetime.date(2025, 1, 9),
        start_time=datetime.time(11, 16, 35),
        end_time=datetime.time(14, 12, 26),
        detail="Paul loved his SmartFemur so much that Lisa asked for one too!",
        surgeon=s2,
    )

    """