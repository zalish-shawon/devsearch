from django.db import models
from users.models import Profile
import uuid

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=20)
    description = models.TextField(null = True, blank = True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg") 
    demo_link = models.CharField(max_length = 2000, null = True, blank = True)
    source_link = models.CharField(max_length = 2000, null = True, blank = True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank= True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key= True,  editable= False)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['created']

class Review(models.Model):
    vote_type = (
        ('up', 'Up vote'),
        ('down', 'Down vote')
    )
    #owner =
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=vote_type)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    def __str__(self) -> str:
        return self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique= True, primary_key= True, editable=False)


    def __str__(self) -> str:
        return self.name
