from django.shortcuts import render
from django import forms
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

app_name = 'tasks'
# Create your views here.
def view(request):
    if "tasks" not in request.session:
        request.session["tasks"]= []

    return render(request, "tasks/view.html", {"tasks":request.session["tasks"]})

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

def add(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
        else:
            return render(request, "tasks.add.html", {"form": form})
    return render(request, "tasks/add.html", {"form":NewTaskForm()})

# create and list 
class CreateListTask(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class RetrieveUpdateDestroyTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'