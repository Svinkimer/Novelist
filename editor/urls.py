from django.urls import path
from . import views

from .view_story import EditStoryView
from .view_hero import EditHeroView
from .view_location import EditLocationView
from .view_scene import EditSceneView

app_name='editor'

urlpatterns = [
    path("", views.EditorIndexView.as_view(), name='editor index'),
    path("character/", EditHeroView.as_view(), name='edit hero'),
    path("edit_project/", EditStoryView.as_view(), name="edit story"),
    path("edit_scene/", EditSceneView.as_view(), name='edit scene'),
    path("edit_location/", EditLocationView.as_view(), name='edit location'),
    path('register/', views.CreateAccountView.as_view(), name='create account'),
    path("story/", views.story_editor), 
    path("project_manager/", views.project_manager, name='project_manager'),
    path("nums/<int:number_param>/", views.nums),
    path("forms/", views.forms),
]