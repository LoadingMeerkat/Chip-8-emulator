import pygame, sys, time
from core import Chip8


class Window:
    AUGMENTATION = 10
    period = 0.02
    Time_0 = time.time()
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((64 * self.AUGMENTATION, 32 * self.AUGMENTATION))
        pygame.display.set_caption('CHIP 8')
        self.pxarr = pygame.PixelArray(self.surface)

        self.chip = Chip8()
        self.keys = self.chip.keypad
        self.chip.load_rom('roms/Pong.ch8')
        self.videobuffer = self.chip.video
        pygame.display.update()
    
    def update(self):
        self.chip.cycle()
        self.chip.keypad = self.keys
        self.videobuffer = self.chip.video

    def draw(self):
#        x = 0
#        y = 0
#
#        for i in self.videobuffer:
#            if i == 0:
#                for j in range(self.AUGMENTATION):
#                    for k in range(self.AUGMENTATION):
#                        #print(x+j,y+k)
#                        self.pxarr[x+j,y+k] = pygame.Color((0,0,0))
#            else:
#                for j in range(self.AUGMENTATION):
#                    for k in range(self.AUGMENTATION):
#                        self.pxarr[x+j,y+k] = pygame.Color((255,255,255))
#            x += self.AUGMENTATION
#            if x == 64 * self.AUGMENTATION:
#                x  = 0
#                y += self.AUGMENTATION
        x = 0
        y = 0
        for i in self.videobuffer:
            pixel = pygame.Rect((x,y),(self.AUGMENTATION, self.AUGMENTATION))
            if i == 0:
                pygame.draw.rect(self.surface, (0,0,0), pixel)
            else:
                pygame.draw.rect(self.surface, (255,255,255),pixel)
            x += self.AUGMENTATION
            if x == 64 * self.AUGMENTATION:
                x = 0
                y += self.AUGMENTATION
        pygame.display.update()

    def processInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                self.keys[0] = 1
            elif event.key == pygame.K_1:
                self.keys[1] = 1
            elif event.key == pygame.K_2:
                self.keys[2] = 1
            elif event.key == pygame.K_3:
                self.keys[3] = 1
            elif event.key == pygame.K_4:
                self.keys[4] = 1
            elif event.key == pygame.K_q:
                self.keys[5] = 1
            elif event.key == pygame.K_w:
                self.keys[6] = 1
            elif event.key == pygame.K_e:
                self.keys[7] = 1
            elif event.key == pygame.K_r:
                self.keys[8] = 1
            elif event.key == pygame.K_a:
                self.keys[9] = 1
            elif event.key == pygame.K_s:
                self.keys[0xA] = 1
            elif event.key == pygame.K_d:
                self.keys[0xB] = 1
            elif event.key == pygame.K_f:
                self.keys[0xC] = 1
            elif event.key == pygame.K_z:
                self.keys[0xD] = 1
            elif event.key == pygame.K_c:
                self.keys[0xE] = 1
            elif event.key == pygame.K_v:
                self.keys[0xF] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                self.keys[0] = 0
            elif event.key == pygame.K_1:
                self.keys[1] = 0
            elif event.key == pygame.K_2:
                self.keys[2] = 0
            elif event.key == pygame.K_3:
                self.keys[3] = 0
            elif event.key == pygame.K_4:
                self.keys[4] = 0
            elif event.key == pygame.K_q:
                self.keys[5] = 0
            elif event.key == pygame.K_w:
                self.keys[6] = 0
            elif event.key == pygame.K_e:
                self.keys[7] = 0
            elif event.key == pygame.K_r:
                self.keys[8] = 0
            elif event.key == pygame.K_a:
                self.keys[9] = 0
            elif event.key == pygame.K_s:
                self.keys[0xA] = 0
            elif event.key == pygame.K_d:
                self.keys[0xB] = 0
            elif event.key == pygame.K_f:
                self.keys[0xC] = 0
            elif event.key == pygame.K_z:
                self.keys[0xD] = 0
            elif event.key == pygame.K_c:
                self.keys[0xE] = 0
            elif event.key == pygame.K_v:
                self.keys[0xF] = 0

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.processInput(event)
            current_time = time.time()
            if current_time - self.Time_0 > period:
                self.Time_0 = current_time
                self.update()
                self.draw()

Display = Window()
Display.main_loop()


