from Form.Button import Button
from color_palete import black
from manager import Manager


class TextButton(Button):
    def __init__(self, text, colour, on_click, show_press=0, **position_args):
        self.text = text
        Button.__init__(self, colour, on_click, show_press, **position_args)


    def redraw_buttons(self):
        Button.redraw_buttons(self)

        text = Manager.get_singleton().display.render(self.text, black,
                                                      "optionfont",
                                                      center=self.rect.center)
        self.normal.blit(*text)
        self.clicked.blit(*text)