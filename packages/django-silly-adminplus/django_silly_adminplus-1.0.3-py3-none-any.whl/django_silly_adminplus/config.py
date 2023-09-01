from django.conf import settings


SILLY_ADMINPLUS = {
    'TEMPLATE': 'adminplus.html',
    'DSAP_PREFIX': 'dsap/',
    'USE_ADMINPLUS_APP': False,
}

try:
    for key in settings.SILLY_ADMINPLUS:
        SILLY_ADMINPLUS[key] = settings.SILLY_ADMINPLUS[key]
except AttributeError:
    pass
