import pygame
import sys


class Button:

    color_light = (170,170,170)
    color_dark = (100,100,100)
    screen_width = None
    screen_height = None

    def __init__(self, label, screen) -> None:
        self.screen = screen
        smallfont = pygame.font.SysFont('Corbel', 35)
        self.text = smallfont.render(label , True , (170, 170, 170))
        Button.screen_width = self.screen.get_width()
        Button.screen_height = self.screen.get_height()
        self.w, self.h = 140, 40

    @property
    def xmin(self):
        return 0.8 * Button.screen_width

    @property
    def xmax(self):
        return self.xmin + self.w

    @property
    def ymin(self):
        return 0.2*Button.screen_height

    @property
    def ymax(self):
        return 0.2*Button.screen_height + self.h

    def get_bpos(self):
        mouse = pygame.mouse.get_pos()
        return self.xmin <= mouse[0] <= self.xmax and self.ymin <= mouse[1] <= self.ymax

    def draw(self):
        color = Button.color_light if self.get_bpos() else  Button.color_dark
        pygame.draw.rect(self.screen, color, [self.xmin, self.ymin, self.w, self.h])
        self.screen.blit(self.text, (self.xmin, self.ymin))


    def callback(self) -> None:
        if self.get_bpos():
            pygame.quit()


def main():
    # initializing the constructor
    pygame.init()
    
    # opens up a window
    screen = pygame.display.set_mode((720, 720))
            
    but = Button('Yo man', screen)


    while True:


        for ev in pygame.event.get():
            
            if ev.type == pygame.QUIT:
                pygame.quit()
                
            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #if the mouse is clicked on the
                # button the game is terminated
                print("YOYO")
                but.callback()
                    
        # fills the screen with a color
        screen.fill((60,25,60))
        
        but.draw()
            
        # updates the frames of the game
        pygame.display.update()

if __name__ == "__main__":
    main()

