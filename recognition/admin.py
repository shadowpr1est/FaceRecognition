from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)