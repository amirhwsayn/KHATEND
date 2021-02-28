from django.utils.crypto import get_random_string


def Random_Token():
    return get_random_string(100)


def Random_Name():
    return get_random_string(5)


def Random_Code():
    return get_random_string(6, '1234567890')
