import os
from PIL import Image


class Features(object):

    def __init__(self, BASE_URL):
        self.BASE_URL = BASE_URL

    def extract_pixel_values(self, image):
        """Returns a feature vector containing the pixel values of the
        picture
        """
        pic = image.convert("1").load()
        features = []
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                features.append(pic[x, y]/255.0 * 1)
        return features

    def extract_max(self, image):
        """Returns a feature vector containing the max pixel values of all
        blocks of four pixels of the image.
        """
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

    def extract_min(self, image):
        """Returns a feature vector containing the min pixel values of all
        blocks of four pixels of the image.
        """
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

    def extract_mean(self, image):
        """Returns a feature vector containing the mean of pixel values of all
        blocks of four pixels of the image.
        """
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

    def extract_black_pixel_ratio(self, image, squares):
        """Returns a feature vector containing the black pixel ratio of all
        the squares of the image. The ratio is calculated as
        black_pixel/all_black_pixels.
        """
        return self.analyze_tiles(image, self.return_tiles(image, squares))

    def get_specific_feature(self, mode="raster", squares=12, folder="train"):
        """Returns the feature vector for the specified feature
        """
        features = []
        for image in os.listdir(self.BASE_URL + folder + "/"):
            class_ = image.split("-")[1][3]
            im = Image.open(self.BASE_URL + folder + "/" + image)
            if mode is "pixels":
                features.append((class_,
                                self.extract_pixel_values(im),
                                folder))
            elif mode is "max":
                features.append((class_, self.extract_max(im), folder))
            elif mode is "min":
                features.append((class_, self.extract_min(im), folder))
            elif mode is "mean":
                features.append((class_, self.extract_mean(im), folder))
            elif mode is "raster":
                features.append((class_,
                                self.extract_black_pixel_ratio(im, squares),
                                folder))
        return features

    def write_feature_vector(self, class_, features, folder, name=""):
        """Write the feature vector to a file also specifying the class"""
        if name is not "":
            name = "." + name
        fname = "mnist" + "." + folder + name + ".txt"
        with open(fname, "aw") as f:
            f.write(class_ + ", ")
            for feature in features:
                f.write(str(feature) + ",")
            f.write("\n")

    def combine_feature_vectors(self, feature_vectors):
        """Combines an arbitrary amount of feature vectors. feature_vectors
        is a list of feature vectors
        """
        folder = feature_vectors[0][0][2]
        features = []
        for i in range(len(feature_vectors[0])):
            new_feature_vector = []
            for feature_vector in feature_vectors:
                class_ = feature_vector[i][0]
                for feature in feature_vector[i][1]:
                    new_feature_vector.append(feature)
            features.append((class_, new_feature_vector, folder))
        return features

    def analyze_tiles(self, image, squares):
        """Calculate the black pixel ratio"""
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

    def return_tiles(self, image, squares):
        """Return the specified amount squares"""
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


# sample implementation
if __name__ == "__main__":
    # Provide locations of images for initialization.
    f = Features("/home/chrigu/Desktop/images/images/")
    features = f.get_specific_feature(squares=8)
    # Get the feature vector and write to file.
    for item in f.get_specific_feature(squares=8):
        f.write_feature_vector(item[0], item[1], item[2], "test")

    # Combine three feature vectors and write to file.
    f1 = f.get_specific_feature("min")
    f2 = f.get_specific_feature("max")
    f3 = f.get_specific_feature("mean")
    print f.combine_feature_vectors([f1, f2, f3])

