from xml.etree import ElementTree as xml
from xml.etree.ElementTree import ParseError


class Settings:
    def __init__(self):
        try:
            self.settings = xml.parse('settings.config')
        except ParseError:
            self.settings = xml.parse(Settings._defaults)
            self.update()

    # TODO: Remove non secure execution of eval
    def __call__(self, setting):
        return eval(self.settings.find(setting).attrib['value'])

    def update(self):
        self.settings.write('settings.config')

    _defaults = '''<Settings>
        <dsp_use_antialias value = "1"/>
        <dsp_window_height value ="500"/>
        <dsp_window_width value ="650"/>
        <dsp_screen_mode value ="0"/>
        <dsp_max_frames	value ="60"/>
        <dsp_render_res	value = "50"/>
    </Settings>'''
