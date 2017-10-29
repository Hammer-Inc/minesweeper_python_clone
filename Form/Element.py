import pygame

from manager import Manager


class Element:
    def __init__(self):
        self.surface = self.surface or None
        self.rect = self.rect or None
        self._is_down = self._is_down or False
        self._is_visible = self._is_visible or True
        self._is_enabled = self._is_enabled or True
        self._has_changes = self._has_changes or False

    def __tick__(self):
        if self._is_enabled:
            if self._is_down:
                if pygame.event.peek(pygame.MOUSEBUTTONUP):
                    if self.is_mouse_over():
                        self.on_click()
                    self._is_down = False
                    self.on_click_finish()

            elif self.is_mouse_over():
                self.on_mouse_over()
                if pygame.event.peek(pygame.MOUSEBUTTONDOWN):
                    self._is_down = True
                    self.on_click_start()
        if self.__should_render():
            self.will_render()
            self.render()
            self.did_render()
        self.post_tick()

    def __should_render(self):
        return self._has_changes and self._is_visible and self.should_render()

    def __did_render(self):
        self.did_render()
        self._has_changes = False

    def should_render(self):
        pass

    def will_render(self):
        pass

    def render(self):
        Manager.get_display().queue(self.surface, self.rect)

    def did_render(self):
        pass

    def on_click(self):
        pass

    def on_click_start(self):
        pass

    def on_click_finish(self):
        pass

    def on_mouse_over(self):
        pass

    def post_tick(self):
        pass

    def update_surface(self, new_surface):
        self.surface.blit(new_surface, (0, 0))
        self._has_changes = True

    def update_rect(self, new_rect):
        self.rect = new_rect
        self._has_changes = True

    def is_mouse_over(self):
        self.rect.collidepoint(pygame.mouse.get_pos())

    def enable(self):
        self._is_enabled = True

    def disable(self):
        self._is_enabled = False

    def show(self):
        self._is_visible = True

    def hide(self):
        self._is_visible = False

    def force_render(self):
        self._has_changes = True

