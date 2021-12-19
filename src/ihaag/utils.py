from pathlib import Path
from PIL import Image
from itertools import chain
import click
import toga
from ih.chart import chart as ih_chart
from ih.cli import main as cli

from toga.style import Pack
from toga.style import pack


def build_settings(self):
    """From the CLI inputs in ih, build toga Widgets"""

    PADDING = 5
    LEFT_ELEMENT = {"style": Pack(width=100, padding=PADDING, alignment=pack.RIGHT)}
    RIGHT_ELEMENT = {"style": Pack(width=100, padding=PADDING)}

    boxes = []
    ignore = ["fileformat", "version", "image_name"]

    for param in cli.params:
        fields = []
        name = param.name
        if name in ignore:
            continue

        if type(param.type) == click.types.Choice:
            fields.append(toga.Label(text=name, **LEFT_ELEMENT))
            fields.append(
                toga.Selection(
                    id=name,
                    items=param.type.choices,
                    **RIGHT_ELEMENT,
                )
            )
        elif type(param.type) == click.types.IntParamType:
            fields.append(toga.Label(text=name, **LEFT_ELEMENT))
            myfield = toga.NumberInput(
                id=name,
                default=param.default,
                **RIGHT_ELEMENT,
            )

            # Scale is important for later
            if myfield.id == "scale":
                self.scale = myfield
                self.scale.on_change = self.get_image_attributes

            self.scale.min_value = 1
            self.scale.max_value = 1000

            fields.append(myfield)
        elif type(param.type) == click.types.BoolParamType:
            fields.append(toga.Label(text="", **LEFT_ELEMENT))
            fields.append(toga.Switch(id=name, label=name, **RIGHT_ELEMENT))

        box = toga.Box(style=Pack(direction=toga.style.pack.ROW, flex=1))
        box.add(*fields)
        boxes.append(box)
    return boxes


def get_settings(boxes):
    """From the Toga widgets, get a dict of values"""
    inputs = {}
    print(boxes)
    for options in boxes:
        for option in options.children:
            if type(option.id) is str:
                if hasattr(option, "value"):
                    value = option.value
                if hasattr(option, "is_on"):
                    value = option.is_on

                if type(option) == toga.widgets.numberinput.NumberInput:
                    value = int(value)

                inputs[option.id] = value
    print(inputs)
    inputs["palette_name"] = inputs["palette"]
    del inputs["palette"]
    return inputs


def generate_chart(inputs):
    chart_file = ih_chart(**inputs)
    return str(Path.cwd() / chart_file)
