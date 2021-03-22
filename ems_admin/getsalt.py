import random
import string


def get_salt():
    return ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, random.randint(5, 10)))
