from PIL import Image
import bs4
import os

small_list = []
reg_list = []

# Rename all files to .jpg and resize them if they arent already
for fname in os.listdir('./images'):

    if fname == '.DS_Store':
        continue

    if 'jpeg' in fname:
        im = Image.open(fname)
        rgb_im = im.convert('RGB')
        rgb_im.save('images/' + fname.replace('jpeg', 'jpg'))
        print('converting {}'.format(fname))
        os.remove(fname)
        fname = fname.replace('jpeg', 'jpg')

    if '_small' in fname:
        small_list.append(fname.replace(
            'images/', '').replace('.jpg', '').replace('_small', ''))

    else:
        reg_list.append(fname.replace('images/', '').replace('.jpg', ''))

not_resized_images = list(set(reg_list) - set(small_list))

for fname in not_resized_images:

    if '.jpg' in fname:
        basewidth = 1000
        img = Image.open('images/' + fname + '.jpg')
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.LANCZOS)
        new_fname = fname + '_small.jpg'
        print('creating {}'.format(new_fname))
        img.save('images/' + new_fname)

with open('index.html') as f:
    txt = f.read()
    soup = bs4.BeautifulSoup(txt, features='html5lib')
    image_div = soup.find('div', {'class', 'image_group'})
    images = image_div.findChildren('img', recursive=False)
    existing_images = [im.get('src')
                       .replace('images/', '')
                       .replace('.jpg', '')
                       .replace('_small', '')
                       for im in images]

    new_images = list(set(reg_list) - set(existing_images))
    
    for im in new_images:
        alt = input('Enter description for file {}: '.format(im))
        new_soup = bs4.BeautifulSoup(features='html5lib')
        new_tag = soup.new_tag('img', src='images/{}_small.jpg'.format(im), alt=alt)
        soup.find('div', {'class', 'image_group'}).append(new_tag)
        with open("index.html", "w", encoding='utf-8') as f:
            f.write(str(soup))

    if len(new_images):
        print('Inserted {} images!'.format(len(new_images)))

print('Done all tasks!')
