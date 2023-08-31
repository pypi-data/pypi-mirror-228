import winreg
import pygame

pygame.init()


class Themes:
    def __init__(self, theme='system', color_theme='green', font=pygame.font.SysFont('arial', 20)):
        self.color_theme = color_theme
        self.theme = self.determine_system_color_theme() if theme == 'system' else theme
        self.colors = {'green': {'unpressed_color': (24, 80, 42), 'frames': (200, 200, 200), 'text': (220, 220, 220),
                                 'pressed_color': (10, 50, 18), 'bg_color': (20, 40, 45), 'label': (20, 40, 45),
                                 'pressed_label': (15, 30, 35), 'aim_color': (20, 70, 32)}}
        self.themes = {'dark': {'main': (43, 43, 43), 'light_text': (220, 220, 220)}}
        self.font = font

    def determine_system_color_theme(self):
        try:
            reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
            reg_key = winreg.OpenKey(reg, reg_path)
            for i in range(1024):
                value_name, value, _ = winreg.EnumValue(reg_key, i)
                if value_name == 'SystemUsesLightTheme':
                    if value == 0:
                        return 'dark'
                    else:
                        return 'white'
        except:
            return None

    def change_theme(self, color_theme=None, theme=None):
        self.color_theme = self.color_theme if not color_theme else color_theme
        self.theme = self.theme if not theme else self.determine_system_color_theme() if theme == 'system' else theme

    def add_color_theme(self, name, main_color, frames_color, darker_color):
        self.colors[str(name)] = {'main': main_color, 'frames': frames_color, 'dark': darker_color}
