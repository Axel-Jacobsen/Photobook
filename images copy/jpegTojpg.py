from PIL import Image
import os

for fname in os.listdir('./'):
    print(fname)
    im = Image.open(fname)
    rgb_im = im.convert('RGB')
    rgb_im.save(fname.replace('jpeg', 'jpg'))

