"""
A GUI-based cross-stitch chart generator
"""
from ctypes import alignment
from logging import disable, info
from pathlib import Path

import toga
from toga.style import Pack
from toga.style import pack
from toga.style.pack import COLUMN, HIDDEN, ROW, VISIBLE, CENTER

from .utils import *

SAMPLE_IMAGE = str(Path.cwd() / "test/images/smile.png")
PLACEHOLDER_IMAGE = str(Path.cwd() / "src/ihaag/resources/placeholder.png")


class ihasaGUI(toga.App):
    def startup(self):
        ITEM_PADDING = {"padding": 5}
        BOX_PADDING = {"padding": 10}
        HEADER_STYLE = {
            "font_size": 14,
            "font_weight": pack.BOLD,
            "padding_top": 20,
            "padding_bottom": 20,
        }

        # File Selection
        select_button = toga.Button(
            "Open Image", on_press=self.open_image, style=Pack(**ITEM_PADDING)
        )
        self.select_input = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, **ITEM_PADDING),
        )
        select_box = toga.Box(
            style=Pack(
                alignment=pack.LEFT,
                direction=ROW,
                **BOX_PADDING,
            )
        )
        select_box.add(select_button)
        select_box.add(self.select_input)

        # Preview Box
        self.preview = toga.ImageView(
            id="image",
            # image=toga.images.Image(PLACEHOLDER_IMAGE),
            style=Pack(
                background_color="#bfbdbd", flex=1, width=400, height=400, **BOX_PADDING
            ),
        )
        preview_box = toga.Box()
        preview_box.add(self.preview)

        ###

        # Options
        self.settings = build_settings(self)

        options_header = toga.Label(
            text="Options",
            style=Pack(**HEADER_STYLE),
        )
        options_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                alignment=pack.CENTER,
                flex=1,
                **BOX_PADDING,
            )
        )
        options_box.add(options_header)
        options_box.add(*self.settings)
        options_box.add(toga.Label(text="", style=Pack(width=300)))

        # Chart Info
        chart_header = toga.Label(
            text="Chart Information",
            style=Pack(**HEADER_STYLE),
        )
        self.chart_info = toga.Label(
            text="Waiting for input.",
            style=Pack(
                height=50,
                width=270,
                alignment=pack.LEFT,
            ),
        )
        self.chart_warning = toga.Label(
            text="",
            style=Pack(
                height=50,
                width=270,
                alignment=pack.LEFT,
                color="#ff0000",
                font_weight=pack.BOLD,
            ),
        )
        info_box = toga.Box(
            style=Pack(
                alignment=pack.CENTER,
                direction=COLUMN,
                flex=1,
                **BOX_PADDING,
            )
        )
        info_box.add(chart_header)
        info_box.add(self.chart_info)
        info_box.add(self.chart_warning)
        info_box.add(toga.Label(text="", style=Pack(width=300)))

        right_panel = toga.Box(style=Pack(direction=COLUMN))
        right_panel.add(options_box)
        right_panel.add(info_box)

        # Generate
        self.generate = toga.Button(
            "Generate",
            on_press=self.generate,
            style=Pack(**ITEM_PADDING),
        )
        self.chart_location = toga.Label(
            text="",
            style=Pack(flex=1, **ITEM_PADDING),
        )
        generate_box = toga.Box(
            style=Pack(
                direction=ROW,
                **BOX_PADDING,
            )
        )
        generate_box.add(self.chart_location)
        generate_box.add(self.generate)

        # Build it out.
        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.add(select_box)
        main_box.add(toga.Divider())

        middle_box = toga.Box(style=Pack(direction=ROW, **BOX_PADDING))
        middle_box.add(preview_box)
        middle_box.add(toga.Divider(direction=toga.Divider.VERTICAL))
        middle_box.add(right_panel)
        main_box.add(middle_box)

        main_box.add(toga.Divider())
        main_box.add(generate_box)

        self.main_window = toga.MainWindow(title=self.formal_name, resizeable=False)
        self.main_window.content = main_box
        self.main_window.show()

    def open_image(self, widget):
        selected = self.main_window.open_file_dialog("Select Image")
        self.select_input.value = selected
        self.preview.image = toga.images.Image(selected)

        self.get_image_attributes()

    def generate(self, widget):
        inputs = get_settings(self.settings)
        inputs["image"] = self.select_input.value
        inputs["outputfolder"] = str(Path(self.select_input.value).parent)
        print(inputs)

        chart_fn = generate_chart(inputs)
        chart_url = "file://" + chart_fn

        self.chart_location.text = f"Saved to {chart_fn} ✨"

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

        def get_scale(palette):
            """This could be improved."""
            if "wool" in palette or "alpacha" in palette:
                return 2.54 / 10
            elif "lego" in palette:
                return 0.8
            elif "perler" in palette:
                return 0.5
            else:
                return 2.54 / 14

        scale = self.scale.value
        if self.select_input.value:
            img = Image.open(self.select_input.value)
            palette = self.palette.value
            size_scale = get_scale(palette)
            scaled = int(img.height / scale), int(img.width / scale)
            sized = round(scaled[0] * size_scale, ndigits=1), round(
                scaled[1] * size_scale, ndigits=1
            )
            self.chart_info.text = (
                f"Chart will be {scaled[0]} x {scaled[1]} points\n"
                f"Approx. {sized[0]} cm x {sized[1]} cm in {palette}"
            )
            if sized[0] > 60 or sized[1] > 60:
                self.chart_warning.text = "\n⚠️ Might be a bit big. Change scale?"
            else:
                self.chart_warning.text = ""


def main():
    return ihasaGUI()
