from PIL import Image
import bs4
import os

def convert_to_jpg(dir: str, fname: str):
    im = Image.open(dir + fname)
    rgb_im = im.convert('RGB')
    print(f'converting {fname}')
    rgb_im.save((dir + fname).replace('jpeg', 'jpg'))
    os.remove(fname)
    fname = fname.replace('jpeg', 'jpg')

def process_fnames(dir: str):
    l = []
    for fname in os.listdir(dir):
        if '.jpeg' in fname:
            convert_to_jpg(dir, fname)
        if '.jpg' in fname:
            l.append(fname)
    return l

def resize(dir: str, im_list: list):
    for fname in im_list:
        basewidth = 1000
        im = Image.open(dir + fname)
        wpercent = (basewidth / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        im = im.resize((basewidth, hsize), Image.LANCZOS)
        print(f'creating {fname} in small_images')
        im.save('small_images/' + fname)

def add_html(dir: str, im_list: list, html_fname: str):
    with open(html_fname) as f:
        txt = f.read()
        soup = bs4.BeautifulSoup(txt, features='html5lib')
        image_div = soup.find('div', {'class', 'image_group'})
        images = image_div.findChildren('img', recursive=False)

        clean_fname = lambda im: im.get('src').replace('small_images/', '')
        is_picture  = lambda fname: fname.get('src').endswith('.jpg')
        existing_ims = list(
                            filter(is_picture,
                                map(clean_fname, 
                                    images)
                                )
                            )

        new_images = list(set(im_list) - set(existing_ims))

        for fname in new_images:
            Image.open(dir + fname).show()
            caption = input('Enter description for file {}: '.format(fname))
            new_tag = soup.new_tag(
                'img', src=f'{dir}{fname}', alt=caption)
            soup.find('div', {'class', 'image_group'}).append(new_tag)
            with open("index.html", "w", encoding='utf-8') as f:
                f.write(str(soup))

        if len(new_images):
            print(f'Inserted {len(new_images)} images!')

if __name__ == '__main__':
    BASE_DIR = './images/'
    SMALL_DIR = './small_images'

    reg_list = process_fnames(BASE_DIR)
    small_list = process_fnames(SMALL_DIR)
    new_ims = list(set(reg_list) - set(small_list))
    resize(BASE_DIR, new_ims)
    add_html(BASE_DIR, new_ims, 'index.html')
