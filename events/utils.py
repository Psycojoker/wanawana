import string
import random

from django.contrib.auth.decorators import user_passes_test


def generate_random_password(size):
    return ''.join(random.SystemRandom().choice(string.hexdigits) for n in xrange(size))


def user_is_professor(function):
    return user_passes_test(lambda x: hasattr(x, "professor"))(function)
