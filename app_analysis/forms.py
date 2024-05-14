from django.forms import CheckboxSelectMultiple
from django.forms import ModelForm
from .models import FileModel, SelectedFile

#https://docs.djangoproject.com/en/5.0/topics/http/file-uploads/

class UploadFileForm(ModelForm):
    class Meta:
        model = FileModel
        fields = '__all__'


class SelectedFileForm(ModelForm):
    class Meta:
        model = SelectedFile
        fields = ['files', 'keyword']
        widgets = {
            "files" : CheckboxSelectMultiple,
        }
   
