from django.shortcuts import render
import matplotlib.pyplot as plt             #グラフ
import io                                   #入出力 画像の保存
import urllib, base64                       #

from django.http import HttpResponse

def input_data(request):
    return render(request, 'input.html')

def plot_graph(request):
    if request.method == 'POST':
        x_values = list(map(float, request.POST.getlist('x_values')))
        y_values = list(map(float, request.POST.getlist('y_values')))
        
        # プロット作成
        plt.figure()
        plt.plot(x_values, y_values, marker='o')
        plt.title('Plot of x vs y')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        
        # グラフを画像として保存
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

        return render(request, 'plot.html', {'plot_url': uri})
    return HttpResponse("Invalid request")