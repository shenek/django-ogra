from django.shortcuts import render

from ogra.charts import OgraPieChart, OgraLineChart, OgraColumnChart


def index(request):
    backend = request.GET.get('backend', 'raphael')

    pie_chart = _create_pie(name='first', title='First Chart', backend=backend)
    column_chart = _create_column(name='second', title='Second Chart', backend=backend)
    line_chart = _create_line(name='third', title='Third Chart', backend=backend)

    return render(
        request,
        'index.html',
        {
            'charts': [pie_chart, column_chart, line_chart],
        }
    )


def _create_pie(name, title, backend):
    data = [
        {'name': 'first', 'value': 7},
        {'name': 'second', 'value': 11},
        {'name': 'third', 'value': 13},
    ]
    fields = [
        {'name': 'Item Name'},
        {'value': 'Actual Value'},
    ]
    return OgraPieChart(name=name, title=title, data=data, fields=fields, backend=backend)


def _create_column(name, title, backend):
    data = [
        {'name': 'first', 'value': 7},
        {'name': 'second', 'value': 11},
        {'name': 'third', 'value': 13},
    ]
    fields = [
        {'name': 'Item Name'},
        {'value': 'Actual Value'},
    ]
    return OgraColumnChart(name=name, title=title, data=data, fields=fields, backend=backend)


def _create_line(name, title, backend):
    data = [
        {'date': '2013-01-01', 'first_line': 23, 'second_line': 7, 'third_line': 19},
        {'date': '2013-01-02', 'first_line': 19, 'second_line': 23, 'third_line': 7},
        {'date': '2013-01-03', 'first_line': 7, 'second_line': 19, 'third_line': 23},
    ]
    fields = [
        {'date': 'Date (YYYY-MM-DD)'},
        {'first_line': 'First line'},
        {'second_line': 'Second line'},
        {'third_line': 'Third line'},
    ]
    return OgraLineChart(name=name, title=title, data=data, fields=fields, backend=backend)
