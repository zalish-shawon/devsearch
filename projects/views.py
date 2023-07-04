from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Project, Tag
from .forms import projectForm


    #################### views data from database on our home page ####################

def projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains = search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) |
        Q(description__icontains = search_query) |
        Q(owner__name__icontains = search_query) |
        Q(tags__in = tags)
    )


    page = request.GET.get('page')
    results = 6
    paginator = Paginator(projects, results)

    try:
      projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    custom_range = range(leftIndex, rightIndex)
    context = {'projects': projects, 'search_query': search_query, 'paginator': paginator, 'custom_range': custom_range }
    return render(request, 'projects/projects.html', context)


     ########################## read a single create data #######################################

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    return render(request, 'projects/single-project.html', {'project': projectObj, 'tags': tags})


    ############################# Create OPERATIONS ##############################################
@login_required(login_url='login')

def projectCreate(request):
    profile = request.user.profile
    form = projectForm()

    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES)
        if form.is_valid():
           project =  form.save(commit=False)
           project.owner = profile
           project.save()
           return redirect('account')

    context = {'form': form}
    return render (request, 'projects/project_form.html', context)

    ############################# Update OPERATIONS ##############################################

@login_required(login_url='login')

def UpdateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = projectForm(instance=project)

    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render (request, 'projects/project_form.html', context)


    ############################# Delete OPERATIONS ##############################################

@login_required(login_url='login')

def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect ('account')
    context = {'object': project }
    return render(request, 'delete_template.html', context)

