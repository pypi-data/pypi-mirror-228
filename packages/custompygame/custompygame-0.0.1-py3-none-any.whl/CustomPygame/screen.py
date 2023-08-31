import pygame
from events import Event

ev = Event()


class Screen:
    def __init__(self, screen_size=(400, 400), screen_title='MyEngine`s application', screen_icon=None,
                 screen_color=(20, 40, 45), fps=60, resizable=False):
        self.screen = pygame.display.set_mode(screen_size, resizable)
        pygame.display.set_caption(screen_title)
        pygame.display.set_icon(screen_icon) if screen_icon else False
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.color = screen_color
        self.figures = []

    def update(self):
        self.screen.fill(self.color)
        ev.check_events(self.figures)
        [self.draw_figure(figure) for figure in ev.figures]
        pygame.display.update()
        self.clock.tick(self.fps)

    def draw_figure(self, figure):
        self.screen.blit(figure.get_figure(), figure.pos)

    def add_figure(self, figure):
        self.figures.append(figure)

    def delete_figure(self, figure):
        self.figures.remove(figure)
