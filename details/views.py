from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
# Create your views here.
def home(request):
    title = "Project Detail Page"

    context = {
        "title" : title,
        
    }

    return render(request, 'details/home.html', context)


def create_project(request):
    title = "Create Project"
    form = CreateProjectForm(request.POST or None)

    if form.is_valid():
        form.save() 
        return redirect("list")
    
    context = {
        "title": title,
        "form":form,
    }
    return render(request, "details/home.html", context)


def list_project(request):
    title = "List Projects"
    form = CreateProjectForm()
    queryset = ProjectDetail.objects.all()

    context = {
        "title":title,
        "form":form,
        "queryset":queryset
    }
    return render(request, "details/list.html", context)


def update_project(request, pk):
    item = get_object_or_404(ProjectDetail, id=pk)
    form = CreateProjectForm(instance=item)

    if request.method == "POST":
        form = CreateProjectForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return redirect('list')
    
    return render(request, "details/list.html")


def delete_project(request, pk):
    item = get_object_or_404(ProjectDetail, id=pk)
    item.delete()
    return redirect('list')