from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from .models import *
from .forms import *



class EditLocationView(View):
    context = {
        "location": None
    }

    def get(self, request):
        info = self.get_info(request)

        if info['new']:
            location = Location(story=info["story"])
            location.save()
        else:
            location = Location.objects.get(id=int(info['location_id']))

        self.context['location_form'] = LocationForm(instance=location)
        self.context['location'] = location

        return render(request, "editor/location_editor.html", self.context)


    def post(self, request):
        info = self.post_info(request)

        location = Location.objects.get(id=info["location_id"])
        location_form = LocationForm(request.POST, request.FILES, instance=location)
        if location_form.is_valid():
            location_form.save()
            print("saved!")
            return redirect(reverse("editor:edit location") + f"?location_id={location.id}")
        else:
            return HttpResponse("<h1>Validation failed</h1>")


    def get_info(self, request):
        return {
            "new": request.GET.get("new", None),
            "story": Story.objects.get(id=int(request.session["current_story"])),
            "location_id": request.GET.get("location_id", None),
            "story": None, 
        }


    def post_info(self, request):
        return {
            "location_id": int(request.POST.get("location_id", None)),

        }
