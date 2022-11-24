from PIL import Image

file_path = './torch.png'

img = Image.open(file_path)
img = img.convert('RGBA')

width, height = img.size
#find most used color
pixels = img.getcolors(width * height)
most_frequent_pixel = pixels[0]

for count, colour in pixels:
    if count > most_frequent_pixel[0]:
        most_frequent_pixel = (count, colour)

#make most frequent pixel transparent
for x in range(width):
    for y in range(height):
        pixel = img.getpixel((x, y))
        #if pixel are almost the same
        if abs(pixel[0] - most_frequent_pixel[1][0]) < 10 and abs(pixel[1] - most_frequent_pixel[1][1]) < 10 and abs(pixel[2] - most_frequent_pixel[1][2]) < 10:
            img.putpixel((x, y), (255, 255, 255, 0))
            
img.save('./torch_out.png')