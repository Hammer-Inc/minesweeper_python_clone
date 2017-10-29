import Form.Button
import Form.SelectButton
import Form.TextButton
import objects
from Form import Element as utils
from main import *
from manager import Manager


class Quit(Exception):
    pass


class GameOver(Exception):
    pass


class State(object):
    BreakException = NotImplementedError
    Use__loop__ = True

    def __init__(self, *args):
        Manager.get_display().refresh()
        self.interface = {}
        self.init(*args)
        try:
            while True:
                self.loop()
                self.__loop__()
                Manager.get_display().will_render()
                Manager.get_display().clock.tick(Manager.get_setting(
                    "dsp_max_frames"))
                gc.collect()
        except self.BreakException:
            return

    def __loop__(self):
        for item in self.interface:
            if self.interface[item]['Open']:
                clickable = self.interface[item]
                for btn in clickable['Buttons']:
                    btn.will_render()
                for txt in clickable['Text']:
                    Manager.get_display().queue(*txt)
                for event in pygame.event.get(
                        [pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.QUIT]):
                    pygame.event.post(event)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if clickable['Hide']:
                            if not clickable['Base'].rect.collidepoint(
                                    pygame.mouse.get_pos()):
                                clickable['Open'] = False
                                Manager.get_display().queue(self.glo.background,
                                                            clickable[
                                                                'Base'].rect)
                                clickable['Button'].recolour(
                                    clickable['Button'].colour,
                                    clickable['Button'].showpress)
                    elif event.type == pygame.QUIT:
                        raise Quit
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if clickable['Hide']:
                            clickable['Open'] = False
                            Manager.get_display().queue(
                                Manager.get_background(),
                                clickable['Base'].rect)
                            clickable['Button'].recolour(
                                'clickable'['Button'].colour,
                                clickable['Button'].showpress)
                        else:
                            self.exit('ESC_KEY')

        pygame.event.clear()

    def init(self, *args):
        raise NotImplementedError()

    def loop(self):
        raise NotImplementedError()

    def exit(self, caller=None):
        Manager.get_display().refresh()
        raise self.BreakException


class MainMenu(State):
    game_level_presets = {
        'Easy': {'width': 10, 'height': 10, 'bombs': 10},
        'Medium': {'width': 20, 'height': 20, 'bombs': 50},
        'Hard': {'width': 30, 'height': 30, 'bombs': 400},
        'Debug': {'width': 20, 'height': 10, 'bombs': 2},
        'Custom': {'custom'}
    }

    BreakException = Quit

    def __init__(self, *args):
        self.options = {}
        super(MainMenu, self).__init__(*args)

    def init(self):
        self.options = {'width': 10, 'height': 10, 'bombs': 10}

        text_start = Manager.get_display().render("New Game", "grey", "text",
                                                  centery=70, left=10)
        text_options = Manager.get_display().render("Game Options", "grey",
                                                    "text",
                                                    centery=140, left=10)
        text_exit = Manager.get_display().render("Quit", "grey", "text",
                                                 centery=210,
                                                 left=10)

        but_start = Form.Button.Button("green", self.new_game, left=0, top=50,
                                       width=150, height=40)
        but_options = Form.Button.Button("orange", self.show_options, left=0,
                                         top=120, width=150, height=40)
        but_exit = Form.Button.Button("red", self.exit, left=0, top=190,
                                      width=150, height=40)
        side_bar = Form.Button.Button("darkgrey", lambda me: None, left=0,
                                      top=0, width=150,
                                      height=Manager.get_display().height)
        self.interface["base"] = {'Open': True,
                                  'Text': [text_start, text_options, text_exit],
                                  'Buttons': [side_bar, but_start, but_exit,
                                              but_options],
                                  'Base': side_bar,
                                  'Button': None,
                                  'Hide': False
                                  }

        # Game option menu
        title = Manager.get_display().render('Game Settings', "lightorange",
                                             "menu_title", top=50, centerx=250)

        opside_bar = Form.Button.Button("darkorange", lambda me: None, left=150,
                                        top=0, width=200,
                                        height=Manager.get_display().height)
        mclevel = Form.SelectButton.MultipleChoice(self.on_level_change, 'Difficulty',
                                                   self.game_level_presets.keys(), 0,
                                                   (175, 100))
        but_width = Form.TextButton.TextButton("Width", "lightorange", left=175,
                                               top=mclevel.rect.bottom + 20,
                                               width=30, height=10)
        but_height = Form.TextButton.TextButton("Height", "lightorange",
                                                left=205,
                                                top=mclevel.rect.bottom + 20,
                                                width=30, height=10)
        but_bombs = Form.TextButton.TextButton("Bombs", "lightorange", left=235,
                                               top=mclevel.rect.bottom + 20,
                                               width=30, height=10)
        self.interface['opmenu1'] = {'Open': False, 'Text': [title],
                                     'Buttons': [opside_bar, mclevel, but_width,
                                                 but_height, but_bombs],
                                     'Base': opside_bar, 'Button': but_options,
                                     'Hide': True}

    def loop(self):
        pass

    def new_game(self, caller=None):
        pygame.event.clear()
        GameUI(self.options)

    def show_options(self, caller=None):
        self.interface['opmenu1']['Open'] = True
        caller.recolour(self.interface['opmenu1']['Base'].colour, False)
        pygame.event.clear()

    def cgs(self, caller):
        return
        # self.options[caller.text.lower()] = tkSimpleDialog.askinteger(
        #     "Set " + caller.text, caller.text + ":",
        #     initialvalue=self.options[caller.text.lower()], minvalue=1,
        #     maxvalue=900 * (caller.text == "Bombs") + 30 * (
        #         not caller.text == "Bombs"))

    def on_level_change(self, caller, selected):
        if not selected.value == "Custom":
            self.options.update(
                self.game_level_presets[selected.value])


class GameUI(State):
    BreakException = GameOver

    def __init__(self, *args):
        self.options = None
        self.handler = None
        super(GameUI, self).__init__(*args)

    def init(self, gameOpt):
        self.interface = {}
        self.options = gameOpt
        self.handler = objects.Handler(gameOpt)

        textmenu = Manager.get_display().render("Menu", "white", "uitext",
                                                centery=10, centerx=25)
        textbombs = Manager.get_display().render(
            "Total Bombs: " + `self.options['bombs']`, "white", "uitext",
            centery=10, left=160)
        texttiles = Manager.get_display().render(
            "Tiles: " + `self.options['width'] * self.options[
                'height']`, "white", "uitext", centery=10,
            left=170 + textbombs[1].width)

        topbar = Form.Button.Button("darkgrey", lambda me: None, left=0, top=0,
                                    width=Manager.get_display().width,
                                    height=20)
        butMenu = Form.Button.Button("lightgrey", self.show_menu, left=0, top=0,
                                     width=150, height=20)

        self.interface["Base"] = {'Open': True,
                                  'Text': [textmenu, textbombs, texttiles],
                                  'Buttons': [topbar, butMenu], 'Base': topbar,
                                  'Button': None, 'Hide': False}
        # PauseMenu
        textExit = Manager.get_display().render("Quit", "grey", "text",
                                                centery=70,
                                                left=10)

        butExit = Form.Button.Button("red", self.exit, left=0, top=50,
                                     width=150, height=40)
        sidebar = Form.Button.Button("grey", lambda me: None, left=0, top=20,
                                     width=150,
                                     height=Manager.get_display().height - 20)
        self.interface["Paused"] = {'Open': False, 'Text': [textExit],
                                    'Buttons': [sidebar, butExit],
                                    'Base': sidebar,
                                    'Button': butMenu, 'Hide': True}
        Manager.get_display().fill("lightblue")

    def loop(self):
        if not self.interface['Paused']['Open']:
            self.handler.will_render()

    def show_menu(self, caller=None):
        self.interface['Paused']['Open'] = True
        caller.recolour(self.interface['Paused']['Base'].colour, False)
        pygame.event.clear()
