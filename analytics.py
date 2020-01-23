from string import Template
from django.utils.safestring import mark_safe

GOOGLE_ANALYTICS_TAG = None

OPTIMIZE_TAG = None

GTAG_MANAGER_TAG = None

class Analytics:
    base = dict()

    def __str__(self):
        return str(self.base)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

class GoogleOptimize(Analytics):
    def __init__(self):
        template = Template(
            "<script>\
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){\
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\
            })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');\
            \
            ga('create', 'UA-148220996-1', 'auto', {'siteSpeedSampleRate': 100});\
            ga('require', '$optimize_tag');\
            </script>"
        )
        self.base.update({'html': template.substitute(optimize_tag=OPTIMIZE_TAG)})

def analytics_context_processor():
    return {
        'google_optimize': GoogleOptimize()
    }

print(analytics_context_processor())