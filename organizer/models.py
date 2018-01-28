from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TIMESLOTS = (
    (1, 'Понеділок'), (2, 'Вівторок'),
    (3, 'Середа'), (4, 'Четвер'),
    (5, 'П*ятниця'), (6, 'Субота'),
)


class Semester(models.Model):
    year = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.NullBooleanField(null=True)

    def __str__(self):
        return str(self.year)


class Group(models.Model):
    name = models.CharField(null=True, max_length=10)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Pupil(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=20)
    last_name = models.CharField(null=True, blank=True, max_length=20)
    middle_name = models.CharField(null=True, blank=True, max_length=20)
    dateBirth = models.DateField(null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.last_name


class Subject(models.Model):
    name = models.CharField(null=True, max_length=30)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    week_day = models.IntegerField(choices=TIMESLOTS, verbose_name='День тижня')
    week_number = models.IntegerField(null=True)
    lesson_number = models.IntegerField(null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
