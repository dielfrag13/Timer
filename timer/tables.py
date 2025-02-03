import django_tables2 as tables
from .models import Surgeon, OperationType

class OperationTypeTable(tables.Table):
    operation_type = tables.LinkColumn('timer:operation_type_detail', args=[tables.A('pk')])
    class Meta:
        model = OperationType
        fields = ('operation_type', 'surgery_count')
        attrs = {'class': 'table table-striped table-hover'}


class SurgeonTableMinimal(tables.Table):
    #full_name = tables.LinkColumn('timer:surgeon_entry_detail', args=[tables.A('pk')])
    class Meta:
        model = Surgeon
        fields = ('full_name', 'email')
        attrs = {'class': 'table table-striped table-hover'}


class SurgeonTable(tables.Table):
    first_name = tables.LinkColumn('timer:surgeon_detail', args=[tables.A('pk')])
    class Meta:
        model = Surgeon
        fields = ('first_name', 'last_name', 'email', 'surgery_count')
        attrs = {'class': 'table table-striped table-hover'}

"""
class TimerEntryTable(tables.Table):
    # per the django table docs, you can do render_foo method for a 'foo' column
    # https://django-tables2.readthedocs.io/en/latest/pages/custom-data.html#table-render-foo-methods
    # so we can render_elapsed_time and convert from seconds to a prettier format
    # HH:MM:SS

    def render_start_time(self, value):
        return value.strftime("%I:%M %p")

    def render_end_time(self, value):
        return value.strftime("%I:%M %p")

    def render_elapsed_time(self, value):
        return f"{value//3600:02}:{(value%3600)//3600:02}:{value%60:02}"

    def render_dist_from_average(self, value, column):
        if value[0] == "-":
            # green
            column.attrs = {'td' : {'class' : 'text-success'}}
            return value[1:] + " lower than average"
        else:
            column.attrs = {'td' : {'class' : 'text-danger'}}
            return value + " higher than average"

    # this has to be paired up with how the view is coded
    title = tables.LinkColumn('timer:timer_entry_detail', args=[tables.A('pk')])
    operation = tables.LinkColumn('timer:operation_entry_detail', args=[tables.A('operation__pk')])
    surgeon = tables.LinkColumn('timer:surgeon_entry_detail', args=[tables.A('surgeon__pk')])
    class Meta:
        model = TimerEntry
        fields = ('title', 'operation', 'surgeon', 'start_time', 'end_time', 'elapsed_time', 'dist_from_average')
        attrs = {'class': 'table table-striped table-hover'}

"""