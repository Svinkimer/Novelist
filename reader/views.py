from django.shortcuts import render
from editor.models import Scene_Event, Replic
from django.http import HttpResponse

def reader_start_reading_project(request):
    return HttpResponse("<h1>Nothing here</h1>")

# Create your views here.
def draw_scene_event(request, scene_event_id):
    s_e = Scene_Event.objects.get(scene_event_id)
    if s_e.event_type == 'R':
        return HttpResponse(f"<h1>Its a replic with id={scene_event_id}</h1>")
    return HttpResponse(f"<h1>Its not a replic</h1>")

