import pygame
from common import config, events, utils
from common.paths import ASSETS_PATH
from session import Session

class Dialogue():
    def __init__(self, session: Session) -> None:
        from common import paths
        from pathlib import Path
        self.dialog_list = session.dialogue_data["dialogues"]
        self.line = 0
        self.section = 0
        self.dialogue_scenes = session.dialogue_scenes
        self.dialogue_surface = pygame.surface.Surface((config.DIALOG_DISP_AREA.width, config.DIALOG_DISP_AREA.height))
        self.alpha = 0
        self.next_section_ev_posted = False
    def next_line(self):
        self.line += 1
    def set_section(self, s):
        self.section = s
        self.next_section_ev_posted = False
        self.alpha = 0
        self.line = 0
    def show(self, display, session: Session):
        
        if self.line < len(self.dialog_list[self.section]):
            from common import paths, config
            display.fill((0, 0, 0))

            section_data = self.dialog_list[self.section][self.line]
            current_bg = self.dialogue_scenes[self.section]
            if self.alpha <= 255:
                current_bg.set_alpha(self.alpha)
                self.alpha += config.TRANSISTION_SPEED * 0.5

            display.blit(current_bg, (0,0))
            self.speakerName = pygame.font.Font(config.FONT[0], config.FONT[1]).render(section_data["speaker"], True, (255, 178, 71))
            self.avatar = session.avatars[section_data["speaker"]]
            
            display.blit(self.avatar, (config.get_window_size()[0] - self.avatar.get_width(), config.get_window_size()[1] - self.avatar.get_height()))

            display.blit(self.speakerName, (config.DIALOG_DISP_AREA.left + 10, config.DIALOG_DISP_AREA.top - self.speakerName.get_height()))
            utils.drawText(
                display,
                section_data["line"], 
                (255, 255, 255),
                pygame.rect.Rect(config.DIALOG_DISP_AREA.left + 10, config.DIALOG_DISP_AREA.top + 10, config.DIALOG_DISP_AREA.width - 20, config.DIALOG_DISP_AREA.height - 20),
                pygame.font.Font(config.FONT[0], config.FONT[1]))
        else:
            if not self.next_section_ev_posted:
                pygame.event.post(pygame.event.Event(events.NEXT_DIALOG_SECTION))
                self.next_section_ev_posted = True
        
    