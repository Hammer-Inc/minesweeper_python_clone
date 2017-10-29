from Form.Element import Element
from Form.TextButton import TextButton
from color_palete import black, grey
from manager import Manager


class MultipleChoice(Element):
    def __init__(self, on_change, title, options, selected_index, top_left):
        self.on_change = on_change
        self.selected = selected_index

        self.surface, self.rect = Manager.get_singleton().display.render(title,
                                                                         black,
                                                                         "optionfont", )
        self.rect.topleft = top_left

        self.options = []

        left = self.rect.right + 10
        for index in xrange(0, len(options)):
            text = options[index]
            button = MCButton(index, text, grey, top=top_left[1], left=left)
            left += button.rect.size[0] + 10
            self.options.append(button)

    def on_child_click(self, child):
        self.options[self.selected].set_enabled(True)
        self.selected = child.index
        child.set_enabled(False)
        self.on_change(caller=self, selected=child)

    def will_render(self):
        for button in self.options:
            button.update()
        Manager.get_singleton().display.queue(self.surface, self.rect)


class MCButton(TextButton):
    def __init__(self, index, text, colour, on_click, **position_args):
        TextButton.__init__(self, text, colour, on_click, **position_args)
        self.index = index
        self.value = text
