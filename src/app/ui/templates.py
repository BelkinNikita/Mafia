from kivy.metrics import sp
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.button import Button


def make_label(text, size=18, height=dp(45)):
    return Label(
        text=text,
        font_size=sp(size),
        size_hint_y=None,
        height=height,
        halign="center",
        valign="middle",
    )

def make_button(text, callback, height=dp(48)):
    button = Button(
        text=text,
        font_size=sp(16),
        size_hint_y=None,
        height=height,
        background_normal="",
        background_color=(0.20, 0.30, 0.48, 1),
        color=(1, 1, 1, 1)
    )
    button.bind(on_release=callback)
    return button