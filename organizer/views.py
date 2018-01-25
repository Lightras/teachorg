from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Semester, Group, Pupil
import simplejson as json
from django.http import HttpResponse
# Create your views here.


def groups(request):
    semester = Semester.objects.filter(user=request.user).first()
    groups = Group.objects.filter(semester=semester)
    pupils = Pupil.objects.filter(group__in=groups)
    return render(request, 'groups.html', {'groups': groups, 'pupils': pupils})


def loginq(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('groups')
        else:
            print('qwe')
    return render(request, 'login.html')


def registration(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, 'email@gmail.com', password)
        user.save()
        return redirect('login')
    return render(request, 'registration.html')

def semesters(request):
    return render(request, 'semesters.html')

def schedule(request):
    return render(request, 'schedule.html')

def subjects(request):
    return render(request, 'subjects.html')


def groupsdata(request):
    semester = Semester.objects.filter(user=request.user).first()
    groups = Group.objects.filter(semester=semester)
    pupils = Pupil.objects.filter(group__in=groups).values('first_name', 'last_name', 'middle_name', 'group__name', 'group__semester__id')
    data = json.dumps(list(pupils))
    return HttpResponse(data, content_type='application/json')
