import os

from django.shortcuts import render, redirect
from .models import FileModel,FreqWord
from .forms import UploadFileForm, SelectedFileForm,SelectedQForm
from django.core.paginator import Paginator
from django.views.generic import ListView

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
            
            files, keyword = getSelectedfileAndKeyword(form)
            filenames, partOfsentence = searchWord(files, keyword)

            context = {
                #'results':results,
                'keyword':keyword,
                'filenames':filenames,
                'partOfsentence':partOfsentence
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
    partOfsentence = {}
    filenames = []
    word10 = [] # アンバウンドエラー回避
    dir = "Texts/KeywordSentences/"
    for file in files:
        with open(file.path, encoding="shift_jis") as f: # file_encodingはshift_jisらしいです
            text = f.read()
        file_name = os.path.basename(file.name)
        file_name = "Texts/Keyworded/"+keyword+"_"+file_name
        partOfsentence[file_name] = []
        filenames.append(file_name)
        with open(file_name, mode='a', encoding="shift_jis") as g:
            with open(file_name, mode='r', encoding="shift_jis") as h:
                text_check = h.read()
                sentences = text.split('.')
                for sentence in sentences:
                    words = sentence.split()
                    if keyword in words:
                        keywordindex = words.index(keyword)
                        start_index = max(0, keywordindex - 5)
                        end_index = min(len(words), keywordindex + 6)
                        word10 = words[start_index:end_index]
                    if word10 not in partOfsentence[file_name]:
                        partOfsentence[file_name].append(word10)
                    if keyword in sentence and sentence not in text_check:
                        g.write(sentence)
    
    return filenames, partOfsentence


def qvsk(request):
    form = SelectedQForm()

    if request.method == 'POST':
        form = SelectedQForm(request.POST)
        
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data['files']
            return redirect("qvsk_analysis")
            
    return render(request, "app_analysis/qvsk.html", {"form" : form})

def qvsk_analysis(request):
    form = request.session.get('form_data')
    if not form:
            return redirect('qvsk')
    
    word_group = {}
    max_word = 0
    selected_files = form
    file_id = [file.id for file in selected_files]

    selected_files = FileModel.objects.filter(id__in=file_id)    
    freq_words = FreqWord.objects.filter(relate_file__in=selected_files).order_by('-count') #countの逆

#    for file in selected_files:
        #freq_words = FreqWord.objects.filter(relate_file__in=file).order_by('-count') #countの逆 
#        freq_words = list(file.frequent_words.order_by('-count'))
#        word_group[file.name] = freq_words
#        max_word = max(max_word,len(freq_words))
    
#    group_index = []
#    for i in range(max_word):
#        row = []
#        for file_name in word_group:
#            if i < len(word_group[file_name]):
#                row.append(word_group[file_name][i])
#            else:
#                row.append(None)
#        group_index.append(row)

    #print("test"+str(max_word))
    paginator = Paginator(freq_words, 20)  
    page_number = request.GET.get('page', 1)
    results = paginator.get_page(page_number)

    context = {
        "results" : results,
        "selected_files" : selected_files,
    }
    return  render(request, "app_analysis/qvsk_analysis.html", {"results":results})