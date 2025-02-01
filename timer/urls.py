from django.urls import path

from . import views
app_name = "timer"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),

    path("surgeons/", views.surgeons, name="surgeons"),
    path("surgeons/<int:surgeon_id>/", views.surgeon_entry_detail, name="surgeon_entry_detail"),
    path("operations/", views.operations, name="operations"),
    path("operations/<int:operation_id>/", views.operation_entry_detail, name="operation_entry_detail"),

    path("update/<int:pk>/", views.TimerUpdateView.as_view(), name="update_timer_entry"),


    # ex: /polls/5/
    path("timer_entry_detail/<int:question_id>/", views.timer_entry_detail, name="timer_entry_detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),

]