from django.http import HttpResponse
from django.shortcuts import render_to_response

from bom import BOM, DAILY_CHART, WEEKEND_CHART, WEEKLY_CHART

bom = None
def index(request, title=DAILY_CHART):
    bom = BOM(title)

    if title == WEEKEND_CHART:
        _chart = 'Weekend Charts'
    elif title == WEEKLY_CHART:
        _chart = 'Weekly Charts'
    else:
        _chart = 'Daily Charts'


    movies = request.session.get(_chart, False)

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

        request.session[m.movie_id] = m.movie_id

    request.session[_chart] = mvs

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
        'height': '80%', 'width': '100%',
        'kw_extra': kw_extra,
        'movies': mvs,
        'chart': _chart,
        'title': title,
        'date': bom.date
    }

    return render_to_response('index.html', data)
