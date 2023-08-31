import pygame

from Widgets.themes import Themes

theme = Themes()


class Combo_Box:
    def __init__(self, size=(100, 20), pos=(0, 0), text=['Box1', 'Box2'], chosen='Box1', radius=10,
                 frame=0, can_press=True, opened=False):
        self.figure_type = 'Combo Box'
        self.main_color = theme.colors[theme.color_theme]['unpressed_color']
        self.frame_color = theme.colors[theme.color_theme]['frames']
        self.text_color = theme.colors[theme.color_theme]['text']
        self.pressed_color = theme.colors[theme.color_theme]['pressed_color']
        self.aim_color = theme.colors[theme.color_theme]['aim_color']
        self.color = self.main_color
        self.font = theme.font
        self.size = size
        self.pos = pos
        self.text = text
        self.chosen = chosen
        self.radius = radius
        self.frame = frame
        self.can_press = can_press
        self.opened = opened

    def res_combo_box(self):
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
        pygame.draw.line(surface, theme.colors[theme.color_theme]['bg_color'], (self.size[0] - self.size[1], 0),
                         (self.size[0] - self.size[1], self.size[1]), 5)
        pygame.draw.lines(surface, self.text_color, False,
                          [(self.size[0] - self.size[1] + self.size[1] // 3, self.size[1] - self.size[1] // 3),
                           (self.size[0] - self.size[1] // 2, self.size[1] // 3),
                           (self.size[0] - self.size[1] // 3, self.size[1] - self.size[1] // 3)], 2)
        surface.blit(self.font.render(self.chosen, True, self.text_color),
                     (self.size[0] // 2 - self.font.render(self.chosen, True, self.text_color).get_width() // 2 -
                      self.size[1] // 2,
                      self.size[1] // 2 - self.font.render(self.chosen, True, self.text_color).get_height() // 2))
        if self.opened:
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
                             (0 + self.radius + self.frame, 0 + self.frame,
                              self.size[0] - ((self.radius + self.frame) * 2),
                              self.size[1] - (self.frame * 2)))
            pygame.draw.rect(surface, self.color, (
                0 + self.frame, 0 + self.frame + self.radius, self.radius,
                self.size[1] - ((self.frame + self.radius) * 2)))
            pygame.draw.rect(surface, self.color,
                             (0 + self.size[0] - self.radius - self.frame, 0 + self.frame + self.radius, self.radius,
                              self.size[1] - ((self.frame + self.radius) * 2)))
            pygame.draw.circle(surface, self.color, (0 + self.frame + self.radius, 0 + self.frame + self.radius),
                               self.radius)
            pygame.draw.circle(surface, self.color,
                               (0 + self.size[0] - self.radius - self.frame, 0 + self.frame + self.radius),
                               self.radius)
            pygame.draw.circle(surface, self.color,
                               (0 + self.size[0] - self.radius - self.frame,
                                0 + self.size[1] - self.radius - self.frame),
                               self.radius)
            pygame.draw.circle(surface, self.color,
                               (0 + self.frame + self.radius, 0 + self.size[1] - self.radius - self.frame), self.radius)
        return surface

    def get_figure(self):
        return self.res_combo_box()

    def get_hitbox(self):
        return pygame.Rect(*self.pos, *self.size)
