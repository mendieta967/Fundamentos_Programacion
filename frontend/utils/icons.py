from pathlib import Path

import customtkinter as ctk
from PIL import Image

assets = Path(__file__).resolve().parents[1] / "assets" / "icons"


def load_icon(name, size=(18, 18)):

    image = Image.open(assets / f"{name}.png")

    return ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=size
    )