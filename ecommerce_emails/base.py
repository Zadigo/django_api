from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template import loader, RequestContext, TemplateDoesNotExist

email_templates = [
    'order_confirmation',
    'payment_confirmation'
]

def templates():
    """Loads all the required templates"""
    base = {}
    for template in email_templates:
        base.update({template: loader.render_to_string(template)})
    return base

class Notifications:
    def __init__(self, request, template_name, order_or_reference, **kwargs):
        # self.templates = templates()
        self.subject = None
        self.body = None

        template = loader.render_to_string(template_name, RequestContext(request))