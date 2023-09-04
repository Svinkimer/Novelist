from django.urls import path
from . import views

urlpatterns = [
    path('scene/<int:scene_event_id>', views.draw_scene_event)
]