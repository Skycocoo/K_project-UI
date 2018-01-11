from collections import defaultdict
import pygame
pygame.init()


class Exeinst(object):
    "Exercise instruxtion"
    def __init__(self):
        self.leftbnd = 0
        # self.pos = defaultdict(lambda: (0, 0))
        self.str = defaultdict(dict)
        self.words = defaultdict(list)
        self.str['exename'][1] = 'Exercise 1 : Muscle Tighting Deep Breathing\n' 
        self.str['exename'][2] = 'Exercise 2 : Clasp and Spread'\
                                 '\n  '\
                                 '\n1. Raise your hands up and hold there.'\
                                 '\n2. Wait until the sign shows "start breath in/out"'\
                                 '\n3. When breathing in, you need to close your hands.' \
                                 '\n4. When breathing out, you need to open your hands.'\
                                 '\n5. After 4 times breath in/out, put down your hands'
        self.str['exename'][3] = 'Exercise 3 : Over Head Pumping\n '
        self.str['exename'][4] = 'Exercise 4 : Push Down Pumping\n '

        self.words[1] = [word.split(' ') for word in self.str['exename'][1].splitlines()]
        self.words[2] = [word.split(' ') for word in self.str['exename'][2].splitlines()]
        self.words[3] = [word.split(' ') for word in self.str['exename'][3].splitlines()]
        self.words[4] = [word.split(' ') for word in self.str['exename'][4].splitlines()]


        self.font_size = 40
        self.font = pygame.font.SysFont('Calibri', self.font_size)
        self.space = self.font.size(' ')[0]  # The width of a space.



    def position(self, surface, ratio, stype=2):
        if stype == 2:
            self.leftbnd = int(surface.get_width()*ratio)
        else:
            self.leftbnd = int(surface.get_width()*(1-ratio))
        return (self.leftbnd, 20)      

    def blit_text(self, surface, exeno, ratio, stype, text=None):

        if text == None:
            words = self.words[exeno]
        else:
            words = [word.split(' ') for word in text.splitlines()] 
       
        if stype == 2:
            max_width = surface.get_width()*(1-ratio)
            max_height = surface.get_height()*ratio
        else:
            max_width = surface.get_width()*ratio
            max_height = surface.get_height()*(1-ratio)            

        # self.screen = pygame.display.set_mode(, pygame.RESIZABLE)

        (x, y) = self.position(surface, ratio, stype)
        x_ori, y_ori = x, y

        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, pygame.Color('green'))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width+x_ori:
                    x = x_ori  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + self.space
            x = x_ori  # Reset the x.
            y += word_height  # Start on new row.
        if y > max_height + y_ori:
            if self.font_size > 12:
                self.font_size = self.font_size - 2
                self.font = pygame.font.SysFont('Calibri', self.font_size)

class Evalinst(object):
    "Evaluation instruction"
    def _init_(self):
        self.upperbnd = 0
        self.words = defaultdict(list)

        self.font_size = 40
        self.font = pygame.font.SysFont('Calibri', self.font_size)
        self.space = self.font.size(' ')[0]

    
    def position(self, surface, ratio, stype=2):
        if stype == 2:
            self.upperbnd = int(surface.get_height()*(1-ratio))
        else:
            self.upperbnd = int(surface.get_height()*ratio)
        return (20, self.upperbnd)  

    def blit_text(self, surface, exeno, ratio, stype, text=None, color='red'):

        if text == None:
            words = self.words[exeno]
        else:
            words = [word.split(' ') for word in text.splitlines()] 
       
        if stype == 2:
            max_width = surface.get_width()*ratio
            max_height = surface.get_height()*(1-ratio)
        else:
            max_width = surface.get_width()*(1-ratio)
            max_height = surface.get_height()*ratio            

        # self.screen = pygame.display.set_mode(, pygame.RESIZABLE)

        (x, y) = self.position(surface, ratio, stype)
        x_ori, y_ori = x, y

        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, pygame.Color(color))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width+x_ori:
                    x = x_ori  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + self.space
            x = x_ori  # Reset the x.
            y += word_height  # Start on new row.
        if y > max_height + y_ori:
            if self.font_size > 12:
                self.font_size = self.font_size - 2
                self.font = pygame.font.SysFont('Calibri', self.font_size)