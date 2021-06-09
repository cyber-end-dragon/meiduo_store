from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


#  make template use function 'static' and 'url'
def jinja2_environment(**options):
    env = Environment(**options)
    # custom syntax
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
