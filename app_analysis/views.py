import os

from django.shortcuts import render, redirect
from .models import FileModel,FreqWord
from .forms import UploadFileForm, SelectedFileForm,SelectedQForm
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
import math


from django.http import HttpResponse

import matplotlib.pyplot as plt
from io import BytesIO
import base64



def plot(request):
     # displlAndodds.htmlからデータ取得
        words = request.POST.getlist('word')
        target_counts = request.POST.getlist('target_count')

        words = [word.strip() for word in words]
        target_counts = [int(count) for count in target_counts]

        # グラフ生成
        plt.plot(words, target_counts, marker='o')  # x-yグラフ生成
        plt.xlabel('Word')
        plt.ylabel('Target Count')
        plt.title('Top Words by Target Count')

        # グラフを画像として保存
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # 画像をbase64エンコードしてHTMLに埋め込む
        graphic = base64.b64encode(image_png).decode('utf-8')
        plt.close()

        return render(request, 'app_analysis/plot.html', {'graphic': graphic})








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
        form = SelectedFileForm(request.POST, request.FILES)
        
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
    dict_group = {}
    max_word = 0
    selected_files = form

    for file in selected_files:
        freq_words = list(FreqWord.objects.filter(relate_file__id=file.id).order_by('-count'))
        word_group[file.name] = freq_words
        max_word = max(max_word,len(freq_words))

        #Odd計算のメソッドでkeyが単語、valueが頻度のdict型が必要.下の４行を追加しました。
        freq_dict = {fr.word: fr.count for fr in freq_words}
        dict_group[file.name] = freq_dict
    ll_val, odds_val = llAndodd(dict_group)
    request.session['ll_val'] = ll_val
    request.session['odds_val'] = odds_val


    group_index = []
    for i in range(max_word):
        row = []
        for file_name in word_group:
            if i < len(word_group[file_name]):
                row.append(word_group[file_name][i])
            else:
                row.append(None)
        group_index.append(row)

    paginator = Paginator(group_index, 20)  
    page_number = request.GET.get('page', 1)
    results = paginator.get_page(page_number)
    filename = [file.name for file in selected_files]
    print(filename)
    context = {
        "results" : results,
        "filename" : filename,
        
    }
    return  render(request, "app_analysis/qvsk_analysis.html", context)

def displlAndodds(request):
    ll_val = request.session['ll_val']
    odds_val = request.session['odds_val']
    if not ll_val:
        return redirect('qvsk_analysis')
    elif not odds_val:
        return redirect('qvsk_analysis')

    ll_page_number = request.GET.get('ll_page', 1)
    odds_page_number = request.GET.get('odds_page', 1)

    ll_list = list(ll_val.items())
    odds_list = list(odds_val.items())

    ll_paginator = Paginator(ll_list, 1)
    odds_paginator = Paginator(odds_list, 1)

    ll_results = ll_paginator.get_page(ll_page_number)
    odds_results = odds_paginator.get_page(odds_page_number)

   
   
    context = {
        #"ll_val": ll_val,
        #"odds_val": odds_val,
        "ll_results": ll_results,
        "odds_results": odds_results,
    
    }
    return render(request, "app_analysis/displlAndodds.html", context)


#dict_groupを計算できる形に直して、QとKのそれぞれのペアに対してcal_llAndoddsを呼び足して計算。
def llAndodd(dict_group):
    dict_Q = {}
    dict_KR = {}
    val_ll = {}
    val_odds = {}
    for filename in dict_group.keys():
        fileinstance = get_object_or_404(FileModel, name = filename)
        if fileinstance.text_type == 'Q':
            dict_Q[filename] = dict_group[filename]
        else :
            dict_KR[filename] = dict_group[filename] #dict_KR はvalueがファイルの名前、valueが単語の頻度を表す辞書の辞書
    for q_filename, q_freqdict in dict_Q.items():
        for k_filename, k_freqdict in dict_KR.items():
            ll_results, odds_results = cal_llAndodds(q_freqdict, k_freqdict)
            val_ll[(q_filename, k_filename)] = ll_results
            val_odds[(q_filename, k_filename)] = odds_results
        
    

    return val_ll, val_odds




def loglikelihood(f1, f2, n1, n2):
    E1 = n1 * (f1 + f2) / (n1 + n2)
    E2 = n2 * (f1 + f2) / (n1 + n2)
    G2 = 2 * ((f1 * math.log(f1 / E1) if f1 > 0 else 0) + (f2 * math.log(f2 / E2) if f2 > 0 else 0))
    return G2

def Odds_Ratio(target_count, total_target, ref_count,total_reference):
    odds_ratio = (target_count / total_target) / (ref_count / total_reference) if ref_count > 0 else float('inf')
    return odds_ratio

# logliliellihoodとoddsの計算
# targetはQ,referenceはK
def cal_llAndodds(target_freq,reference_freq):
    total_reference = sum(reference_freq.values())
    total_target = sum(target_freq.values())

    llresults = []
    oddsresults = []
    for word in target_freq:
        if word in reference_freq:
            ref_count = reference_freq[word]
        else:
            ref_count = 0
        target_count = target_freq[word]
        ll = loglikelihood(target_count, ref_count, total_target, total_reference)
        odds_ratio = Odds_Ratio(target_count, total_target, ref_count, total_reference)
        llresults.append((word, target_count, ref_count, ll, odds_ratio))
        if not math.isinf(odds_ratio):
            oddsresults.append((word, target_count, ref_count, ll, odds_ratio))


    llresults.sort(key=lambda x: x[3], reverse=True)
    oddsresults.sort(key=lambda x: x[4], reverse=True)

    return llresults, oddsresults