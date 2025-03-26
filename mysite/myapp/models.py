from django.contrib.auth.models import User
from django.db import models

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assign existing notes to user with ID 1
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
