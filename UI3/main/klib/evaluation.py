import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d as gf
from collections import defaultdict
import numpy as np
from math import acos
import pygame, pdb
import pandas as pd
import os.path
from openpyxl import load_workbook

class Evaluation(object):
    def __init__(self):
        self.upperbnd = 0
        self.words = defaultdict(list)
        self.font_size = 60
        # self.font = pygame.font.SysFont('Arial', self.font_size)
        # self.space = self.font.size(' ')[0]

    def joint_angle(self, joints, idx=[0, 1, 2], offset=0):
        """ finding the angle between 3 joints.
            default joints are left shld, elbow, wrist.
        """
        if joints.shape[0] == 33:
            offset = 4
        # Elbow - sholder
        vec1 = np.array([joints[(offset+idx[1])*3+0]-joints[(offset+idx[0])*3+0],
                         joints[(offset+idx[1])*3+1]-joints[(offset+idx[0])*3+1],
                         joints[(offset+idx[1])*3+2]-joints[(offset+idx[0])*3+2]])
        # Elbow - Wrist
        vec2 = np.array([joints[(offset+idx[1])*3+0]-joints[(offset+idx[2])*3+0],
                         joints[(offset+idx[1])*3+1]-joints[(offset+idx[2])*3+1],
                         joints[(offset+idx[1])*3+2]-joints[(offset+idx[2])*3+2]])

        costheta = vec1.dot(vec2)/sum(vec1**2)**.5/sum(vec2**2)**.5
        return acos(costheta)*180/np.pi

    def breath_plot(self, ana):
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        if len(ana.hs.hstate) == 0:  # only did breathe test (i.e. exer 1)
            ax.plot(gf(ana.brth.breath_list, 5), color='g')
            if len(ana.brth.ngframe) != 0:
                for i in ana.brth.ngframe:
                    y1 = ana.brth.breath_list[i]
                    y2 = y1 - 20  
                    ax.annotate('Not deep breath', xy=(i, y1-2), xytext=(i, y2),\
                                arrowprops=dict(facecolor='red', shrink=0.05),)
            plt.title('Breath in and out')
            fig.savefig('output/Exer%s_bio_1.jpg' % str(exeno))
            plt.close(fig)
    
    def breath_hand_plot(self, ana, exeno, scale=5):
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        ax.plot(ana.hs.hstate[:, 0]*15, color='b')
        ax.plot(ana.hs.hstate[:, 1]*15-20, color='r')
        ax.plot(gf(ana.brth.breath_list, scale), color='g')
        if len(ana.brth.ngframe) != 0:
            for i in ana.brth.ngframe:
                y1 = ana.brth.breath_list[i]#/self.breath_list[0]*2
                y2 = 1.5*10
                ax.annotate('breath not deep enough', xy=(i, y1), xytext=(i, y2),\
                            arrowprops=dict(facecolor='red', shrink=0.05),)
        if len(ana.brth.missingbreath) != 0:
            for i in ana.brth.missingbreath:
                x = sum(i)/2
                y1 = ana.brth.breath_list[x]#/self.breath_list[0]*2 
                y2 = 1*10
                ax.annotate('missing breath', xy=(x, y1), xytext=(x, y2),\
                            arrowprops=dict(facecolor='green', shrink=0.05),)
        plt.title('Breath in and out & hands open and close')
        fig.savefig('output/Exer%s_biohoc_1.jpg' %str(exeno)) 
        plt.close(fig)
  

    def cutdata(self, data, length=4):
        """ if data too long (user do more than default repitition), cut it
            if data too short (user do less than default repitition), add ''
        """
        if len(data) == length:
            return data
        elif len(data) > length:
            data = data[:length]
        else:
            data = data + ['']*length-len(data)
        return data

    def run(self, exeno, ana):
        """ exercise performance evaluation
        """
        if exeno == 1 :
            self.breath_plot(ana)
            if len(ana.brth.brth_diff) == 0:
                return ['','','']
            return [min(ana.brth.brth_diff), max(ana.brth.brth_diff),
                    np.mean(ana.brth.brth_diff)]        
        elif exeno == 2:
            self.breath_hand_plot(ana)
            return [min(ana.brth.brth_diff), max(ana.brth.brth_diff), 
                    np.mean(ana.brth.brth_diff), ana.brth.sync_rate]
        elif exeno == 3:
            self.breath_hand_plot(ana, exeno, 10)
            langle = list(np.vstack([ana.dtw.Lcangle, ana.dtw.Ltangle]).T.flatten())
            rangle = list(np.vstack([ana.dtw.Rcangle, ana.dtw.Rtangle]).T.flatten())
            rangle = (rangle+['-NaN']*8)[:8]
            langle = (langle+['-NaN']*8)[:8]         
            result = rangle + [np.mean(ana.dtw.Rcangle), np.mean(ana.dtw.Rtangle)]+ langle + [np.mean(ana.dtw.Lcangle), np.mean(ana.dtw.Ltangle)]
            return result            
        elif exeno == 4:
            langle = list(np.vstack([ana.dtw.Lcangle, ana.dtw.Ltangle]).T.flatten())
            rangle = list(np.vstack([ana.dtw.Rcangle, ana.dtw.Rtangle]).T.flatten())
            return rangle + [np.mean(rangle[::2]), np.mean(rangle[1::2])]+ langle + [np.mean(langle[::2]), np.mean(langle[1::2])]
        elif exeno == 5:
            max_right = np.abs(ana.swing.angle_ini - np.min(ana.swing.min_ary[1:, 1]))
            min_right = np.abs(ana.swing.angle_ini - np.max(ana.swing.min_ary[1:, 1]))
            max_left  = np.abs(ana.swing.angle_ini - np.max(ana.swing.max_ary[1:, 1]))
            min_left  = np.abs(ana.swing.angle_ini - np.min(ana.swing.max_ary[1:, 1]))
            return [max_right, min_right, max_left, min_left]
        elif exeno == 6:
            return [max(ana.shld.dep_diff).astype(np.uint8), min(ana.shld.dep_diff).astype(np.uint8)]
        elif exeno == 7:
            max_hold  = np.max(ana.clsp.holdtime)
            min_hold  = np.min(ana.clsp.holdtime)
            mean_hold = np.mean(ana.clsp.holdtime)
            #clasp_rate = 1.*ana.clsp.claspsuc/ana.clsp.cnt
            return [max_hold, min_hold, mean_hold]
        else:
            raise ImportError('Did not define this ecercise yet.')
    def cmphist(self, log, userinfo, exeno, time, data=[]):
        """  compare user's latest data with its historical data
        """
        if not os.path.isfile('./output/compare.txt'):
            text_file = open("./output/compare.txt", "w") 
        else:
            text_file = open("./output/compare.txt", "a")
        date = '-'.join(map(str,[time.year,time.month,time.day,time.hour,time.minute]))
        str0 = '\n%10s: %s\n %10s: %s\n %10s: %s\n'% ('Exercise', exeno, 'Username', userinfo.name, 'Date', date)

        text_file.write(str0)
        print(str0)
        if os.path.isfile(log.excelPath):
            name = userinfo.name
            df = pd.read_excel(log.excelPath, sheet_name='exercise %s' %exeno)
            cols = log.colname[exeno][4:-1]  # donot neet common & errmsg info
            roi = df[df['name'] == name]  # rows of interest
            hisres = []
            terms = []
            for col in cols:
                try:
                    hisres.append(round(roi[col].mean(),2))
                    terms.append(col)
                except:
                    pdb.set_trace()
                    pass
            str1 = '%40s | %18s | %15s | %16s\n'%('Terms', 'In history record', 'This time', 'Results')
            print(str1)
            text_file.write(str1)
            for i in xrange(len(cols)):
                if hisres[i] > data[i]:
                    updown = 'decrease'
                else:
                    updown = 'increase'
                num = round(np.abs(data[i]-hisres[i])/hisres[i]*100, 2)
                str2 = '%40s | %18s | %15s | %6s%s %8s\n' %(terms[i], hisres[i], round(data[i], 2), num, '%', updown) 
                print(str2)
                text_file.write(str2)
        else:
            str1 = 'No historical data for this user.\n'
            print(str1)
            text_file.write(str1)
        text_file.close()
    def errmsg(self, errs=[], dolist=None, contents=['Breath eval', 'Hand eval', 'Exercise motion',\
                                                     'Shoulder State', 'Clasp & Spread', 'Swing']):
        """ According to the test results, showing evaluation results.
        """
        print('\nevaluation:\n')
        for idx, err in enumerate(errs):
            if len(err) != 0:
                for text in set(err):
                    print (('%18s' % contents[idx])+' : '+text)
            elif dolist[idx]:  # done without err
                print(('%18s' % contents[idx])+' : Perfect !!\n')
            else:
                pass
                #print(('%18s' % contents[idx])+' : Did not test this part.')

    def position(self, surface, ratio, stype=2, region=1, height=0):
        """According to the scene type, ratio and the region number
           set up different upper bound and lower bound to the text"""

        if stype == 2:
            self.upperbnd = int(surface.get_height()*ratio + (region-1)*height/4.)
        else:
            self.upperbnd = int(surface.get_height()*(1-ratio) + (region-1)*height/4.)
        return (20, self.upperbnd+20)

    def blit_text(self, surface, exeno, kp, text=None, region=1, emph=False, color=(107, 71, 107, 255)):
        """Creat a text surface, this surface will change according to the scene type,
           ratio and the region number. According to the size of the surface, the text 
           will auto change line also auto change size
        """
        if emph:
            self.font = pygame.font.SysFont('Bahnschrift', self.font_size, bold=True, italic=True)
        else:
            self.font = pygame.font.SysFont('Arial', self.font_size)
        self.space = self.font.size(' ')[0]
        if text == None:
            words = self.words[exeno]
        else:
            words = [word.split(' ') for word in text.splitlines()]

        if kp.scene_type == 2:
            max_width = surface.get_width()*kp.ratio
            height = surface.get_height()*(1-kp.ratio)
        else:
            max_width = surface.get_width()*(1-kp.ratio)
            height = surface.get_height()*kp.ratio
        max_height = height/4

        (x, y) = self.position(surface, kp.ratio, kp.scene_type, region, height)
        x_ori, y_ori = x, y

        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width+x_ori:  # change line(row)
                    x = x_ori  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + self.space
            x = x_ori  # Reset the x
            y += word_height  # Start on new row.
        if y > max_height + y_ori:
            if self.font_size > 12:
                self.font_size = self.font_size - 2
                if emph:
                    self.font = pygame.font.SysFont('Arial', self.font_size, bold=True, italic=True)
                else:
                    self.font = pygame.font.SysFont('Arial', self.font_size)           
                

