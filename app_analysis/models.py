from django.db import models

class FileModel(models.Model):
    name = models.CharField(max_length=255)
    file_field = models.FileField(upload_to='Texts/uploaded')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SelectedFile(models.Model):
    files = models.ManyToManyField(FileModel)
    keyword = models.CharField(max_length=255, null = True, default = None)

    def __str__(self):
        return self.name





#class KeywordForm(models.Model):
  #  name = models.CharField(max_length=255)
 #   file = models.FileField(upload_to='Texts')

 #   def __str__(self):
 #       return self.name





