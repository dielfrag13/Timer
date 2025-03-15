from timer.models import *
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

class OperationInstanceResource(resources.ModelResource):

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

    class Meta:
        model = OperationInstance
        fields = (
            "operation_type", #fk
            "date",
            "detail",
            "surgeon", #fk
            "elapsed_time",
        )

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

