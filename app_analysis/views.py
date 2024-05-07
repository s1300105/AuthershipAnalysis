from django.shortcuts import render, redirect
from .models import FileModel
from .forms import UploadFileForm, SelectedFileForm

def home(request):
    files = FileModel.objects.all()
    return render(request, "app_analysis/home.html", {"files":files})




def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UploadFileForm()
    
    return render(request, "app_analysis/upload.html", {"form" : form})


def file_detail(request, pk):
    file = FileModel.objects.get(id=pk)
    return render(request, "app_analysis/file_detail.html", {"file":file})

def deletefile(request, pk):
    file = FileModel.objects.get(id=pk)
    if request.method == 'POST':
        file.delete()
        return redirect("home")
    return render(request, "app_analysis/delete.html", {"file":file})


def updatefile(request, pk):
    file = FileModel.objects.get(id=pk)
    form = UploadFileForm(instance=file)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "app_analysis/upload.html", {"form":form})
    

def analysis(request):
    form = SelectedFileForm()   
    return render(request, "app_analysis/analysis.html", {"form" : form})


