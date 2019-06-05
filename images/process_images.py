from PIL import Image
import os

small_list = []
reg_list = []

# Rename all files to .jpg and resize them if they arent already
for fname in os.listdir('.'):
	if 'jpeg' in fname and fname != 'process_images.py':
		im = Image.open(fname)
		rgb_im = im.convert('RGB')
		rgb_im.save(fname.replace('jpeg', 'jpg'))
		print('converting {}'.format(fname))
		os.remove(fname)

	if '_small' in fname:
		small_list.append(fname)
	else:
		reg_list.append(fname)

small_list = map(lambda str: str.replace('_small', ''), small_list)
not_resized_images = list(set(reg_list) - set(small_list))

for fname in not_resized_images:
	if '.jpg' in fname and fname != 'process_images.py':	
		basewidth = 1000
		img = Image.open(fname)
		wpercent = (basewidth / float(img.size[0]))
		hsize = int((float(img.size[1]) * float(wpercent)))
		img = img.resize((basewidth, hsize), Image.LANCZOS)
		fname_split = fname.split('.')
		new_fname = fname_split[0] + '_small.' + fname_split[1]
		print('creating {}'.format(new_fname))
		img.save(new_fname)
