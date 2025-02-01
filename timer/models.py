from django.db import models
from django.urls import reverse
import datetime

# Create your models here.
class SurgeonEntry(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    @property
    def surgery_count(self):
        return TimerEntry.objects.filter(surgeon__pk=self.pk).count()

    # for minimal table
    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class OperationEntry(models.Model):
    operation_type = models.CharField(max_length=100)

    @property
    def surgery_count(self):
        return TimerEntry.objects.filter(operation__pk=self.pk).count()



    def __str__(self):
        return "{}".format(self.operation_type)


class TimerEntry(models.Model):

    # 50 characters to title this entry
    title = models.CharField(max_length=50)

    # Operation type
    operation = models.ForeignKey(OperationEntry, on_delete=models.CASCADE)

    date = models.DateField()
    # time started and ended
    start_time = models.TimeField("time started")
    end_time = models.TimeField("time ended")

    # 500 characters to describe what was done in this entry
    detail = models.TextField(max_length=500)

    # who did this
    surgeon = models.ForeignKey(SurgeonEntry, on_delete=models.CASCADE)

    # calculated by the view based on other relative timer entries
    #from_average = models.CharField()

    elapsed_time = models.IntegerField(null=True, default=None)


    def save(self, *args, **kwargs):
        if not self.elapsed_time:
            st = datetime.datetime.combine(datetime.date.today(), self.start_time)
            et = datetime.datetime.combine(datetime.date.today(), self.end_time)
            self.elapsed_time = (et - st).seconds
        super().save(*args, **kwargs)
    
    dist_from_average = models.CharField(max_length=50)

    # used in the update class-based view to redirect on success
    def get_absolute_url(self):
        return reverse('timer:timer_entry_detail', args=(self.pk,))

    #def __str__(self):
    #    return self.title


