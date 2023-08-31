import pygame
from Widgets.themes import Themes

theme = Themes()


class Label:
    def __init__(self, size=None, pos=(0, 0), text='Label', radius=10, frame=0, can_press=False):
        self.figure_type = 'Label'
        self.frame_color = theme.colors[theme.color_theme]['frames']
        self.text_color = theme.colors[theme.color_theme]['text']
        self.main_color = theme.colors[theme.color_theme]['label']
        self.pressed_color = theme.colors[theme.color_theme]['pressed_label']
        self.aim_color = theme.colors[theme.color_theme]['aim_color']
        self.color = self.main_color
        self.font = theme.font
        self.text = theme.font.render(text, True, self.text_color)
        self.size = size if size else (self.text.get_width(), self.text.get_height())
        self.pos = pos
        self.radius = radius
        self.frame = frame
        self.can_press = can_press

    def res_label(self):
        surface = pygame.Surface(self.size)
        surface.fill(self.color)
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
        surface.blit(self.text, (self.size[0] // 2 - self.text.get_width() // 2, self.size[1] // 2 - self.text.get_height() // 2))
        return surface

    def get_figure(self):
        return self.res_label()

    def get_hitbox(self):
        return pygame.Rect(*self.pos, *self.size)

