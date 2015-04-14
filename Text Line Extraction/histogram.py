from PIL import Image

original = Image.open("DC/DC1/DC1.1/AA03-1.jpg")
im = original.convert("1")

def histogram(image):
    pic = image.load()
    whitelines = []
    black = 0
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            if pic[x,y] == 0:
                black += 1
        whitelines.append(black)
        black = 0
    return whitelines

def paintLines(image, lines):
    rgb_img = image.convert("RGB")
    pic = rgb_img.load()
    position = 0
    blackline = False
    for l in lines:
        if l == 0 and blackline:
            for x in range(0, image.size[0]):
                pic[x,position] = (255,40,36)
            blackline = False
        else:
            for x in range(0, image.size[0]):
                if pic[x,position] == (0,0,0):
                    blackline = True
                    break
        position += 1
    return rgb_img

hist = histogram(im)
image_lines = paintLines(im, hist)
image_lines.save("histo_pic.png")
