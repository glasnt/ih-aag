"""
A GUI-based cross-stitch chart generator
"""
from ctypes import alignment
from logging import info
from pathlib import Path

import toga
from toga.style import Pack
from toga.style import pack
from toga.style.pack import COLUMN, HIDDEN, ROW, VISIBLE, CENTER

from .utils import *

SAMPLE_IMAGE = str(Path.cwd() / "test/images/smile.png")
PLACEHOLDER_IMAGE = str(Path.cwd() / "src/ihaag/resources/placeholder.png")


class ihasaGUI(toga.App):
    ITEM_PADDING = 10

    def startup(self):

        header_box = toga.Box(
            style=Pack(background_color="#b1ccbe", padding=20, direction=ROW)
        )
        header_box.add(toga.Label(text="ih, by glasnt", style=Pack(font_size=24)))

        select_box = toga.Box(
            style=Pack(
                background_color="#ccc3b1", direction=ROW, padding=ihasaGUI.ITEM_PADDING
            )
        )
        self.select_input = toga.TextInput(
            placeholder="", style=Pack(flex=1, padding=5), readonly=True
        )
        select_button = toga.Button(
            "Select Image", on_press=self.open_image, style=Pack(padding=5)
        )
        select_box.add(select_button)
        select_box.add(self.select_input)

        settings_box = toga.Box(
            style=Pack(
                background_color="#ccb1c1",
                flex=1,
                direction=ROW,
                padding=ihasaGUI.ITEM_PADDING,
            )
        )

        options_box = toga.Box(
            style=Pack(
                background_color="#b9b1cc", direction=COLUMN, alignment=pack.CENTER
            )
        )
        options_box.add(
            toga.Label(
                text="Options",
                style=Pack(font_size=14, font_weight=pack.BOLD),
            )
        )
        self.settings = build_settings(self)
        options_box.add(*self.settings)

        options_box.add(toga.Divider())

        generate_box = toga.Box(
            style=Pack(background_color="#b1ccb9", direction=ROW, alignment=pack.CENTER)
        )

        self.scaled_size = toga.Label(
            text="",
            style=Pack(
                flex=1,
                width=200,
                height=40,
            ),
        )
        generate_box.add(self.scaled_size)
        self.generate = toga.Button(
            "Generate!",
            on_press=self.generate,
            style=Pack(padding=5, visibility=HIDDEN),
        )
        generate_box.add(self.generate)

        options_box.add(generate_box)

        self.chart_location = toga.Label(
            text="", style=Pack(flex=1, width=400, padding=20)
        )
        options_box.add(self.chart_location)
        settings_box.add(options_box)

        self.preview = toga.ImageView(
            id="image",
            image=toga.images.Image(PLACEHOLDER_IMAGE),
            style=Pack(
                flex=1,
                width=400,
                alignment=CENTER,
                padding=20,
            ),
        )

        settings_box.add(self.preview)

        main_box = toga.Box(style=Pack(background_color="#fbffdb", direction=COLUMN))
        main_box.add(header_box)
        main_box.add(toga.Divider())
        main_box.add(select_box)
        main_box.add(toga.Divider())
        main_box.add(settings_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def open_image(self, widget):
        selected = self.main_window.open_file_dialog("Select Image")
        self.select_input.value = selected
        self.preview.image = toga.images.Image(selected)
        self.preview.style.visibility = VISIBLE

        self.get_image_attributes()
        self.generate.style.visibility = VISIBLE

    def generate(self, widget):
        inputs = get_settings(self.settings)
        inputs["image"] = self.select_input.value

        chart_fn = generate_chart(inputs)
        chart_url = "file://" + chart_fn

        self.chart_location.text = f"Saved to {chart_fn}"

        chart_box = toga.Box(style=Pack(direction=COLUMN))
        chart_view = toga.WebView(id="preview", style=Pack(flex=1), url=chart_url)
        chart_box.add(chart_view)

        self.window = toga.Window(
            title="Generated Chart",
            position=(
                self.main_window.position[0] + 100,
                self.main_window.position[1] + 100,
            ),
        )
        self.window.app = self.app
        self.window.content = chart_box
        self.window.show()

    def get_image_attributes(self, widget=None):
        """For an image, get some preview elements"""
        print("get_image_attributes()")
        scale = self.scale.value
        if self.select_input.value:
            img = Image.open(self.select_input.value)
            self.scaled_size.text = (
                f"{int(img.height/scale)} x {int(img.width/scale)} stitches\n"
                f'({int(img.height/scale/14)}" x {int(img.width/scale/14)}" in 14 ct)'
            )


def main():
    return ihasaGUI()
