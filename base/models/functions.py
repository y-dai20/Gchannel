from django.conf import settings
from django.utils.crypto import get_random_string
import uuid

def create_id():
    return get_random_string(settings.ID_LENGTH)

def img_directory_path(instance, filename):
    return '{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])
