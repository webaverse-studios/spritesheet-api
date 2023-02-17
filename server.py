from fastapi import FastAPI
from fastapi.responses import FileResponse
from api import initModel, do_run
from pymatting import cutout
import PIL
from crop import crop
from post_process import postprocessImg
from cleaner import cleanImage
from rembg import remove

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

            img = postprocessImg(img)
            img = img.convert('RGBA')

            width, height = img.size
            img = remove(img)
            
            img = crop(img)   
            #img = cleanImage(img)

            #check if the image is mostly empty
            extrema = img.convert("L").getextrema()
            if extrema == (0, 0):
                isBlack = True
            else:
                img.save(preCutFileName)
                isBlack = False

            
            #cutout(preCutFileName, "./mask.png", cutFileName)

    return FileResponse(preCutFileName)


if __name__ == "__main__":
    initModel()
    print("model initialized")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777, log_level="debug")