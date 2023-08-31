import pygame
from Widgets.themes import Themes

theme = Themes()


class Check_Box:
    def __init__(self, size=None, pos=(0, 0), text='Check Box', radius=10, frame=0, active=False, can_press=True):
        self.figure_type = 'Check_Box'
        self.main_color = theme.colors[theme.color_theme]['unpressed_color']
        self.pressed_color = theme.colors[theme.color_theme]['pressed_color']
        self.aim_color = theme.colors[theme.color_theme]['aim_color']
        self.frame_color = theme.colors[theme.color_theme]['frames']
        self.text_color = theme.colors[theme.color_theme]['text']
        self.bg_color = theme.colors[theme.color_theme]['bg_color']
        self.color = self.main_color
        self.active = active
        self.font = theme.font
        self.text = self.font.render(text, True, self.text_color)
        self.size = size if size else (self.text.get_width() + self.text.get_height() + 10, self.text.get_height())
        self.pos = pos
        self.radius = radius
        self.frame = frame
        self.can_press = can_press

    def res_checkbox(self):
        surface = pygame.Surface(self.size)
        surface.fill(self.bg_color)
        cb_rad = (self.size[1] - self.frame * 2) // 2 - (self.size[1] - self.frame * 2) // 5
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
        pygame.draw.rect(surface, self.bg_color,
                         (0 + self.radius + self.frame, 0 + self.frame, self.size[0] - ((self.radius + self.frame) * 2),
                          self.size[1] - (self.frame * 2)))
        pygame.draw.rect(surface, self.bg_color, (
            0 + self.frame, 0 + self.frame + self.radius, self.radius, self.size[1] - ((self.frame + self.radius) * 2)))
        pygame.draw.rect(surface, self.bg_color,
                         (0 + self.size[0] - self.radius - self.frame, 0 + self.frame + self.radius, self.radius,
                          self.size[1] - ((self.frame + self.radius) * 2)))
        pygame.draw.circle(surface, self.bg_color, (0 + self.frame + self.radius, 0 + self.frame + self.radius),
                           self.radius)
        pygame.draw.circle(surface, self.bg_color,
                           (0 + self.size[0] - self.radius - self.frame, 0 + self.frame + self.radius),
                           self.radius)
        pygame.draw.circle(surface, self.bg_color,
                           (0 + self.size[0] - self.radius - self.frame, 0 + self.size[1] - self.radius - self.frame),
                           self.radius)
        pygame.draw.circle(surface, self.bg_color,
                           (0 + self.frame + self.radius, 0 + self.size[1] - self.radius - self.frame), self.radius)

        pygame.draw.rect(surface, self.color,
                         (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad, self.frame,
                          self.size[1] - self.frame * 2 - cb_rad * 2,
                          self.size[1] - self.frame * 2))
        pygame.draw.rect(surface, self.color, (
            self.size[0] - self.frame - (self.size[1] - self.frame * 2), self.frame + cb_rad, cb_rad,
            self.size[1] - ((cb_rad + self.frame) * 2)))
        pygame.draw.rect(surface, self.color,
                         (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + self.size[
                             1] - self.frame * 2 - cb_rad, self.frame + cb_rad, cb_rad,
                          self.size[1] - ((cb_rad + self.frame) * 2)))
        pygame.draw.circle(surface, self.color,
                           (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad, self.frame + cb_rad),
                           cb_rad)
        pygame.draw.circle(surface, self.color,
                           (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + self.size[
                               1] - self.frame * 2 - cb_rad, self.frame + cb_rad), cb_rad)
        pygame.draw.circle(surface, self.color,
                           (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + self.size[
                               1] - self.frame * 2 - cb_rad, 0 + self.size[1] - self.frame - cb_rad), cb_rad)
        pygame.draw.circle(surface, self.color,
                           (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad,
                            0 + self.size[1] - self.frame - cb_rad), cb_rad)

        cb_rad3 = cb_rad - cb_rad // 5
        pygame.draw.rect(surface, self.bg_color,
                         (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad3 + cb_rad3 // 2,
                          self.frame + cb_rad3 // 2, self.size[1] - self.frame * 2 - cb_rad3 * 2 - cb_rad3,
                          self.size[1] - self.frame * 2 - cb_rad3))
        pygame.draw.rect(surface, self.bg_color, (
            self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad3 // 2,
            self.frame + cb_rad3 + cb_rad3 // 2, cb_rad3, self.size[1] - ((cb_rad3 + self.frame) * 2) - cb_rad3))
        pygame.draw.rect(surface, self.bg_color,
                         (self.size[0] - self.frame - cb_rad3 - cb_rad3 // 2, self.frame + cb_rad3 + cb_rad3 // 2, cb_rad3,
                          self.size[1] - ((cb_rad3 + self.frame) * 2) - cb_rad3))
        pygame.draw.circle(surface, self.bg_color,
                           (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad3 + cb_rad3 // 2,
                            self.frame + cb_rad3 + cb_rad3 // 2), cb_rad3)
        pygame.draw.circle(surface, self.bg_color,
                           (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + self.size[
                               1] - self.frame * 2 - cb_rad3 - cb_rad3 // 2, self.frame + cb_rad3 + cb_rad3 // 2), cb_rad3)
        pygame.draw.circle(surface, self.bg_color,
                           (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + self.size[
                               1] - self.frame * 2 - cb_rad3 - cb_rad3 // 2,
                            0 + self.size[1] - self.frame - cb_rad3 - cb_rad3 // 2), cb_rad3)
        pygame.draw.circle(surface, self.bg_color,
                           (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad3 + cb_rad3 // 2,
                            0 + self.size[1] - self.frame - cb_rad3 - cb_rad3 // 2), cb_rad3)
        if self.active:
            cb_rad2 = cb_rad - cb_rad // 3
            pygame.draw.rect(surface, self.color,
                             (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad2 * 2, self.frame + cb_rad2,
                              self.size[1] - self.frame * 2 - cb_rad2 * 4,
                              self.size[1] - self.frame * 2 - cb_rad2 * 2))
            pygame.draw.rect(surface, self.color, (
                self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad2, self.frame + cb_rad2 * 2, cb_rad2,
                self.size[1] - self.frame * 2 - cb_rad2 * 4))
            pygame.draw.rect(surface, self.color,
                             (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + self.size[
                                 1] - self.frame * 2 - cb_rad2 * 2, self.frame + cb_rad2 * 2, cb_rad2,
                              self.size[1] - self.frame * 2 - cb_rad2 * 4))
            pygame.draw.circle(surface, self.color,
                               (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad2 * 2,
                                self.frame + cb_rad2 * 2),
                               cb_rad2)
            pygame.draw.circle(surface, self.color,
                               (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + self.size[
                                 1] - self.frame * 2 - cb_rad2 * 2, self.frame + cb_rad2 * 2), cb_rad2)
            pygame.draw.circle(surface, self.color,
                               (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + self.size[
                                 1] - self.frame * 2 - cb_rad2 * 2, 0 + self.size[1] - self.frame - cb_rad2 * 2), cb_rad2)
            pygame.draw.circle(surface, self.color,
                               (self.size[0] - self.frame - (self.size[1] - self.frame * 2) + cb_rad2 * 2,
                                0 + self.size[1] - self.frame - cb_rad2 * 2), cb_rad2)
        surface.blit(self.text, ((self.size[0] - self.size[1]) // 2 - self.text.get_width() // 2,
                                 self.size[1] // 2 - self.text.get_height() // 2))
        return surface

    def get_figure(self):
        return self.res_checkbox()

    def get_hitbox(self):
        return pygame.Rect(*self.pos, *self.size)

    def change_status(self, status):
        self.active = status
