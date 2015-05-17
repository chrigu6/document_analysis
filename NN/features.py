import os
from PIL import Image

BASE_URL = "/Users/Nic/Desktop/images/"


def extract_pixel_values(image):
    pic = image.convert("1").load()
    features = []
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            features.append(pic[x, y]/255.0 * 1)
    return features


def extract_black_pixel_ratio(image, squares):
    features = []
    allblacks = 0
    pic = image.convert("1").load()
    for i in range(len(squares[1])-1):
        for k in range(len(squares[0])-1):
            black = 0
            for y in range(squares[1][i], squares[1][i+1]):
                for x in range(squares[0][k], squares[0][k+1]):
                    if pic[x, y] == 0:
                        black += 1
            allblacks += black
            features.append(black)
            black = 0
    result = []
    for feature in features:
        result.append(feature / float(allblacks))
    return result


def extract_max(image):
    features = []
    pic = image.convert("1").load()
    for y in range(0, image.size[1], 2):
        for x in range(0, image.size[0], 2):
            features.append(
                (max(max(max(
                    pic[x, y],
                    pic[x+1, y]),
                    pic[x, y+1]),
                    pic[x+1, y+1])) / 255.0 * 1
            )
    return features


def extract_min(image):
    features = []
    pic = image.convert("1").load()
    for y in range(0, image.size[1], 2):
        for x in range(0, image.size[0], 2):
            features.append((min(min(min(
                pic[x, y],
                pic[x+1, y]),
                pic[x, y+1]),
                pic[x+1, y+1])) / 255.0 * 1
            )
    return features


def extract_mean(image):
    features = []
    pic = image.convert("1").load()
    for y in range(0, image.size[1], 2):
        for x in range(0, image.size[0], 2):
            mean = ((
                pic[x, y] +
                pic[x+1, y] +
                pic[x, y+1] +
                pic[x+1, y+1]) / 4) / 255.0 * 1
            features.append(mean)
    return features


def return_tiles(image, squares):
    tiles_y = 2
    if squares % 2 is not 0:
        print "The number of squares has to be even"
    tiles_x = squares / tiles_y
    tiles_sizeX = round(image.size[0] / float(tiles_x))
    tiles_sizeY = round(image.size[1] / 2.0)
    squares_x = []
    squares_y = []
    x = y = 0
    for i in range(tiles_x):
        squares_x.append(int(x))
        x += tiles_sizeX
    squares_x.append(image.size[0])
    for k in range(tiles_y):
        squares_y.append(int(y))
        y += tiles_sizeY
    squares_y.append(image.size[1])
    return [squares_x, squares_y]


def prepare_set(name, mode="raster"):
    for image in os.listdir(BASE_URL + name + "/"):
        _class = image.split("-")[1][3]
        im = Image.open(BASE_URL + name + "/" + image)
        if mode is "pixels":
            features = extract_pixel_values(im)
        elif mode is "max":
            features = extract_max(im)
        elif mode is "min":
            features = extract_min(im)
        elif mode is "mean":
            features = extract_mean(im)
        elif mode is "raster":
            features = extract_black_pixel_ratio(im, return_tiles(im, 12))
        write_feature_vector(features, name, _class)


def write_feature_vector(features, name, _class):
    with open("mnist" + "." + name + ".txt", "aw") as f:
        f.write(_class + ", ")
        for feature in features:
            f.write(str(feature) + ",")
        f.write("\n")

if __name__ == "__main__":
    prepare_set("train", "mean")
    #prepare_set("test")
