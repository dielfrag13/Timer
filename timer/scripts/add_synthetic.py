import datetime
import timer.models


def run():
    print("adding synthetic data!")
    s1, _ = timer.models.SurgeonEntry.objects.get_or_create(first_name="Tom", last_name="Foolery", email="tom.foolery@lol.gov")
    s2, _ = timer.models.SurgeonEntry.objects.get_or_create(first_name="Darrin", last_name="Trask", email="dirtydog69@aol.com")


    o1, _ = timer.models.OperationEntry.objects.get_or_create(operation_type="Sixth Finger Augmentation")
    o2, _ = timer.models.OperationEntry.objects.get_or_create(operation_type="Synthetic Femur Upgrade")

    
    timer.models.TimerEntry.objects.all().delete()
    timer.models.TimerEntry.objects.get_or_create(
        title="Paul's First Sixth Finger", 
        operation=o1,
        date=datetime.date(2024, 12, 12),
        start_time=datetime.time(7, 30, 20),
        end_time=datetime.time(9, 12, 26),
        detail="Today we gave Paul a sixth finger on his right hand.",
        surgeon=s1,
    )

    timer.models.TimerEntry.objects.get_or_create(
        title="Paul's Second Sixth Finger", 
        operation=o1,
        date=datetime.date(2025, 1, 17),
        start_time=datetime.time(12, 16, 35),
        end_time=datetime.time(17, 12, 26),
        detail="Today we gave Paul a sixth finger on his left hand.",
        surgeon=s2,
    )

    timer.models.TimerEntry.objects.get_or_create(
        title="Paul's new SmartFemur", 
        operation=o2,
        date=datetime.date(2025, 1, 5),
        start_time=datetime.time(10, 00, 35),
        end_time=datetime.time(13, 12, 26),
        detail="Today we successfully replaced Paul's natural femur with our propritary new SmartFemur",
        surgeon=s1,
    )

    timer.models.TimerEntry.objects.get_or_create(
        title="Lisa's new SmartFemur", 
        operation=o2,
        date=datetime.date(2025, 1, 9),
        start_time=datetime.time(11, 16, 35),
        end_time=datetime.time(14, 12, 26),
        detail="Paul loved his SmartFemur so much that Lisa asked for one too!",
        surgeon=s2,
    )
