from PIL import Image
import numpy as np

def cleanImage(img: Image):
   # Convert the image to RGBA format
    img = img.convert('RGB')
    im_array = np.array(img)

    # Get the shape of the image
    height, width, channels = im_array.shape

    # Set the color thresholds for the background colors
    color_threshold_r = 10
    color_threshold_g = 10
    color_threshold_b = 10

    # Loop through the pixels in the image
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the pixel
            r, g, b = im_array[y, x]

            # Check if the pixel is a shade of green
            if abs(r - 0) < color_threshold_r and abs(b - 0) < color_threshold_b:
                # Check the surrounding pixels to see if the current pixel is surrounded by pixels with the same color
                surrounding_pixels = [(y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)]
                same_color = True
                for pixel in surrounding_pixels:
                    y_pos, x_pos = pixel
                    if y_pos < 0 or y_pos >= height or x_pos < 0 or x_pos >= width:
                        continue
                    r_surrounding, g_surrounding, b_surrounding = im_array[y_pos, x_pos]
                    if abs(r - r_surrounding) > color_threshold_r or abs(g - g_surrounding) > color_threshold_g or abs(b - b_surrounding) > color_threshold_b:
                        same_color = False
                        break
                if same_color:
                    # Set the alpha value of the pixel to 0 to make it transparent
                    im_array[y, x] = 0

    # Create a new image from the modified NumPy array
    transparent_im = Image.fromarray(im_array)
    
      # Create a new image from the modified NumPy array
    transparent_im = Image.fromarray(im_array)

    #remove white background
    transparent_im = transparent_im.convert("RGBA")
    datas = transparent_im.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    transparent_im.putdata(newData)

    # Save the transparent image
    return transparent_im