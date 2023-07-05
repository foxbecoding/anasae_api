import string, secrets, os
from PIL import Image
import tempfile

def tmp_image(img_format = 'jpg'):
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.{}'.format(img_format), prefix="test_img_")
    if img_format == 'jpg':
        img_format = 'jpeg'
    image.save(tmp_file, img_format)
    tmp_file.seek(0)
    return tmp_file

def create_uid(prefix = '') -> str : 
    uid_str = ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(9)))
    return prefix+uid_str

def is_valid_square_img(img_file) -> bool: 
    img = Image.open(img_file)
    print(img.size)
    pass
