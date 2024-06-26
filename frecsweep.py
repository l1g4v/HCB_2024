import pyvisa
import time
import csv
import math

#calibration =
rm = pyvisa.ResourceManager('@ivi')
fields = ['Frecuency', 'dB','Amplitude']
data = []

#scope_rm = pyvisa.ResourceManager('@ivi')
#print(rm.list_resources())

afg = rm.open_resource('USB0::0x0699::0x0350::C012871::INSTR')
scope = rm.open_resource('USB0::0x0699::0x040C::C010822::INSTR')

print(afg.query("*IDN?"))
#print(scope.query("*IDN?"))
afg.write("SOURce1:FREQuency:FIXed 10Hz")
#afg.write("SOURce1:FREQuency:FIXed 20000Hz")
afg.write("SOURce1:FUNCtion:SHAPe SINusoid")

scope.write("MESSage:STATE ON")
scope.write('MESSage:SHOW "Adquiriendo datos"')
#scope.write('ACQUIRE:STATE ON')
scope.write('MEASUREMENT:IMMED:SOURCE CH1')
scope.write('MEASUrement:IMMed:TYPe:Amplitude')
scope.write('HORizontal:SCAle 10E-{}'.format(3))
base = abs(scope.query_ascii_values('MEASUrement:MEAS1:VALue?')[0])/2

time.sleep(1)
del afg.timeout
del scope.timeout
dep_count = 2
factor = 500
done0 = False
done1 = False
done = False
skip_step=0
for i in range(11,100011):
    if i < skip_step and done:
        continue
    else:
        done=False

    scope.write('MESSage:SHOW "Adquiriendo datos {}Hz"'.format(i))
    if i > 5000 and not done1:
        scope.write('HORizontal:SCAle 200E-6')
        done1 = True
    elif i > 1000 and not done0:
        scope.write('HORizontal:SCAle 1E-3')
        done0 = True
    
    afg.write("SOURce1:FREQuency:FIXed {}Hz".format(i))
    time.sleep(0.6)
    amp = abs(scope.query_ascii_values('MEASUrement:MEAS1:VALue?')[0])/2
    db = 10*math.log10(amp/base)
    print(amp)
    data.append([i,db,amp])
    if i >= 10000 and not done:
        skip_step = i+1000
        done = True
        continue
    if i >= 1000 and not done:
        skip_step = i+10
        done = True
        continue
    

#filename = "frecuency_inoxx_speaker_50vpp_1Mohm_045offset_10step_10cm_sensorbase_2cmwide_15height.csv"
filename="frecuency_base_speaker_2Vpp_1Mohm_044offset.csv"
# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(data)
