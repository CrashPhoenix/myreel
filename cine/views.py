from django.http import HttpResponse
from django.shortcuts import render_to_response

from bom import BOM


def index(request):
    #return HttpResponse("Hello, world. You're at cine.")
    bom = BOM()

    movies = bom.weekend_chart()

    xdata = []
    titles = []
    ydata = []

    for (i, m) in enumerate(movies):
        xdata.append(i)
        titles.append(str(m.title))
        ydata.append(m.gross_val)

    extra_serie = {"tooltip": {"y_start": "$", "y_end": ""}}

    chartdata = {
        'x': titles,
        #'name1': 'Weekend Box Office Charts',
        'y1': ydata, 'extra1': extra_serie
        #'y2': ydata, 'extra2': extra_serie
    }

    for i in range(0, len(xdata)):
        chartdata['name%d' % (i+1)] = titles[i]
        chartdata['y%d' % (i+1)] = [ydata[i]]
        chartdata['extra%d' % (i+1)] = extra_serie

    charttype = "multiBarHorizontalChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'height': '90%', 'width': '100%'
    }

    return render_to_response('multibarhorizontalchart.html', data)