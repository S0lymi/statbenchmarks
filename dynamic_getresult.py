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


uteststreamlength = streamlength
stsstreamlength = streamlength

resetbitfilecommand = "head -c "+str(streamlength)+" /dev/random > devrandombits.bin"
perf_dieharderstr = ["perf stat -e cycles,instructions dieharder -d "," -g 201 -f "+inputfile+" -D 0 -D 16384 -m "]
perf_uteststr = "perf stat -e cycles,instructions utest/Utest "+inputfile+" "
perf_stsstr = "perf stat -e cycles,instructions ./stsassess "+str(stsstreamlength)+" "+inputfile+" "
perf_entstr = "perf stat -e cycles,instructions ./ent -c "

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
    #dieharder
    if dodieharder:
        
        randbytes = []
        rtot = []
        cycles = []
        instructions = []
        times = []
        testnames = []
        bitpercycle = []
        bitperinst = []
        bitpersec = []
        
        print("Dieharder runs...")
    
        if resets:
            subprocess.run(resetbitfilecommand,shell=True)
        for params in dieharderparams:
            params1 = params[1]
            if dieharderparam2:
                params1 = dieharderparam2
            print(str(params[0])+" " + str(params1))
            #perfrun = subprocess.run(perf_dieharderstr[0]+str(params[0])+perf_dieharderstr[1]+str(params[1]),shell=True, capture_output=True, text=True)
            perfrun = subprocess.run(perf_dieharderstr[0]+str(params[0])+perf_dieharderstr[1]+str(int(params1)),shell=True, capture_output=True, text=True)
            perfrunstr = perfrun.stdout + perfrun.stderr
            if print_console_out:
                print(perfrunstr)
            
            if "Error" not in perfrunstr:            
                for line in perfrunstr.split('\n'):
                    line = " "+line
                    if "#Randbytes" in line:
                        randbytes.append(re.split('\W+',line)[2])
                        #print(file)
                        #print(re.split('\W+',line)[2])
                        rtot.append(re.split('\W+',line)[4])
                        #print(re.split('\W+',line)[4])
                    if "cycles:u" in line:
                        #print(re.split('\W+|\,',line.replace(",","")))
                        cycles.append(re.split('\W+|\,',line.replace(",",""))[1])
                    if "instructions:u" in line:
                        #print(re.split('\W+|\,',line.replace(",","")))
                        instructions.append(re.split('\W+|\,',line.replace(",",""))[1])
                    if "seconds user" in line:
                        #print(re.split('\s+',line))
                        times.append(re.split('\s+',line)[1])
                testnames.append("dieharder_"+str(params[0]))
        #get the stats
        for i in range(len(cycles)):
            bitpercycle.append(str("{:.10f}".format(float(int(randbytes[i])/int(cycles[i])))))
            
        for i in range(len(instructions)):
            bitperinst.append(str("{:.10f}".format(float(int(randbytes[i])/int(instructions[i])))))
            
        for i in range(len(times)):
            if float(times[i]) == 0:
                print("execution time ~0, check input parameters! (case "+str(i)+")!!")
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/(float(times[i])+0.000000001))))) # to avoid div0 error for fast tests with too short sample sizes
            else:
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/float(times[i])))))
                
        res= [testnames, cycles, instructions, times, bitpercycle, bitperinst, bitpersec, randbytes, rtot]
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%b-%d-%H-%M-%S")
        
        fres = open(directory+"/"+diehardresfile+"-"+timestampStr+resfileend, "a+")
        for i in range(len(res[0])):
            for j in range(len(res)):
                #print(res[j][i])
                fres.write(str(res[j][i])+" ")
            fres.write("\n")
        fres.close()
    
    #utest
    if doutest:
        print("Utest runs...")
    
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
        for params in utestparams:
            print(params)
            perfrun = subprocess.run(perf_uteststr + str(params) + " " + str(uteststreamlength),shell=True, capture_output=True, text=True)
            perfrunstr = perfrun.stdout + perfrun.stderr
            if print_console_out:
                print(perfrunstr)
    
            bits = 0
            for line in perfrunstr.split('\n'):
                line = " "+line
                if "bits have been read" in line:
                    bits += int(re.split('\W+',line)[1])
                    #randbytes.append(re.split('\W+',line)[2])
                    #print(re.split('\W+',line)[1])
                    #rtot.append(re.split('\W+',line)[4])
                    #print(re.split('\W+',line)[4])
                if "cycles:u" in line:
                    #print(re.split('\W+|\,',line.replace(",","")))
                    cycles.append(re.split('\W+|\,',line.replace(",",""))[1])
                if "instructions:u" in line:
                    #print(re.split('\W+|\,',line.replace(",","")))
                    instructions.append(re.split('\W+|\,',line.replace(",",""))[1])
                if "seconds user" in line:
                    #print(re.split('\s+',line))
                    times.append(re.split('\s+',line)[1])
            randbytes.append(bits)
            testnames.append("utest_"+str(params))
        #get the stats
        for i in range(len(cycles)):
            bitpercycle.append(str("{:.10f}".format(float(int(randbytes[i])/int(cycles[i]))))) 
        for i in range(len(instructions)):
            bitperinst.append(str("{:.10f}".format(float(int(randbytes[i])/int(instructions[i])))))
        for i in range(len(times)):
            if float(times[i]) == 0:
                print("execution time ~0, check input parameters! (case "+str(i)+")!!")
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/(float(times[i])+0.000000001))))) # to avoid div0 error for fast tests with too short sample sizes
            else:
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/float(times[i])))))  
        res= [testnames, cycles, instructions, times, bitpercycle, bitperinst, bitpersec, randbytes]
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%b-%d-%H-%M-%S")
        fres = open(directory+"/"+utestresfile+"-"+timestampStr+resfileend, "a+")
        for i in range(len(res[0])):
            for j in range(len(res)):
                #print(res[j][i])
                fres.write(str(res[j][i])+" ")
            fres.write("\n")
        fres.close()
        
#split up repeats
#for repeatnum in range(repeats):
#    print("-----Run "+str(int(repeatnum)+1)+"/"+str(repeats)+"-----")    
    #sts
    if dosts:
        print("STS runs...")
        
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
        
        os.chdir(stsdir) #change wdir to run stsassess
            
        for params in stsparams:
            print(params)
            perfrun = subprocess.run(perf_stsstr + str(params)+" "+str(stsbitstreams),shell=True, capture_output=True, text=True)
            perfrunstr = perfrun.stdout + perfrun.stderr
            if print_console_out:
                print(perfrunstr)
            bits = 0
            for line in open(stsfreqfile):
                    if "BITSREAD" in line:
                        bits+= int(re.split('\W+',line)[2])
                        #print(re.split('\W+',line)[2])
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
            randbytes.append(bits)
            testnames.append("sts_"+str(params))
        #get the stats    
        for i in range(len(cycles)):
            bitpercycle.append(str("{:.10f}".format(float(int(randbytes[i])/int(cycles[i])))))
            
        for i in range(len(instructions)):
            bitperinst.append(str("{:.10f}".format(float(int(randbytes[i])/int(instructions[i])))))
            
        for i in range(len(times)):
            if float(times[i]) == 0:
                print("execution time ~0, check input parameters! (case "+str(i)+")!!")
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/(float(times[i])+0.000000001))))) # to avoid div0 error for fast tests with too short sample sizes
            else:
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/float(times[i])))))
            
        res= [testnames, cycles, instructions, times, bitpercycle, bitperinst, bitpersec, randbytes]
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%b-%d-%H-%M-%S")
        
        os.chdir("..") #change back wdir
        
        fres = open(directory+"/"+stsresfile+"-"+timestampStr+resfileend, "a+")
        for i in range(len(res[0])):
            for j in range(len(res)):
                #print(res[j][i])
                fres.write(str(res[j][i])+" ")
            fres.write("\n")
        fres.close()
        
    #ent
    if doent:
        print("ENT run...")
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
        for entrun in range(2):
            if entrun == 0:
                print("Doing bytes")
                perfrun = subprocess.run(perf_entstr + inputfile,shell=True, capture_output=True, text=True, errors="ignore")
            if entrun == 1:
                print("Doing bits")
                perfrun = subprocess.run(str(perf_entstr) + "-b "+inputfile,shell=True, capture_output=True, text=True, errors="ignore")
            perfrunstr = perfrun.stdout + perfrun.stderr
            if print_console_out:
                print(perfrunstr)
            
            if "Error" not in perfrunstr:            
                for line in perfrunstr.split('\n'):
                    line = " "+line
                    if "Total:" in line:
                        if entrun == 0:
                            randbytes.append(int(re.split('\W+',line)[2]))
                        if entrun == 1:
                            randbytes.append(int(int(re.split('\W+',line)[2])/8))
                        #print(file)
                        #print(re.split('\W+',line))
                    if "cycles:u" in line:
                        #print(re.split('\W+|\,',line.replace(",","")))
                        cycles.append(re.split('\W+|\,',line.replace(",",""))[1])
                    if "instructions:u" in line:
                        #print(re.split('\W+|\,',line.replace(",","")))
                        instructions.append(re.split('\W+|\,',line.replace(",",""))[1])
                    if "seconds user" in line:
                        #print(re.split('\s+',line))
                        times.append(re.split('\s+',line)[1])
                if entrun == 0:
                    testnames.append("ent_byte")
                if entrun == 1:
                    testnames.append("ent_bit")
                
        #get the stats
        for i in range(len(cycles)):
            bitpercycle.append(str("{:.10f}".format(float(int(randbytes[i])/int(cycles[i])))))
            
        for i in range(len(instructions)):
            bitperinst.append(str("{:.10f}".format(float(int(randbytes[i])/int(instructions[i])))))
            
        for i in range(len(times)):
            if float(times[i]) == 0:
                print("execution time ~0, check input parameters! (case "+str(i)+")!!")
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/(float(times[i])+0.000000001))))) # to avoid div0 error for fast tests with too short sample sizes
            else:
                bitpersec.append(str("{:.10f}".format(float(int(randbytes[i])/float(times[i])))))
                
        res= [testnames, cycles, instructions, times, bitpercycle, bitperinst, bitpersec, randbytes]
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%b-%d-%H-%M-%S")
        
        fres = open(directory+"/"+entresfile+"-"+timestampStr+resfileend, "a+")
        for i in range(len(res[0])):
            for j in range(len(res)):
                #print(res[j][i])
                fres.write(str(res[j][i])+" ")
            fres.write("\n")
        fres.close()
                       
dateTimeend = datetime.now()
print("Timespent: " + str(dateTimeend - dateTimestart))

#exec(open("getresult3.py").read())

