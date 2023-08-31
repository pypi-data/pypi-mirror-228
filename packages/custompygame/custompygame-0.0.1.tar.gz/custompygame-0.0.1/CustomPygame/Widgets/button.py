import pygame
from Widgets.themes import Themes

theme = Themes()


class Button:
    def __init__(self, size=(100, 20), pos=(0, 0), text='Button', radius=10, frame=0, can_press=True):
        self.figure_type = 'Button'
        self.main_color = theme.colors[theme.color_theme]['unpressed_color']
        self.frame_color = theme.colors[theme.color_theme]['frames']
        self.text_color = theme.colors[theme.color_theme]['text']
        self.pressed_color = theme.colors[theme.color_theme]['pressed_color']
        self.aim_color = theme.colors[theme.color_theme]['aim_color']
        self.color = self.main_color
        self.font = theme.font
        self.size = size
        self.pos = pos
        self.text = self.font.render(text, True, self.text_color)
        self.radius = radius
        self.frame = frame
        self.can_press = can_press

    def res_button(self):
        surface = pygame.Surface(self.size)
        surface.fill(theme.colors[theme.color_theme]['bg_color'])
        pygame.draw.rect(surface, self.frame_color,
                         (0 + self.radius, 0, self.size[0] - (self.radius * 2),
                          self.size[1]))
        pygame.draw.rect(surface, self.frame_color, (
            0, 0 + self.radius, self.radius, self.size[1] - (self.radius * 2)))
        pygame.draw.rect(surface, self.frame_color,
                         (0 + self.size[0] - self.radius, 0 + self.radius, self.radius,
                          self.size[1] - (self.radius * 2)))
        pygame.draw.circle(surface, self.frame_color, (0 + self.radius, 0 + self.radius),
                           self.radius)
        pygame.draw.circle(surface, self.frame_color,
                           (0 + self.size[0] - self.radius, 0 + self.radius),
                           self.radius)
        pygame.draw.circle(surface, self.frame_color,
                           (0 + self.size[0] - self.radius, 0 + self.size[1] - self.radius),
                           self.radius)
        pygame.draw.circle(surface, self.frame_color,
                           (0 + self.radius, 0 + self.size[1] - self.radius), self.radius)
        pygame.draw.rect(surface, self.color,
                         (0 + self.radius + self.frame, 0 + self.frame, self.size[0] - ((self.radius + self.frame) * 2),
                          self.size[1] - (self.frame * 2)))
        pygame.draw.rect(surface, self.color, (
            0 + self.frame, 0 + self.frame + self.radius, self.radius, self.size[1] - ((self.frame + self.radius) * 2)))
        pygame.draw.rect(surface, self.color,
                         (0 + self.size[0] - self.radius - self.frame, 0 + self.frame + self.radius, self.radius,
                          self.size[1] - ((self.frame + self.radius) * 2)))
        pygame.draw.circle(surface, self.color, (0 + self.frame + self.radius, 0 + self.frame + self.radius),
                           self.radius)
        pygame.draw.circle(surface, self.color,
                           (0 + self.size[0] - self.radius - self.frame, 0 + self.frame + self.radius),
                           self.radius)
        pygame.draw.circle(surface, self.color,
                           (0 + self.size[0] - self.radius - self.frame, 0 + self.size[1] - self.radius - self.frame),
                           self.radius)
        pygame.draw.circle(surface, self.color,
                           (0 + self.frame + self.radius, 0 + self.size[1] - self.radius - self.frame), self.radius)
        surface.blit(self.text,
                     (self.size[0] // 2 - self.text.get_width() // 2, self.size[1] // 2 - self.text.get_height() // 2))
        return surface

    def get_figure(self):
        return self.res_button()

    def get_hitbox(self):
        return pygame.Rect(*self.pos, *self.size)
