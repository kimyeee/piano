import os
from PIL import Image
def change_img_type(img_path):

    img = Image.open(img_path)
    img = img.convert('RGB')
    img.save('../myspider/lo/415.jpg')

for i in range(9999):
    change_img_type('../myspider/LOGO/415.jpg')
    img_path = '../myspider/LOGO/%s.jpg'%i
    if not os.path.isfile(img_path):
        continue
    img = Image.open(img_path)
    img = img.convert('RGB')
    img.save('../myspider/lo/%s.jpg'%i)