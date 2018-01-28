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
            con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
            cursor = con.cursor()
            cursor.execute("SELECT ID FROM ORGANIZER_SEMESTER where USER_ID=:user_id AND is_active=1", user_id=user.id)
            semester = cursor.fetchone()[0]
            group = request.POST['group']
            cursor.execute(
                "insert into ORGANIZER_GROUP (NAME, SEMESTER_ID, USER_ID) VALUES (:name, :semester_id, :user_id)", name=group, semester_id=semester, user_id=user.id)
            con.commit()
        elif request.POST.get('first_name'):
            user = request.user
            first = request.POST['first_name']
            middle = request.POST['middle_name']
            last = request.POST['last_name']
            dateBirth = datetime.datetime.strptime(request.POST['dateBirth'], '%d.%m.%Y').date()
            con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
            cursor = con.cursor()
            cursor.execute("SELECT ID FROM ORGANIZER_SEMESTER where USER_ID=:user_id AND is_active=1", user_id=user.id)
            semester_id = cursor.fetchone()[0]
            cursor.execute("SELECT ID FROM ORGANIZER_GROUP where SEMESTER_ID=:semester AND NAME=:group_name", semester=semester_id, group_name=request.POST['group_name'])
            group = cursor.fetchone()[0]
            cursor.execute(
                "insert into ORGANIZER_PUPIL (FIRST_NAME, LAST_NAME, MIDDLE_NAME, DATEBIRTH, GROUP_ID) VALUES (:first, :last, :middle, :birth, :group_id)",
                 first=first, last=last, middle=middle, birth=dateBirth, group_id=group)
            con.commit()
        elif request.POST.get('first_name_edit'):
            user = request.user
            con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
            cursor = con.cursor()
            first = request.POST['first_name_edit']
            middle = request.POST['middle_name']
            last = request.POST['last_name']
            dateBirth = datetime.datetime.strptime(request.POST['dateBirth'], '%d.%m.%Y').date()
            pupil_id = request.POST['pupil_id']
            cursor.execute(
                "update ORGANIZER_PUPIL set FIRST_NAME=:first, LAST_NAME=:last, MIDDLE_NAME=:middle, DATEBIRTH=:birth where ID=:pupil",
                 first=first, last=last, middle=middle, birth=dateBirth, pupil=pupil_id)
            con.commit()
        elif request.POST.get('del_pupil'):
            pupil_id = request.POST['del_pupil']
            con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
            cursor = con.cursor()
            cursor.execute(
                "delete from ORGANIZER_PUPIL where ID=:pupil",  pupil=pupil_id)
            con.commit()

        return render(request, 'groups.html', {})
    else:
        return redirect('login')


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

def logoutq(request):
    logout(request)
    return redirect('login')


def registration(request):
    if request.POST:
        #con = cx_Oracle.connect('SCOTT/python@localhost/oracal')
        #cursor = con.cursor()
        username = request.POST['username']
        password = request.POST['password']
        #cursor.execute("insert into AUTH_USER (PASSWORD, IS_SUPERUSER, USERNAME, IS_STAFF, IS_ACTIVE, DATE_JOINED) VALUES (:password, '0', :username, '0', '1', :now)", password=password, username=username, now=datetime.datetime.now())
        #con.commit()
        user = User.objects.create_user(username, 'email@gmail.com', password)
        user.save()
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
        pupils = Pupil.objects.filter(group__in=groups).values('id', 'first_name', 'last_name', 'middle_name', 'group__name', 'group__semester__id', 'dateBirth')
        data = json.dumps(list(pupils), default=str)
        return HttpResponse(data, content_type='application/json')
    else:
        return redirect('login')
