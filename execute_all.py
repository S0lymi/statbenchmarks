#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 19:45:48 2021

@author: slab
"""

from datetime import datetime

import os


dateTimestart1 = datetime.now()

#general setup

dodieharder = 0
doutest = 0
dosts = 0
doent = 0
dobitcount = 0

resets = 1 #reset random file after each run by default
repeats = 20 # run each case 20 times by default

streamlength = 10000000000 #use 10GB random file by default

resfileend = ".res" #default resorce file extension

print_console_out = 0 #debug

#default names and paths for tests
stsdir = "sts-2.1.2"
diehardresfile = "diehardres"
utestresfile = "utestres"
stsresfile = "stsres"
stsfreqfile = "experiments/AlgorithmTesting/freq.txt"
entresfile = "entres"
bitcountresfile = "bitcountres"

dieharderparam2 = 10 #overwrite -m to this for all dieharder cases (set to 0 to deactivate)
#set custom parameter for each dieharder case here if dieharderparam2 is 0
dieharderparams = [(0,100),(1,100),(2,100), (3, 100), (4, 100), (5, 100), (6, 100), (7, 100), (8, 100), (9, 100), (10, 100), (11, 100), (12, 100), (13, 100), (14, 100), (15, 100), (16, 100), (17, 100), (100, 100), (101, 100), (102, 100), (200, 100), (201, 100), (202, 100), (203, 100), (204, 100), (205, 100), (206, 100), (207, 100), (208, 100), (209, 100)]
utestparams = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] #utest cases to run
stsparams = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] #sts cases to run
stsbitstreams = 5 # bitstream number to pass to sts

inputfile = os.getcwd() + "/devrandombits.bin" #location of the random file.

#bitcount tests
#10G
streamlength = 10000000000
directory = "scriptres_bitcount_20_10G"
dobitcount = 1
exec(open("dynamic_getbitcountresult.py").read())
#100M
streamlength = 100000000
directory = "scriptres_bitcount_20_100M"
dobitcount = 1
exec(open("dynamic_getbitcountresult.py").read())
#10M
streamlength = 10000000
directory = "scriptres_bitcount_20_10M"
dobitcount = 1
exec(open("dynamic_getbitcountresult.py").read())
#resets
dobitcount = 0
streamlength = 10000000000

#testu01
#10G
streamlength = 10000000000
directory = "scriptres_utest_20_10G"
doutest = 1
exec(open("dynamic_getresult.py").read())
#100M
streamlength = 100000000
directory = "scriptres_utest_20_100M"
doutest = 1
exec(open("dynamic_getresult.py").read())
#10M
streamlength = 10000000
directory = "scriptres_utest_20_10M"
doutest = 1
exec(open("dynamic_getresult.py").read())
#resets
doutest = 0
streamlength = 10000000000

#sts
#10G
streamlength = 10000000000
directory = "scriptres_sts_20_10G"
dosts = 1
exec(open("dynamic_getresult.py").read())
#100M
streamlength = 100000000
directory = "scriptres_sts_20_100M"
dosts = 1
exec(open("dynamic_getresult.py").read())
#10M
streamlength = 10000000
directory = "scriptres_sts_20_10M"
dosts = 1
exec(open("dynamic_getresult.py").read())
#resets
dosts = 0
streamlength = 10000000000

#ent
#10G
streamlength = 10000000000
directory = "scriptres_ent_20_10G"
doent = 1
exec(open("dynamic_getresult.py").read())
#100M
streamlength = 100000000
directory = "scriptres_ent_20_100M"
doent = 1
exec(open("dynamic_getresult.py").read())
#10M
streamlength = 10000000
directory = "scriptres_ent_20_10M"
doent = 1
exec(open("dynamic_getresult.py").read())
#resets
doent = 0
streamlength = 10000000000

#dieharder
#m1
streamlength = 10000000000
directory = "scriptres_dieharder_20_1"
dieharderparam2 = 1
dodieharder = 1
#m10
streamlength = 10000000000
directory = "scriptres_dieharder_20_10"
dieharderparam2 = 10
dodieharder = 1
#resets
dodieharder = 0

dateTimeend = datetime.now()
print("Timespent: " + str(dateTimeend - dateTimestart1))