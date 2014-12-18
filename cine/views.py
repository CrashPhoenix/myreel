from django.http import HttpResponse
from django.shortcuts import render_to_response

from bom import BOM

import random
import datetime
import time

def index(request):
    """
    lineChart page
    """
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 150
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
        'color': '#a4c639'
    }
    extra_serie2 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
        'color': '#FF8aF8'
    }
    chartdata = {'x': xdata,
                 'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1,
                 'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2}

    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%d %b %Y %H',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('linechart.html', data)

'''
def index(request):
    #return HttpResponse("Hello, world. You're at cine.")
    bom = BOM()

    movies = bom.weekend_chart()

    xdata = []
    titles = []
    ydata = []

    for (i, m) in enumerate(movies):
        xdata.append(i+1)
        titles.append(str(m.title))
        ydata.append(m.gross_val)

    extra_serie = {"tooltip": {"y_start": "$", "y_end": ""}}

    kw_extra = {
        'show_legend': False,
        'show_labels': False,
        'color_category': 'category20'
    }

    chartdata = {
        'x': xdata,
        #'name1': 'Weekend Box Office Charts',
        #'y1': ydata, 'extra1': extra_serie,
        #'y2': ydata, 'extra2': extra_serie
        #'kwargs': kwargs
    }
    
    for i in range(0, len(xdata)):
        chartdata['name%d' % (i+1)] = titles[i]
        chartdata['y%d' % (i+1)] = [ydata[i]]
        chartdata['extra%d' % (i+1)] = extra_serie
    
    charttype = "multiBarHorizontalChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'height': '80%', 'width': '110%',
        'kw_extra': kw_extra
    }

    return render_to_response('multibarhorizontalchart.html', data)
'''