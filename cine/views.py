from django.http import HttpResponse
from django.shortcuts import render_to_response

from bom import BOM, DAILY_CHART, WEEKEND_CHART, WEEKLY_CHART

import time, random, datetime

def index(request, title=DAILY_CHART):
    bom = BOM(title)

    if title == WEEKEND_CHART:
        _chart = 'Weekend Charts'
    elif title == WEEKLY_CHART:
        _chart = 'Weekly Charts'
    else:
        _chart = 'Daily Charts'

    request.session['chart'] = title

    movies = request.session.get(title, False)

    if not movies:
        movies = bom.get_chart()

    xdata = []
    titles = []
    ydata = []
    ranks = []
    mvs = []

    for (i, m) in enumerate(movies):
        xdata.append(i+1)
        titles.append(str(m.title))
        ydata.append(m.gross_val)
        ranks.append({'title':m.title, 'rank':m.rank})
        mvs.append(m)

    request.session[title] = mvs

    extra_serie = {"tooltip": {"y_start": "$", "y_end": ""}}

    kw_extra = {
        'show_legend': False,
        'show_labels': False,
    }

    chartdata = {
        'x': xdata,
    }
    
    for i in range(0, len(xdata)):
        chartdata['name%d' % (i+1)] = titles[i]
        chartdata['y%d' % (i+1)] = [ydata[i]]
        chartdata['extra%d' % (i+1)] = extra_serie
    
    charttype = "multiBarHorizontalChart"
    chartcontainer = "multibarhorizontalchart_container"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'height': '80%', 'width': '100%',
        'kw_extra': kw_extra,
        'movies': mvs,
        'chart': _chart,
        'title': title,
        'date': bom.date
    }

    return render_to_response('index.html', data)

def movie(request, movie_id):
    """
    lineChart page
    """
    _chart = request.session.get('chart')
    movies = request.session.get(_chart, False)
    if movies:
        for m in movies:
            if m.movie_id == movie_id:
                movie = m
                break
                
    data = {}
    xdata = []
    ydata = []
    trend_data = None

    try:
        trend_data = movie.get_trend(_chart)
    except:
        data['unavailable'] = True

    if trend_data != None:
        for p in trend_data:
            (x, date, rank, gross) = p
            xdata.append(int(x))
            gross = gross[1:].replace(',', '')
            ydata.append(int(gross))

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
        'color': '#a4c639'
    }
    chartdata = {'x': xdata,
                 'name1': movie.title, 'y1': ydata}

    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    _data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'chart': movie.title,
        'kw_extra': {
            'x_is_date': False,
            'tag_script_js': True,
            'show_labels': False,
        },
        'height': '80%', 'width': '90%'
    }
    data.update(_data)
    return render_to_response('movie.html', data)
