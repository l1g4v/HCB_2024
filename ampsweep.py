import pyvisa
import time
import csv
rm = pyvisa.ResourceManager('@ivi')
fields = ['Source1 G', 'output G']
data = []

#scope_rm = pyvisa.ResourceManager('@ivi')
#print(rm.list_resources())
def gs(volt):
    return 0.77*volt
    
afg = rm.open_resource('USB0::0x0699::0x0350::C012871::INSTR')
scope = rm.open_resource('USB0::0x0699::0x040C::C010822::INSTR')

print(afg.query("*IDN?"))
print(scope.query("*IDN?"))

del afg.timeout
del scope.timeout

afg.write("SOURce1:FREQuency:FIXed 100Hz")
afg.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 1V")
afg.write("SOURce1:FUNCtion:SHAPe SINusoid")

scope.write("MESSage:STATE ON")
scope.write('MESSage:SHOW "Adquiriendo datos"')
#scope.write('ACQUIRE:STATE ON')
scope.write('MEASUREMENT:IMMED:SOURCE CH1')
scope.write('MEASUrement:IMMed:TYPe:MAXimum')
scope.write('HORizontal:SCAle 10E-{}'.format(3))
time.sleep(1)
afg.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 0.01Vpp")
volt = 0.00
for i in range(1,42):
    time.sleep(0.1)
    afg.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {}Vpp".format(round(volt,2)))
    scope.write('MESSage:SHOW "Adquiriendo datos {}V"'.format(round(volt,2)))
    volt = round(volt + 0.5,2)
    time.sleep(3)
    val = (scope.query_ascii_values('MEASUrement:MEAS1:VALue?')[0]/2)/0.15 
    print(val)
    data.append([gs(volt),val])

time.sleep(1) 
afg.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 0.01Vpp")
filename = "lineality_base_speaker_20vpp_1Mohm_0.5step.csv"
 
# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(data)
