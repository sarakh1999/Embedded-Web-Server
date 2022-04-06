from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Directory(models.Model):
    parent_dir = models.ForeignKey(
        'Directory', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    abs_path = models.CharField(max_length=1000, blank=True)

    def get_name(self):
        if self.abs_path == '/':
            return '/'
        else:
            return self.abs_path.split('/')[-1]

    def __str__(self):
        return self.abs_path


class File(models.Model):
    parent_dir = models.ForeignKey(Directory, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    abs_path = models.CharField(max_length=1000)
    file = models.FileField(upload_to='uploaded_files')

    def get_name(self):
        if self.abs_path == '/':
            return '/'
        else:
            return self.abs_path.split('/')[-1]

    def __str__(self):
        return self.abs_path
