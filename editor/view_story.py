from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .forms import *



# В get - получение всех данных, отрисовка
# В post - сохраненние инфы в БД

class EditStoryView(View):
    context = {
        'form': None,
        "story": None,
        'scenes': None,
        'heroes': None,
        'locations': None,
        }

    def get(self, request):
        info = self.get_info(request)
        print(info["id"])

        if info['new']:
            story = Story(owner=info['user'])
            story.save()

            first_scene = Scene(story=story, previous=None)
            first_scene.save()
            
            story.start = first_scene
            story.save()
        
        else:
            story = Story.objects.get(id=info["id"])

        print(story)

        # context fill
        self.context['story'] = story
        
        # Story form
        self.context['form'] = StoryForm(instance=story)
        # Heroes, Locations, Scenes
        self.context['heroes'] = story.heroes.all()
        self.context['locations'] = story.locations.all()
        self.context['scenes'] = story.scenes.all()
        # Locations
        # Scenes
        return render(request, "editor/edit_project.html", self.context) 

    
    def post(self, request):
        info = self.post_info(request)
        scene = story = Story.objects.get(id=info["id"])
        form = StoryForm(request.POST, request.FILES, instance=scene)
        if form.is_valid():
            form.save()

        return redirect(reverse("editor:edit story") + f"?story_id={info['id']}")
    
    def get_info(self, request):
        return {
            'new': request.GET.get('new', None),
            'user': User.objects.get(id=int(request.session.get('user_id', None))),
            'id': int(request.GET.get('story_id', None)),

        }
    

    def post_info(self, request):
        return {
            'id': int(request.POST.get('story_id', None)),
        }