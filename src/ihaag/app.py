"""
A GUI-based cross-stitch chart generator
"""
from logging import info
from pathlib import Path

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, HIDDEN, ROW, VISIBLE

from .utils import *

SAMPLE_IMAGE = str(Path.cwd() / "test/images/smile.png")


class ihasaGUI(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        box_setup = {"style": Pack(direction=ROW, padding=5)}

        # TODO(glasnt): file selector
        self.select_input = toga.TextInput(
            placeholder="Open an image", style=Pack(flex=1, padding=5), readonly=True
        )

        select_button = toga.Button(
            "Open", on_press=self.open_image, style=Pack(padding=5)
        )

        select_box = toga.Box(**box_setup)
        select_box.add(select_button)
        select_box.add(self.select_input)

        button = toga.Button("Generate!", on_press=self.generate, style=Pack(padding=5))

        self.preview = toga.ImageView(
            id="image", style=Pack(width=60, height=60, padding=10, visibility=HIDDEN)
        )

        self.img_info = toga.TextInput(
            id="info", readonly=True, style=Pack(padding=10, visibility=VISIBLE)
        )

        info_box = toga.Box(**box_setup)
        info_box.add(self.preview)
        info_box.add(self.img_info)

        options_box = toga.Box(**box_setup)
        self.settings = build_settings()
        options_box.add(*self.settings)

        main_box.add(select_box)
        main_box.add(toga.Divider())
        main_box.add(info_box)
        main_box.add(toga.Divider())
        main_box.add(options_box)
        main_box.add(toga.Divider())
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def load_image(self, widget):
        pass

    def open_image(self, widget):
        selected = self.main_window.open_file_dialog("Select Image")
        self.select_input.value = selected
        self.preview.image = toga.images.Image(selected)
        self.preview.style.visibility = VISIBLE

        self.img_info.value = get_image_attributes(selected)
        self.img_info.style.visilbility = VISIBLE

    def generate(self, widget):
        inputs = get_settings(self.settings)
        inputs["image"] = self.select_input.value

        print(inputs)
        chart_fn = generate_chart(inputs)
        chart_url = "file://" + chart_fn
        print(chart_url)

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


def main():
    return ihasaGUI()
