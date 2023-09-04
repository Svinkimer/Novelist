from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import *
from .forms import *


# связать форму с моделью (ивент), заполнение через instance

class EditSceneView(View):

    def set_ordered_events(self, request, info):
        start_event = SceneEvent.objects.filter( scene=info['id'] ).get(previous=None)
        ordered_events = []

        event = start_event
        while event.next != None:
            ordered_events.append(event)
            event = event.next
        
        self.template_data["events"] = ordered_events
        return ordered_events



    template_data = {
        "form": None,
        "scene": None,
        "events": None,
        "edited_id": None,
        "event": None,
        "event_form": None
    }


    def get_info(self, request):
        return {
            "id": int(request.GET.get('id', 0)),                 # id of current scene
            "new": request.GET.get('new', None),               # was this scene just created?
            "event_id": int(request.GET.get('event_id', 0)),     # id of processed event (which is replaced with form)
            "story_id": request.session.get('current_story', 0)
        }

    def post_info(self, request):
        return {
            "id": request.POST.get('id', 0),                 # id of current scene
            "new": request.POST.get('new', 0),               # was this scene just created?
            "event_id": request.POST.get('event_id', 0),     # id of processed event (which is replaced with form)
            "story_id": request.session.get('current_story', 0),
            "action": request.POST.get("action", None),              # изменить сцену / создать ивент / изменить ивент
            "title": request.POST.get("title", None),
            "description": request.POST.get('description', None),
            "img": request.POST.get('img', None),
            "choice_option_name": request.POST.get('choice_option_name', None),
            "type":  request.POST.get('type', None),
        }
    


    ### GET ###

    def get(self, request):

        info = self.get_info(request)        

        # Если создаем новую сцену
        if info['new']=='true':
            scene = Scene( story=Story.objects.get(id=info['story_id']) )
            scene.save()
            start_event = SceneEvent(scene=scene, previous=None, next=None)
            start_event.save()
            info['id'] = scene.id   
            scene.save()
        

        # Если запрос на редактирование какого-то ивента

        else:
            scene = Scene.objects.get(id=info['id'])
            if info['event_id']:
                self.template_data['edited_id'] = info['event_id']
                edited_event = SceneEvent.objects.get(id=info['event_id'])

                switch_event = {
                    'R': ReplicForm,
                    'A': ArrivalLeaveForm,
                    'T': ShowTitleForm,
                }

                if edited_event.type == 'R':
                    event_form = ReplicForm(instance=edited_event.replic.all().first(), story_id=info['story_id'])
                elif edited_event.type == 'A':
                    event_form = ArrivalLeaveForm(instance=edited_event.arrival.all().first(), story_id=info['story_id'])
                elif edited_event.type == 'T':
                    event_form = ShowTitleForm(instance=edited_event.title.all().first(), story_id=info['story_id'])

                self.template_data['event_form'] = event_form
                self.template_data['form'] = SceneForm(story_id=info['story_id'], instance=scene)


            
        self.template_data['scene'] = scene
        self.set_ordered_events(request, info)
        return render(request, 'editor/scene_editor.html', self.template_data)


    ### POST ###

    ## отрисовка происходит в GET (POST только обновляет сведения и возвращает redirect)
    def post(self, request):
        info = self.post_info(request)
        scene = Scene.objects.get(id=info['id'])
        start_event = scene.events.get(previous=None)


        if info["action"] == "edit_scene":
            initial_scene_form = request.POST
            self.template_data['form'] = SceneForm(instance=scene, data=request.POST, story_id=info['story_id'])
            self.template_data['form'].save()
            scene.title = info['title']
            scene.description = info['description']
            scene.img = info['img']
            scene.choice_option_name = info['choice_option_name']
        

        # заполнить пустой шаблон ивента
        # (прикрепить реплику / титры)

        elif info["action"] == "add_event":
            print(f"Add Event. Type={info['type']}")
            empty_event = SceneEvent.objects.filter(scene=scene).get(next=None)
            empty_event.type = info['type']
            empty_event.save()

            info['event_id'] = empty_event.id

            event_subclass = {
                'R': Replic,
                'A': ArrivalLeave,
                'T': ShowTitle,
            }

            event_subclass = event_subclass[info['type']](event=empty_event)
            event_subclass.save()


            # Создать новый пустой шаблон ивента,
            # обоюдно связать с предыдущим

            last_filled = empty_event
            empty_event = SceneEvent(scene=Scene.objects.get(id=info['id']), previous=last_filled, next=None)

            empty_event.save()
            last_filled.next = empty_event
            last_filled.save()
            
            info['action'] = 'edit_event'


        elif info['action'] == "edit_event":
            switch_event = {
                'R': (ReplicForm, Replic),
                'A': (ArrivalLeaveForm, ArrivalLeave),
                'T': (ShowTitleForm, ShowTitle)
            }

            edited_event = scene.events.get(id=info['event_id'])
            event_class = switch_event[edited_event.type][1]
            instance = event_class.objects.get(event=edited_event)

            print(f"Edited event: {edited_event}")
            self.template_data['event_form'] = switch_event[edited_event.type][0](story_id=request.session['current_story'], instance=instance, data=request.POST)
            self.template_data['event_form'].save()       

        return redirect(reverse("editor:edit scene") + f"?id={info['id']}")