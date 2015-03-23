from PIL import Image

im = Image.open("DC/DC1/DC1.1/3243a181-1.jpg")
im = im.convert("1")

def horizontalSmearing(image, limit):
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

def verticalSmearing(image, limit):
    pic = image.load()
    white = 0
    for y in range(0, image.size[0]):
        white = 0
        for x in range(0, image.size[1]):
            if pic[y,x] == 255:
                white += 1
            elif pic[y,x] == 0 or x == image.size[0]:
                if white >= limit and white < 50:
                    for i in range(x, x-white-1, -1):
                        pic[y,i] = 0
                white = 0
    return image

def combine(image1, image2):
    pic1 = image1.load()
    pic2 = image2.load()
    newImage = Image.new("1", (image1.size[0], image1.size[1]), "white")
    combinedImage = newImage.load()
    for y in range(0, image1.size[1]):
        for x in range(0, image1.size[0]):
            combined = pic1[x,y] + pic2[x,y]
            if combined == 0:
                combinedImage[x,y] = 0
    return newImage




horizontalImage = horizontalSmearing(im, 2)
horizontalImage.save("horizontal_processed.png")

verticalImage = verticalSmearing(horizontalImage, 3)
verticalImage.save("vertical_processed.png")

combinedImage = combine(horizontalImage, verticalImage)
combinedImage.save("combined_processed.png")

