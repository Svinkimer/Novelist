from django.db import models
from login.models import User

# usr.stories - reverse for all Stories of user
class my_User(models.Model):
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=400, unique=True, blank=False, null=False)
    password = models.CharField(max_length=400, blank=False, null=False)
    img = models.ImageField(upload_to='user_icon/', default='/user_icon/default.jpg')
    balance = models.IntegerField(default=0)

    def __str__(self):  
        return f"{self.nickname} (ID {self.id})"

# 
class Story(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, default='Your title')
    description = models.CharField(max_length=600, default="Here you can add description")
    owner = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, related_name="stories")
    img = models.ImageField(upload_to='poster/', default='poster/default.jpg')
    start = models.ForeignKey('Scene', on_delete=models.SET_NULL, default=None, null=True, related_name='story_to_begin')

    def __str__(self):
        return f"Project: {self.title}"

class Location(models.Model):
    id = models.BigAutoField(primary_key=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True, default=None, related_name="locations")
    title = models.CharField(max_length=100, default='Untitled')
    img = models.ImageField(upload_to='background/', default="background/default.jpeg")

    def __str__(self):
        return f"{self.title} (ID {self.id})"

class Scene(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True, default='Untitled' )
    story = models.ForeignKey(Story, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='scenes')
    location = models.ForeignKey(Location, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='scenes')
    description = models.CharField(max_length=400)
    previous = models.ForeignKey('self', null=True, default=None, on_delete=models.PROTECT)
    choice_option_name = models.CharField(max_length=70, default='no_choice')

    def __str__(self):
        return f"Scene: {self.title} (ID {self.id})"

class Hero(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=False, null=False)
    description = models.CharField(max_length=400)
    color = models.CharField(max_length=7, default='#FFFFFF')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='heroes')

    def __str__(self):
        return f"{self.name} (ID {self.id})"

class State(models.Model):
    id = models.BigAutoField(primary_key=True)
    hero = models.ForeignKey(Hero, blank=False, null=False, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=20)
    img = models.ImageField(upload_to='state/', default='state/default.jpg')

    def __str__(self):
        return f"{self.name} (ID {self.id})"

class SceneEvent(models.Model):
    TYPE_CHOICE = [
        ('R', 'Replic'),
        ('A', 'Arrival/Leave'),
        ('T', 'Show Title'),
    ]

    id = models.BigAutoField(primary_key=True)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='events')
    previous = models.ForeignKey('self', default=None, on_delete=models.CASCADE, related_name='next_event', null=True)
    next = models.ForeignKey('self', default=None, on_delete=models.CASCADE, related_name='previous_event', null=True)
    type = models.CharField(max_length=1, default='R', choices=TYPE_CHOICE, blank=True)

    def __str__(self):
        return f"ID {self.id}"
        if self.type == 'R':
            obj = Replic.objects.get(event=self)
            if obj:
                return obj
        if self.type == 'A':
            obj = Replic.objects.get(event=self)
            if obj:
                return obj
        if self.type == 'T':
            obj = Replic.objects.get(event=self)
            if obj:
                return obj
            else: return "Trouble with finding replic"

class Replic(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(SceneEvent, null=True, on_delete=models.CASCADE, related_name='replic')
    hero_state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True, related_name="replics")
    text = models.CharField(max_length=400)

    def __str__(self):
        return f"Related to: {self.event.id}: {self.text}"

    def __str__(self):
        return self.text

class ArrivalLeave(models.Model):
    CHOICES = [
        ('A', 'Arrival'),
        ('L', 'Leave')
    ]
    event = models.ForeignKey(SceneEvent, on_delete=models.CASCADE, null=True, related_name="arrival")
    type = models.CharField(max_length=1, choices=CHOICES, default="A")
    hero_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name="arrivals")
    img = models.ImageField(upload_to='arrival/', default='arrival/default.jpeg')

    def __str__(self):
        return "A hero Appeared!"

class ShowTitle(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(SceneEvent, on_delete=models.CASCADE, null=True, related_name="title")
    text = models.CharField(max_length=500, default=None, null=True, blank=True,)
    img = models.ImageField(upload_to='title_background/')

    def __str__(self):
        return f"Title: {self.text}"