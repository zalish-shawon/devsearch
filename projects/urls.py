from django.urls import path
from . import views


urlpatterns = [
    path('project/<str:pk>', views.project, name="project"),
    path('', views.projects, name='projects'), 
    path('create-project', views.projectCreate, name="create-project"),
    path('update-project/<str:pk>/', views.UpdateProject, name='update-project'),
    path('delete-project/<str:pk>/', views.deleteProject, name='delete-project'),
    
]