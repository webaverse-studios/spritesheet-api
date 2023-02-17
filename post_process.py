from PIL import Image

def getLeftOrRight(img: Image):
    img = img.convert('RGBA')

    width, height = img.size
    pixels = img.getcolors(width * height)
    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if abs(pixel[0] - most_frequent_pixel[1][0]) < 10 and abs(pixel[1] - most_frequent_pixel[1][1]) < 10 and abs(pixel[2] - most_frequent_pixel[1][2]) < 10:
                img.putpixel((x, y), (255, 255, 255, 0))
    
    
    img = img.convert('RGBA')
    width, height = img.size
    cel_width = width / 4
    cel_height = height / 4
    cell = img.crop((0, 0, cel_width, cel_height))
    pixel = cell.getpixel((cel_width / 2, cel_height / 2))
    alpha = pixel[3]
    if alpha == 0:
       return False #right
    else: 
        return True #left
    

def postprocessImg(img1: Image):
    isLeft = getLeftOrRight(img1)
    if not isLeft:
        width = img1.size[0]
        height = img1.size[1]
        qHeight = height / 4

        def cutImgTo4Rows(img: Image):
            imgs = []
            for i in range(4):
                imgs.append(img.crop((0, i * qHeight, width, (i + 1) * qHeight)))
            return imgs

        imgs1 = cutImgTo4Rows(img1)

        imgs1[1], imgs1[2] = imgs1[2], imgs1[1]

        img1 = Image.new("RGBA", (width, height))
        for i in range(4):
            img1.paste(imgs1[i], (0, int(i * qHeight)))

        return img1
    return img1