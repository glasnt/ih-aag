from pathlib import Path
from PIL import Image

from ih.chart import chart as ih_chart


def get_image_attributes(filename):
    """For an image, get some preview elements"""
    img = Image.open(filename)

    return f"Image: {img.width} x {img.height}"


def generate_chart(inputs):
    chart_file = ih_chart(**inputs)
    return str(Path.cwd() / chart_file)
