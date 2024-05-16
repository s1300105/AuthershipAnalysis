import os

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
    

def keyword(request):
    print("keyword view is called!!")
    form = SelectedFileForm()   
    
    if request.method == 'POST':
        print("request is POSTed")
        form = SelectedFileForm(request.POST, request.FILES);
        
        if form.is_valid():
            file_list = []
            files, keyword = getSelectedfileAndKeyword(form)
            results = searchWord(files, keyword)
            for file_name in results:
                with open(file_name) as f:
                    file_list.append({
                        'file_name':file_name,
                        'sentence':f.read()
                    })
                    #sentence_list[file_name] = f.read()
                    
            context = {
                #'results':results,
                'keyword':keyword,
                'file_list':file_list,
                #'keysentence':sentence
            }
            return render(request, "app_analysis/keyword_analysis.html", context)
           # files = keyword_analysis(form)
            

            #keyword_form = KeywordForm(files)
    return render(request, "app_analysis/keyword.html", {"form" : form})


def getSelectedfileAndKeyword(form):
    obj = []
    filelist = []
    keyword = form.cleaned_data['keyword']
    files = form.cleaned_data['files']
    for file in files:
        obj.append(file.id)
    
    files_objects = FileModel.objects.filter(id__in=obj)
    #return render(request, "app_analysis/keyword_analysis.html", {"files_ids" : files_ids})
    for obj in files_objects:
        filequery = FileModel.objects.get(id=obj.id)
        filelist.append(filequery.file_field)
    return filelist, keyword


def searchWord(files, keyword):
    results = []
    dir = "Texts/KeywordSentences/"
    for file in files:
        with open(file.path) as f:
            text = f.read()
        file_name = os.path.basename(file.name)
        file_name = "Texts/Keyworded/"+keyword+"_"+file_name
        results.append(file_name)
        with open(file_name, mode='a') as g:
            with open(file_name, mode='r') as h:
                text_check = h.read()
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence and sentence not in text_check:
                        sentence += '.\n'
                        g.write(sentence)
    
    return results
                        
                    


    

 


    


    






