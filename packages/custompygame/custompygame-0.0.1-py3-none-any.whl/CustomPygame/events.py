import pygame


class Event:
    def __init__(self):
        self.figures = []

    def check_events(self, figures=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                return f'KeyboardButton: {event.key}'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if figures:
                    self.check_figure_pressed(figures)
                    break
            elif event.type == pygame.MOUSEBUTTONUP:
                if figures:
                    self.check_figure_unpressed(figures)
                    break
            elif event.type == pygame.MOUSEMOTION:
                if figures:
                    self.check_figure_on_aim(figures)
                    break
            elif event.type == pygame.VIDEORESIZE:
                return f'Resize'
            self.figures = figures

    def check_figure_pressed(self, figures):
        res_figures = []
        for figure in figures:
            if figure.can_press and figure.get_hitbox().collidepoint(pygame.mouse.get_pos()):
                figure.color = figure.pressed_color
                if figure.figure_type == 'Check_Box':
                    figure.change_status(True if not figure.active else False)
            res_figures.append(figure)
        self.return_figures_with_new_color(res_figures, figures)

    def check_figure_unpressed(self, figures):
        res_figures = []
        for figure in figures:
            figure.color = figure.main_color
            res_figures.append(figure)
        self.return_figures_with_new_color(res_figures, figures)

    def return_figures_with_new_color(self, res_figures, figures):
        if len(res_figures) >= 1:
            self.figures = res_figures
        else:
            self.figures = figures

    def check_figure_on_aim(self, figures):
        res_figures = []
        for figure in figures:
            if figure.get_hitbox().collidepoint(pygame.mouse.get_pos()) and figure.can_press:
                figure.color = figure.aim_color
            elif figure.can_press:
                figure.color = figure.main_color
            res_figures.append(figure)
        self.return_figures_with_new_color(res_figures, figures)