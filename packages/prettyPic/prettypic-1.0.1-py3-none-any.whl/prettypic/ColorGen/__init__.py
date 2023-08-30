from PIL import Image
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def initial_filters(df):
    rows_to_drop = []
    for index, row in df.iterrows():
        if row["r"] < 90 and row["g"] < 90 and row["b"] < 90:
            rows_to_drop.append(index)
        elif row["r"] > 170 and row["g"] > 170 and row["b"] > 170:
            rows_to_drop.append(index)
    filtered_df = df.drop(rows_to_drop)
    return filtered_df


class ColorGenerator:
    def __init__(self, imagePath, initial_filters=initial_filters):
        self.imagePath = imagePath
        self.image = Image.open(imagePath)
        self.imageWidth, self.imageHeight = self.image.size
        self.imagePixels = self.image.load()
        rgb = list(self.image.getdata())
        self.dataframe = initial_filters(pd.DataFrame([
            {"r": pixel[0], "g": pixel[1], "b": pixel[2]} for pixel in list(self.image.getdata())
        ]))
        self.ks = None

    def normalize(self):
        scaler = StandardScaler()
        scale = scaler.fit_transform(self.dataframe)
        self.dataframe = pd.DataFrame([
            {"r": pixel[0], "g": pixel[1], "b": pixel[2]} for pixel in list(scale)
        ])

    def kmeans_df(self, k):
        kmeans = KMeans(n_clusters=k, n_init="auto")
        kmeans.fit(self.dataframe)
        ks = []
        for i in kmeans.labels_:
            if i not in ks:
                ks.append(i)
        self.ks = ks
        self.dataframe["cluster"] = kmeans.labels_
        return self.dataframe

    def find_densist_scale(self):
        largest_set = {
            "cluster": None,
            "size": 0
        }
        for k in self.ks:
            if largest_set["size"] < len(self.dataframe[self.dataframe["cluster"] == k]):
                largest_set["cluster"] = k
                largest_set["size"] = len(
                    self.dataframe[self.dataframe["cluster"] == k])
        self.densist_scale = largest_set["cluster"]
        return largest_set["cluster"]

    def use_densist_color(self):
        cluster = self.find_densist_scale()
        filtered = self.dataframe[self.dataframe["cluster"] == cluster]
        filtered = filtered.drop(columns=["cluster"])
        r, g, b = round(filtered["r"].mean(
        )), round(filtered["g"].mean()), round(filtered["b"].mean())
        self.color_as_image = Image.new(
            "RGB", (self.imageWidth, self.imageHeight), (r, g, b))
        self.color_as_RGB = f"rgb({r},{g},{b})"
        self.color = (r, g, b)
        return (r, g, b)


def color_from_image(imagePath):
    """Turns an image into a plain color

    Parameters
    ----------
    imagePath : str
        path to the image

    Returns
    -------
    ColorGenerator
        ColorGenerator object with the following attributes:
            - color
            - color_as_image
            - color_as_RGB
    """
    colorGen = ColorGenerator(imagePath)
    colorGen.normalize()
    colorGen.kmeans_df(4)
    colorGen.use_densist_color()
    return colorGen
