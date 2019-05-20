from PIL import Image
import os

for fname in os.listdir('./'):
    print(fname, end=' ')
    if 'jpeg' in fname and fname != 'jpegTojpg.py':
        im = Image.open(fname)
        rgb_im = im.convert('RGB')
        rgb_im.save(fname.replace('jpeg', 'jpg'))
        os.remove(fname)
        print('converted!')
    else:
        print('')
