from django import template

from django.utils.safestring import mark_safe

from ..charts import OgraChart

register = template.Library()


@register.filter
def ogra_charts(charts):
    if not charts:
        return ''
    if isinstance(charts, OgraChart):
        charts = [charts]

    res = ""
    for chart in charts:
        res += chart.javascript

    return mark_safe(_wrap_js(res))


def _wrap_js(js):
    return """
<script type="text/javascript">
    window.onload = function(e){
        %s
    }
</script>
""" % js
