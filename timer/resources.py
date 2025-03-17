from timer.models import *
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

class OperationInstanceResource(resources.ModelResource):

    def __init__(self, step_instances=None):
        super().__init__()
        self.dynamic_fields = {}

        # dynamically add fields from the Step list
        step_names = step_instances.values_list("title", flat=True).distinct()
        for step_name in step_names:
            self.dynamic_fields[step_name] = fields.Field(column_name=step_name)
            setattr(self, f"dehydrate_{step_name}", self.make_dehydrate_method(step_name))

        # Add fields to resource
        self.fields.update(self.dynamic_fields)


    operation_type = fields.Field(
        column_name = "Operation",
        attribute = "operation_type",
        widget = ForeignKeyWidget(OperationType, field="operation_type"),
    )

    surgeon = fields.Field(
        column_name = "Surgeon",
        attribute = "surgeon",
        widget = ForeignKeyWidget(Surgeon, field="full_name"),
    )

    def dehydrate_elapsed_time(self, value):
        value = value.elapsed_time
        return f"{value//3600:02}:{(value%3600)//60:02}:{value%60:02}"

    def make_dehydrate_method(self, step_name):
        """dynamically creates a method for retrieving the time for a given step."""
        def dehydrate_method(obj):
            step = obj.steps.get(step__title=step_name)
            value = step.elapsed_time
            return f"{value//3600:02}:{(value%3600)//60:02}:{value%60:02}"
        return dehydrate_method
    

    class Meta:
        model = OperationInstance
        fields = (
            "operation_type", #fk
            "date",
            # "detail",
            "surgeon", #fk
            "elapsed_time",
        )
    """
    def get_export_fields(self, operation):
        # Ensures both static and dynamic fields are included in the export.
        print("what's the parameter passed?")
        import code
        code.interact(local=locals())
        return list(super().get_export_fields()) + list(self.dynamic_fields.values())
    """


class StepInstanceResource(resources.ModelResource):

    step = fields.Field(
        column_name="step",
        attribute = "step",
        widget = ForeignKeyWidget(Step, field="title")
    )

    class Meta:
        model = StepInstance
        fields = (
            "step", # fk
            "start_time", 
            "end_time", 
            "elapsed_time",
            "dist_from_average",
        )

