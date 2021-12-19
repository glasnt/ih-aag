from pathlib import Path
from PIL import Image

import click
import toga
from ih.chart import chart as ih_chart
from ih.cli import main as cli


def build_settings():
    """From the CLI inputs in ih, build toga Widgets"""
    fields = []
    defaults = {"style": toga.style.Pack(padding=3)}
    ignore = ["fileformat", "version", "image_name"]
    print(cli.params)
    for param in cli.params:
        name = param.name
        if name in ignore:
            continue

        if type(param.type) == click.types.Choice:
            fields.append(toga.Label(text=name, **defaults))
            fields.append(toga.Selection(id=name, items=param.type.choices, **defaults))
        elif type(param.type) == click.types.IntParamType:
            fields.append(toga.Label(text=name, **defaults))
            fields.append(toga.NumberInput(id=name, default=param.default, **defaults))
        elif type(param.type) == click.types.BoolParamType:
            fields.append(toga.Switch(id=name, label=name, **defaults))

    return fields


def get_settings(settings):
    """From the Toga widgets, get a dict of values"""
    inputs = {}
    for option in settings:

        if type(option.id) is str:
            if hasattr(option, "value"):
                value = option.value
            if hasattr(option, "is_on"):
                value = option.is_on

            if type(option) == toga.widgets.numberinput.NumberInput:
                value = int(value)

            inputs[option.id] = value
    inputs["palette_name"] = inputs["palette"]
    del inputs["palette"]
    return inputs


def get_image_attributes(filename):
    """For an image, get some preview elements"""
    img = Image.open(filename)

    return f"Image: {img.width} x {img.height}"


def generate_chart(inputs):
    chart_file = ih_chart(**inputs)
    return str(Path.cwd() / chart_file)
