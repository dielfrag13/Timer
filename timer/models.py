from django.db import models
from django.urls import reverse
import datetime

# Create your models here.
class Surgeon(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    @property
    def operation_count(self):
        return OperationInstance.objects.filter(surgeon=self, complete=True).count()

    # for minimal table
    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    # used in the update class-based view to redirect on success
    def get_absolute_url(self):
        return reverse('timer:surgeon_entry_detail', args=(self.pk,))
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)



class OperationType(models.Model):
    """Represents a type of operation (e.g. Sixth finger augmentation, SmartFemur replacement)"""
    operation_type = models.CharField(max_length=100)

    @property
    def operation_count(self):
        return OperationInstance.objects.filter(operation_type=self, complete=True).count()

    # used in the update class-based view to redirect on success
    def get_absolute_url(self):
        return reverse('timer:operation_entry_detail', args=(self.pk,))

    def __str__(self):
        return "{}".format(self.operation_type)



class OperationInstance(models.Model):
    """represents an instance of an operation."""

    # operation type 
    operation_type = models.ForeignKey(OperationType, on_delete=models.CASCADE)

    # date of this operation
    date = models.DateField()

    # 500 characters to describe what was done in this operation
    detail = models.TextField(max_length=500)

    # who did this
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)


    # status flags - to be true when mentioned
    ocs1 = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    elapsed_time = models.IntegerField(null=True, default=None)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.elapsed_time and self.steps.all() and self.steps.first().start_time and self.steps.last().end_time:
            st = datetime.datetime.combine(datetime.date.today(), self.steps.first().start_time)
            et = datetime.datetime.combine(datetime.date.today(), self.steps.last().end_time)
            self.elapsed_time = (et - st).seconds
        super().save(*args, **kwargs)

    def __str__(self):
        return self.operation_type.operation_type

class Step(models.Model):
    """
    Reusable model to indicate a step of an operation.
    Steps are unique by title (i.e. 'incision made'), 
      but may not be unique by operation (i.e. multiple operations involve making incisions).
    """

    # 50 characters to title this step
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    # 'instances' field comes from StepInstance 


class StepInstance(models.Model):
    """Each instance of a step is timed. These are the new Timer Entries"""

    # on_delete refers to what is to be done when the *referenced* model is deleted.
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="instances")
    operation_instance = models.ForeignKey(OperationInstance, on_delete=models.CASCADE, related_name="steps")

    # used to define the order of steps in this operation instance
    order = models.PositiveIntegerField()


    # time started and ended
    start_time = models.TimeField("time started", null=True, blank=True)
    end_time = models.TimeField("time ended", null=True, blank=True)

    # calculated by the view based on other relative timer entries
    #from_average = models.CharField()

    elapsed_time = models.IntegerField(null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.elapsed_time and self.start_time and self.end_time:
            st = datetime.datetime.combine(datetime.date.today(), self.start_time)
            et = datetime.datetime.combine(datetime.date.today(), self.end_time)
            self.elapsed_time = (et - st).seconds
        super().save(*args, **kwargs)
    
    dist_from_average = models.CharField(max_length=50)

    class Meta:
        ordering = ['order']


    # used in the update class-based view to redirect on success
    def get_absolute_url(self):
        return reverse('timer:timer_entry_detail', args=(self.pk,))

    def __str__(self):
        return self.step.title




