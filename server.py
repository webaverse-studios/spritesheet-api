from fastapi import FastAPI
from fastapi.responses import FileResponse
from api import initModel, do_run
from pymatting import cutout
import PIL
from crop import crop

app = FastAPI()

@app.get("/")
async def root(s: str):
    if s.find("spritesheet") == -1:
        s = s + " spritesheet"

    cutFileName = None
    isBlack = True

    while isBlack == True:
        res = do_run(s)
        print(res)
        filename = res[0] + "/" + res[1] + "(" + str(res[2]) + ")_0.png"
        preCutFileName = res[0] + "/" + res[1] + "(" + str(res[2]) + ")_pre_cut_0.png"
        cutFileName = res[0] + "/" + res[1] + "(" + str(res[2]) + ")_cut_0.png"

        img = PIL.Image.open(filename)
        extrema = img.convert("L").getextrema()
        if extrema == (0, 0):
            isBlack = True
        else:
            isBlack = False
         
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
            
            img = crop(img)   
            img.save(preCutFileName)
            
            cutout(preCutFileName, "./mask.png", cutFileName)

    return FileResponse(cutFileName)


if __name__ == "__main__":
    initModel()
    print("model initialized")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777, log_level="debug")