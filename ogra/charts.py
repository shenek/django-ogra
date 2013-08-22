from django.utils import simplejson
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

    def __init__(self, name, **kwargs):
        self.name = name
        self.fields = kwargs['fields'] if 'fields' in kwargs else None
        self._data = kwargs['data'] if 'data' in kwargs else []
        self.title = kwargs['title'] if 'title' in kwargs else ""
        self.label_formater = kwargs['label_formater'] if 'label_formater' in kwargs else None
        self.backend = kwargs.get('backend', 'raphael')

    @property
    def dom_id(self):
        return self.name

    @property
    def data(self):
        res = self._data if self._data else []
        return convert_to_data_table(res, self.fields, self.label_formater)


class OgraPieChart(OgraChart):
    left = 200
    top = 150
    radius = 100
    preserveValues = 'true'  # == don't sort the data before creating piechart before ('true'/'false')
    reformat_numbers = 'reduce_number'

    @property
    def dom_id(self):
        return "%s_pie" % self.name

    @property
    def javascript(self):
        res = []
        res.append('var %s_data = %s;' % (self.dom_id, simplejson.dumps(self.data)))
        res.append("Ogra.graph('%s', %s_data, 'pie', '%s', { x: %s, y: %s, radius: %s, title: '%s', preserveValues: %s, reformat_numbers: '%s' });\n" % (
            self.dom_id,
            self.dom_id,
            self.backend,
            self.left,
            self.top,
            self.radius,
            self.title,
            self.preserveValues,
            self.reformat_numbers,
        ))
        return '\n'.join(res)


class OgraColumnChart(OgraChart):
    grid_num = 3
    left = 80
    top = 30
    height = 200
    width = 320

    def __init__(self, name, **kwargs):
        super(OgraColumnChart, self).__init__(name, **kwargs)

    @property
    def dom_id(self):
        return "%s_bar" % self.name

    @property
    def javascript(self):
        res = []
        res.append('var %s_data = %s;' % (self.dom_id, simplejson.dumps(self.data)))
        res.append("Ogra.graph('%s', %s_data, 'column', '%s', { x: %s, y: %s, gwidth: %s, gheight: %s, grid_num: %s, title: '%s' });\n" % (
            self.dom_id,
            self.dom_id,
            self.backend,
            self.left,
            self.top,
            self.width,
            self.height,
            self.grid_num,
            self.title,
        ))
        return '\n'.join(res)


class OgraLineChart(OgraChart):
    left = 80
    top = 30
    height = 500
    width = 1000

    def __init__(self, name, **kwargs):
        super(OgraLineChart, self).__init__(name, **kwargs)

    @property
    def dom_id(self):
        return "%s_line" % self.name

    @property
    def javascript(self):
        res = []
        res.append('var %s_data = %s;' % (self.dom_id, simplejson.dumps(self.data)))
        res.append("Ogra.graph('%s', %s_data, 'line', '%s', { x: %d, y: %d, gwidth: %d, gheight: %d, title: '%s' });\n" % (
            self.dom_id,
            self.dom_id,
            self.backend,
            self.left,
            self.top,
            self.width,
            self.height,
            self.title,
        ))
        return '\n'.join(res)
