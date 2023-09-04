from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import *
from .forms import *

class EditHeroView(View):
    template_data = {
        'hero_obj': None,
        'hero_form': None,
        'state_form': None,
        'states': None,
        'edited_id': None,
        'errors': None
    }


    # здесь происходит ТОЛЬКО отрисовка изображения

    def get(self, request):
        info = self.get_info(request)
        
        # получить объект hero
        if info['new']:
            hero = Hero(name='Anonimous', story=info['story'])
            hero.save()
        else:
            hero = Hero.objects.get(id=info['id'])

        self.template_data['hero_form'] = HeroForm(instance=hero)
        self.template_data['hero_obj'] = hero
        self.template_data['states'] = State.objects.filter(hero=hero)  # hero.states.all()

        
        if info['new_state']:
            print("New_state")
            temp_name = f"{hero.name}_idle"
            state = State(hero=hero, name=temp_name)
            state.save()
            self.template_data['edited_id'] = state.id

        elif info['state_id']:
            self.template_data['edited_id'] = info['state_id']
            state = State.objects.get(id=info['state_id'])
            self.template_data['state_form'] = StateForm(instance=state)

        return render(request, 'editor/character_editor.html', self.template_data)



    # здесь происходит ТОЛЬКО запись в базу данных
    # и redirect в get для отрисовки
    def post(self, request):
        info = self.post_info(request)
        
        hero = Hero.objects.get(id=info['id'])
        self.template_data['hero_form'] = HeroForm(data=request.POST, instance=hero)

        if self.template_data['hero_form'].is_valid():
            print("OK!")
            self.template_data['hero_form'].save()
        else:
            
            pass #raise Exception
        
        if info['state_id']:
            state = State.objects.get(id=info['state_id'])
            state_form = StateForm(request.POST, request.FILES, instance=state)
            if state_form.is_valid():
                state_form.save()
            else:
                errors = state_form.errors.as_data
                print(errors)
                
        
        return redirect(reverse('editor:edit hero') + f"?id={info['id']}&state_id={info['state_id']}")


    def get_info(self, request):
        info = {
            "new": request.GET.get('new', None),
            "story": Story.objects.get(id=int(request.session['current_story'])),
            "id": int(request.GET.get('id', False)),
            "new_state": request.GET.get('new_state', None),
            "state_id": int(request.GET.get('state_id', False)), 
            }
        return info

    def post_info(self, request):
        info = {
            "new": request.POST.get('new', None),
            "story": Story.objects.get(id=int(request.session['current_story'])),
            "id": int(request.POST.get('id', False)),
            "state_id": int(request.GET.get('state_id', False)), 
        }
        return info