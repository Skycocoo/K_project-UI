# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:13:39 2017

@author: medialab
@usage: data = cPickle.load(file(__processed_filename__,'rb'))
"""
from Mocam2Kinect import *
from Human_mod import *
from rawK2array import *
import cPickle
import numpy as np
import glob,os,win32com.client,pdb

src_path = os.path.dirname(os.path.abspath(__file__)) + '\\data\\'
dst_path = os.path.dirname(os.path.abspath(__file__)) + '\\processed\\'

jidx = [0, 1, 2, 3, 4, 5, 6, 8, 9 ,10, 20]

def folder_retarget(src_path,shortcut):
    shell = win32com.client.Dispatch("WScript.Shell")
    return str(shell.CreateShortCut(src_path+shortcut).Targetpath)

def process_subfolders(src_path, dst_path):
    for subfolder in os.listdir(src_path):
        for exeno in range(1, 8):
            if '.lnk' in subfolder:
                path = folder_retarget(src_path,subfolder)
                filelist = glob.glob(os.path.join(path, '*ex'+repr(exeno)+'.pkl') ) # find all pkl files
            else:
                filelist = glob.glob(os.path.join(src_path+subfolder, '*ex'+repr(exeno)+'.pkl') ) # find all pkl files
        #    pdb.set_trace()
            for infile in filelist:
                print infile
                data = cPickle.load(file(infile,'rb'))
                Kbody = rawK2ary(data,jidx)
                J     = human_mod(Kbody)

                name = infile.split('\\')[-1].split('ex')
                # if name[0].split('data')[1][0]=='1':
                #     year = '2016'
                # else:
                #     year = '2017'
                year = '2018'
                fname = dst_path+'ex'+repr(exeno)+'/' + name[0].replace('data','data'+year)+'unified_ex'+name[1]
                cPickle.dump(J,file(fname,'wb'))

def process_single_file(infile):
    jidx = [0,1,2,3,4,5,6,8,9,10,20]
    data  = cPickle.load(file(infile,'rb'))
    Kbody = rawK2ary(data,jidx)
    J     = human_mod(Kbody)
    name  = infile.split('\\')[-1].split('.pkl')
    fname = dst_path + name[0] + '_unified.pkl'
    cPickle.dump(J,file(fname,'wb'))

process_single_file(src_path + os.listdir(src_path)[0])
