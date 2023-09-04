from django import forms
from editor.models import *

class SignInForm(forms.Form):
    nickname = forms.CharField(max_length=400)
    password = forms.CharField(max_length=400)


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'description', 'img']

class SceneForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = ['title', 'description', 'choice_option_name', 'location']
    
    # location = forms.ModelChoiceField(queryset=None, empty_label="No location selected")
    
    def __init__(self, story_id, *args, **kwargs):
        super(SceneForm, self).__init__(*args, **kwargs)
        queryset = Location.objects.filter(story=Story.objects.get(id=story_id))
        if len(queryset) == 0:
            new_location = Location(story=Story.objects.get(id=story_id))
            new_location.save()
            queryset = Location.objects.filter(story=Story.objects.get(id=story_id))
        self.fields['location'].queryset = queryset
            


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['name', 'description', 'color']

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name', 'img']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['title', 'img']




class ReplicForm(forms.ModelForm):
    hero = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Replic
        fields = ['hero_state', 'text']

    def __init__(self, story_id, *args, **kwargs):
        super(ReplicForm, self).__init__(*args, **kwargs)
        self.fields['hero'].queryset = Hero.objects.filter(story=Story.objects.get(id=story_id))
        self.fields['hero_state'].queryset = State.objects.filter(hero__in=self.fields['hero'].queryset)



class ArrivalLeaveForm(forms.ModelForm):
    hero = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = ArrivalLeave
        fields = ['hero_state', 'img']

    def __init__(self, story_id, *args, **kwargs):
        super(ArrivalLeaveForm, self).__init__(*args, **kwargs)
        self.fields['hero'].queryset = Hero.objects.filter(story=Story.objects.get(id=story_id))
        self.fields['hero_state'].queryset = State.objects.filter(hero__in=self.fields['hero'].queryset)

    
    

class ShowTitleForm(forms.ModelForm):
    class Meta:
        model = ShowTitle
        fields = ['text', 'img']

    def __init__(self, story_id, *args, **kwargs):
        super(ShowTitleForm, self).__init__(*args, **kwargs)


