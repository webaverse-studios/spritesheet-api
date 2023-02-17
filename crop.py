from PIL import Image

def crop(img):
    img = img.convert('RGBA')
    width, height = img.size
    cel_width = width / 4
    cel_height = height / 4
    cell = img.crop((0, 0, cel_width, cel_height))
    pixel = cell.getpixel((cel_width / 2, cel_height / 2))
    alpha = pixel[3]
    if alpha == 0:
        img = img.crop((cel_width, 0, width, height))
    else: 
        img = img.crop((0, 0, width - cel_width, height))
    return img