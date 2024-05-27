from django.db import models

class FileModel(models.Model):
    CATEGORY = (
      ('Q','Questioned'),
      ('K','Known'),
      ('R','Reference'),
      )
    name = models.CharField(max_length=255)
    file_field = models.FileField(upload_to='Texts/uploaded')
    date = models.DateTimeField(auto_now_add=True)
    text_type = models.CharField(max_length=10,choices=CATEGORY,blank=False)

    def save(self, *args, **kwargs):
        cnt = FileModel.objects.filter(text_type=self.text_type).count()
        self.name = self.text_type + str(cnt+1)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.name


class SelectedFile(models.Model):
    files = models.ManyToManyField(FileModel)
    keyword = models.CharField(max_length=255, null = True, default = None)

    def __str__(self):
        return self.name

class FreqWord(models.Model):
    relate_file = models.ForeignKey(FileModel, on_delete=models.CASCADE, related_name='frequent_words')
    word = models.CharField(max_length=255)
    count = models.IntegerField()
    def __str__(self):
        return f"{self.word}: {self.count}"





#class KeywordForm(models.Model):
  #  name = models.CharField(max_length=255)
 #   file = models.FileField(upload_to='Texts')

 #   def __str__(self):
 #       return self.name





