# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 18:46:40 2021

@author: Solymi
"""
#import glob
import re
from datetime import datetime
import subprocess
import os




resetbitfilecommand = "head -c "+str(streamlength)+" /dev/random > devrandombits.bin"
perf_bitcountstr = "perf stat -e cycles,instructions ./bitcount "

randbytes = []
rtot = []
cycles = []
instructions = []
times = []
testnames = []
bitpercycle = []
bitperinst = []
bitpersec = []

os.makedirs(directory, exist_ok=True)

dateTimestart = datetime.now()

for repeatnum in range(repeats):
    print("-----Run "+str(int(repeatnum)+1)+"/"+str(repeats)+"-----")
    
        
    #bitcount
    if dobitcount:
        print("bitcount run...")
        txtfiles = []
        randbytes = []
        cycles = []
        instructions = []
        times = []
        testnames = []
        bitpercycle = []
        bitperinst = []
        bitpersec = []
    
        if resets:
            subprocess.run(resetbitfilecommand,shell=True)
        print("Doing bitcount")
        perfrun = subprocess.run(perf_bitcountstr + inputfile,shell=True, capture_output=True, text=True, errors="ignore")
        perfrunstr = perfrun.stdout + perfrun.stderr
        print(perfrunstr)
        
        if "Error" not in perfrunstr:
            randbytes.append(streamlength*8)
            for line in perfrunstr.split('\n'):
                line = " "+line
                if "cycles:u" in line:
                    #print(re.split('\W+|\,',line.replace(",","")))
                    cycles.append(re.split('\W+|\,',line.replace(",",""))[1])
                if "instructions:u" in line:
                    #print(re.split('\W+|\,',line.replace(",","")))
                    instructions.append(re.split('\W+|\,',line.replace(",",""))[1])
                if "seconds user" in line:
                    #print(re.split('\s+',line))
                    times.append(re.split('\s+',line)[1])
            testnames.append("bitcount")
                
        #get the stats
        for i in range(len(cycles)):
            bitpercycle.append(str("{:.10f}".format(float(int(randbytes[i])/int(cycles[i])))))
            
        for i in range(len(instructions)):
            bitperinst.append(str("{:.10f}".format(float(int(randbytes[i])/int(instructions[i])))))
            
        for i in range(len(times)):
            if float(times[i]) == 0:
                print("execution time ~0, check input parameters!")
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/(float(times[i])+0.000000001))))) # to avoid div0 error for fast tests with too short sample sizes
            else:
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/float(times[i])))))
                
        res= [testnames, cycles, instructions, times, bitpercycle, bitperinst, bitpersec, randbytes]
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%b-%d-%H-%M-%S")
        
        fres = open(directory+"/"+bitcountresfile+"-"+timestampStr+resfileend, "a+")
        for i in range(len(res[0])):
            for j in range(len(res)):
                #print(res[j][i])
                fres.write(str(res[j][i])+" ")
            fres.write("\n")
        fres.close()
                       
dateTimeend = datetime.now()
print("Timespent: " + str(dateTimeend - dateTimestart))

#exec(open("getresult3.py").read())

