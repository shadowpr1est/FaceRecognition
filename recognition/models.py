from django.db import models

class Attendance(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='attendance/%Y-%m-%d/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
