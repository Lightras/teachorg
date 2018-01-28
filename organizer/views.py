from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Semester, Group, Pupil
import simplejson as json
from django.http import HttpResponse
import cx_Oracle
import datetime
# Create your views here.


def groups(request):
    if request.user.is_authenticated:
        if request.POST.get('group'):
            user = request.user
            semester = Semester.objects.get(user=user, is_active=True)
            group = request.POST['group']
            con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
            cursor = con.cursor()
            cursor.execute(
                "insert into ORGANIZER_GROUP (NAME, SEMESTER_ID, USER_ID) VALUES (:name, :semester_id, :user_id)", name=group, semester_id=semester.id, user_id=user.id)
            con.commit()
        elif request.POST.get('first_name'):
            user = request.user
            semester = Semester.objects.get(user=user, is_active=True)
            group = Group.objects.filter(semester=semester)
            group = group.filter(name=request.POST['group_name']).first()
            print(group.id)
            first = request.POST['first_name']
            middle = request.POST['middle_name']
            last = request.POST['last_name']
            dateBirth = request.POST['dateBirth']
            con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
            cursor = con.cursor()
            cursor.execute(
                "insert into ORGANIZER_PUPIL (FIRST_NAME, LAST_NAME, MIDDLE_NAME, GROUP_ID) VALUES (:first, :last, :middle, :group_id)",
                 first=first, last=last, middle=middle, group_id=group.id)
            con.commit()
        elif request.POST.get('first_name_edit'):
            user = request.user
            semester = Semester.objects.get(user=user, is_active=True)
            group = Group.objects.filter(semester=semester)
            group = group.filter(name=request.POST['group_name']).first()
            first = request.POST['first_name_edit']
            middle = request.POST['middle_name']
            last = request.POST['last_name']
            dateBirth = request.POST['dateBirth']
            pupil_id = request.POST['pupil_id']
            con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
            cursor = con.cursor()
            cursor.execute(
                "update ORGANIZER_PUPIL set FIRST_NAME=:first, LAST_NAME=:last, MIDDLE_NAME=:middle where ID=:pupil",
                 first=first, last=last, middle=middle, pupil=pupil_id)
            con.commit()
        elif request.POST.get('del_pupil'):
            pupil_id = request.POST['del_pupil']
            con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
            cursor = con.cursor()
            cursor.execute(
                "delete from ORGANIZER_PUPIL where ID=:pupil",  pupil=pupil_id)
            con.commit()
        semester = Semester.objects.filter(user=request.user).first()
        groups = Group.objects.filter(semester=semester)
        pupils = Pupil.objects.filter(group__in=groups)
        return render(request, 'groups.html', {'groups': groups, 'pupils': pupils})
    else:
        return redirect('login')


def loginq(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('groups')
        else:
            print('qwe')
    return render(request, 'login.html')

def logoutq(request):
    logout(request)
    return redirect('login')


def registration(request):
    if request.POST:
        print(request.POST)
        con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
        cursor = con.cursor()
        username = request.POST['username']
        password = request.POST['password']
        cursor.execute("insert into AUTH_USER (PASSWORD, IS_SUPERUSER, USERNAME, IS_STAFF, IS_ACTIVE, DATE_JOINED) VALUES (:password, '0', :username, '0', '1', :now)", password=password, username=username, now=datetime.datetime.now())
        #res = cursor.fetchone()
        #print(res)
        con.commit()
        # user = User.objects.create_user(username, 'email@gmail.com', password)
        # user.save()
        return redirect('login')
    return render(request, 'registration2.html')

def semesters(request):
    if request.user.is_authenticated:
        return render(request, 'semesters.html')
    else:
        return redirect('login')

def schedule(request):
    if request.user.is_authenticated:
        return render(request, 'schedule.html')
    else:
        return redirect('login')

def subjects(request):
    if request.user.is_authenticated:
        return render(request, 'subjects.html')
    else:
        return redirect('login')


def groupsdata(request):
    if request.user.is_authenticated:
        semester = Semester.objects.filter(user=request.user).first()
        groups = Group.objects.filter(semester=semester)
        pupils = Pupil.objects.filter(group__in=groups).values('id', 'first_name', 'last_name', 'middle_name', 'group__name', 'group__semester__id')
        data = json.dumps(list(pupils))
        return HttpResponse(data, content_type='application/json')
    else:
        return redirect('login')
