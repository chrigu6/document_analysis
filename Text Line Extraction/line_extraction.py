from PIL import Image

im = Image.open("DC/DC1/DC1.1/3243a181-1.jpg")
im = im.convert("1")

def smearing(image, limit):
    pic = image.load()
    white = 0
    for y in range(0, image.size[1]):
        white = 0
        for x in range(0, image.size[0]):
            if pic[x,y] == 255:
                white += 1
            elif pic[x,y] == 0 or x == image.size[0]:
                if white >= limit and white < 50:
                    for i in range(x, x-white-1, -1):
                        pic[i,y] = 0
                white = 0
    return image

processedImage = smearing(im, 2)
processedImage.save("processed.png")
