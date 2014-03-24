import json
from django.db.models.query import QuerySet


def convert_to_data_table(data, fields=None, label_formater=None):
    res = {}

    # Make sure that data will contain compatible structure (list of dicts)
    if isinstance(data, QuerySet):
        data = data.values()

    # Data are empty TBD
    if not data:
        return res

    # Fields to list of tuples
    if not fields:
        fields = map(lambda x: (x, x, ), sorted(data[0].keys()))
    else:
        fields = map(lambda x: (x.keys()[0], x[x.keys()[0]], ), fields)

    fields_names = map(lambda x: x[0], fields)
    field_trans = {x[0]: x[1] for x in fields}

    # Determine the field types
    sample_data = {}
    for element in data:
        for field in fields_names:
            if element[field] and not field in sample_data:
                sample_data[field] = element[field]

    for key in set(fields_names) - set(sample_data.keys()):
        sample_data[key] = None

    def get_type(element):
        return 'number' if isinstance(element, (int, long, float)) else 'string'

    # Set the cols in the proper format
    res['cols'] = [{'label': field_trans[k], 'type': get_type(sample_data[k])} for k in fields_names]

    # Process rows
    res['rows'] = []
    for element in data:
        new_row = {'c': []}
        for field in fields_names:
            new_row['c'].append({'v': element[field]})

        # Format the first value according to the label_formater function
        if label_formater and new_row['c']:
            new_row['c'][0]['v'] = label_formater(new_row['c'][0]['v'])

        res['rows'].append(new_row)

    return res


class OgraChart(object):
    type = None

    def __init__(self, name, **kwargs):
        self.name = name
        self.fields = kwargs.get('fields')
        self._data = kwargs.get('data', [])
        self.title = kwargs.get('title', '')
        self.label_formater = kwargs.get('label_formater')
        self.backend = kwargs.get('backend', 'raphael')
        self.options = kwargs.get('options', {})

    @property
    def dom_id(self):
        return self.name

    @property
    def data(self):
        res = self._data if self._data else []
        return convert_to_data_table(res, self.fields, self.label_formater)

    @property
    def json(self):
        res = {
            'element_id': self.dom_id,
            'data': self.data,
            'chart_type': self.type,
            'library': self.backend,
            'options': self.options,
        }
        return json.dumps(res)


class OgraPieChart(OgraChart):
    type = "pie"

    def __init__(self, name, **kwargs):
        super(OgraPieChart, self).__init__(name, **kwargs)

    @property
    def dom_id(self):
        return "%s_pie" % self.name

    @property
    def javascript(self):
        res = []
        res.append('var %s_data = %s;' % (self.dom_id, json.dumps(self.data)))
        res.append("Ogra.graph('%s', %s_data, 'pie', '%s', { x: %s, y: %s, radius: %s, title: '%s', preserveValues: %s, reformat_numbers: '%s' });\n" % (
            self.dom_id,
            self.dom_id,
            self.backend,
            self.options.get('left', 200),
            self.options.get('top', 150),
            self.options.get('radius', 100),
            self.title,
            self.options.get('preserve_values', "true"),
            self.options.get('reformat_numbers', "reduce_number"),
        ))
        return '\n'.join(res)


class OgraColumnChart(OgraChart):
    type = "column"

    def __init__(self, name, **kwargs):
        super(OgraColumnChart, self).__init__(name, **kwargs)

    @property
    def dom_id(self):
        return "%s_bar" % self.name

    @property
    def javascript(self):
        res = []
        res.append('var %s_data = %s;' % (self.dom_id, json.dumps(self.data)))
        res.append("Ogra.graph('%s', %s_data, 'column', '%s', { x: %s, y: %s, gwidth: %s, gheight: %s, grid_num: %s, title: '%s', reformat_numbers: %s });\n" % (
            self.dom_id,
            self.dom_id,
            self.backend,
            self.options.get('left', 80),
            self.options.get('top', 30),
            self.options.get('width', 320),
            self.options.get('height', 200),
            self.options.get('grid_num', 4),
            self.title,
            self.options.get('reformat_numbers', "true"),
        ))
        return '\n'.join(res)


class OgraLineChart(OgraChart):
    type = "line"

    def __init__(self, name, **kwargs):
        super(OgraLineChart, self).__init__(name, **kwargs)

    @property
    def dom_id(self):
        return "%s_line" % self.name

    @property
    def javascript(self):
        res = []
        res.append('var %s_data = %s;' % (self.dom_id, json.dumps(self.data)))
        res.append("Ogra.graph('%s', %s_data, 'line', '%s', { x: %d, y: %d, gwidth: %d, gheight: %d, title: '%s' });\n" % (
            self.dom_id,
            self.dom_id,
            self.backend,
            self.options.get('left', 80),
            self.options.get('top', 30),
            self.options.get('height', 500),
            self.options.get('width', 1000),
            self.title,
        ))
        return '\n'.join(res)