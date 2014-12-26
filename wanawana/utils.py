from django.conf import settings


def get_base_url(request):
    if filter(lambda x: x != "*", settings.ALLOWED_HOSTS):
        return filter(lambda x: x != "*", settings.ALLOWED_HOSTS[0])

    return request.META["SERVER_NAME"]
