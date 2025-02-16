from django.urls import path

from . import views
app_name = "timer"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),

    path("surgeons/", views.surgeons, name="surgeons"),
    path("surgeons/<int:surgeon_id>/", views.surgeon_detail, name="surgeon_detail"),
    path("operations/", views.operations, name="operations"),
    path("operations/<int:operation_id>/", views.operation_type_detail, name="operation_type_detail"),

    
    path("operations/<int:operation_id>/", views.operation_type_detail, name="operation_type_detail"),

    # ocs1: operation creation step 1
    path("op/<int:operation_instance_id>/new_s1/", views.operation_creation_step_one, name="ocs1"),
    path("op/<int:operation_instance_id>/new_s2/", views.operation_creation_step_two, name="ocs2"),
    #path("updateTimer/<int:pk>/", views.TimerUpdateView.as_view(), name="update_timer_entry"),
    path("updateSurgeon/<int:pk>/", views.SurgeonUpdateView.as_view(), name="update_surgeon_entry"),
    path("updateOperation/<int:pk>/", views.OperationUpdateView.as_view(), name="update_operation_entry"),

    path("delete_surgeon/<int:pk>/", views.DeleteSurgeonView.as_view(), name="delete_surgeon"),
    #path("delete_timer/<int:pk>/", views.DeleteTimerView.as_view(), name="delete_timer"),
    path("delete_operation/<int:pk>/", views.DeleteOperationView.as_view(), name="delete_operation"),
    #path("deleteSuccess", views.Delete.as_view(), name="delete_timer"),
    #path("deleteSuccess", views.DeleteTimerView.as_view(), name="delete_timer"),

    # ex: /polls/5/
    #path("timer_entry_detail/<int:question_id>/", views.timer_entry_detail, name="timer_entry_detail"),
    # ex: /polls/5/results/
    #path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    #path("<int:question_id>/vote/", views.vote, name="vote"),

]