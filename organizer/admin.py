from django.contrib import admin

# Register your models here.
from .models import Group, Pupil, Semester, Subject, Lesson


class SemesterInline(admin.StackedInline):
    model = Semester
    fieldsets = (
        ('Semester info', {
         'fields': ('year', 'number', 'user')
         }),

    )
    inline_classes = ('grp-open',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('number', 'year')
    fieldsets = (
        ('Semester info', {
         'fields': ('year', 'number', 'user', 'start_date', 'end_date')
         }),
    )


class GroupInline(admin.StackedInline):
    model = Group
    fieldsets = (
        ('Group info', {
         'fields': ('name')
         }),

    )
    inline_classes = ('grp-open',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    fieldsets = (
        ('Group info', {
         'fields': ('name', 'semester', 'user')
         }),
    )


class PupilInline(admin.StackedInline):
    model = Pupil
    fieldsets = (
        ('Pupil info', {
         'fields': ('first_name', 'middle_name', 'last_name', 'dateBirth', 'group')
         }),

    )
    inline_classes = ('grp-open',)


@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'group')
    fieldsets = (
        ('Pupil info', {
         'fields': ('first_name', 'middle_name', 'last_name', 'dateBirth', 'group')
         }),
    )


class SubjectInline(admin.StackedInline):
    model = Subject
    fieldsets = (
        ('Subject info', {
         'fields': ('name', 'semester')
         }),

    )
    inline_classes = ('grp-open',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        ('Subject info', {
         'fields': ('name', 'semester')
         }),
    )


class LessonInline(admin.StackedInline):
    model = Lesson
    fieldsets = (
        ('Lesson info', {
         'fields': ('week_day', 'week_number', 'lesson_number',)
         }),

    )
    inline_classes = ('grp-open',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('week_day', 'week_number', 'lesson_number',)
    fieldsets = (
        ('Lesson info', {
         'fields': ('week_day', 'week_number', 'lesson_number', 'group', 'subject')
         }),
    )
