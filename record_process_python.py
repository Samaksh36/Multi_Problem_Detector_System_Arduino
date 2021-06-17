import pyaudio
import wave
import pyfirmata
import time
import pyaudio
import wave
from playsound import playsound
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import numpy as np
from numpy import*
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

#Following is a standard code for recording. source:https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "out.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
############################### RECORDING ENDS HERE NOW WE ANALYSE



sig= wave.open(WAVE_OUTPUT_FILENAME, "r")
noisy= sig.readframes(-1)
noisy= np.frombuffer(noisy, "Int16")

sampleRate= sig.getframerate()
dt=1/sampleRate
t=np.arange(0, len(noisy)/sampleRate, dt)
print("TRYING TO EXTRACT CLEAN WAVE FROM RECORDED FILE")

plt.figure(0)
plt.title("AUDIO WAVEFILE")
plt.xlabel("TIME")
plt.plot(t, noisy,color='black')


n= len(t)
f_hat=np.fft.fft(noisy,n)
PSD= f_hat*np.conj(f_hat)/n
freq=(1/(dt*n))*np.arange(n)
L= np.arange(1,np.floor(n/2), dtype='int')

plt.figure(1)
plt.subplot(2,1,1)
plt.title("PSD")
plt.plot(freq[L], PSD[L], color='brown')


plt.subplot(2,1,2)
plt.title("PSD")
plt.xlim(3800,7200)
plt.plot(freq[L], PSD[L], color='brown')




indices= PSD>=2*100000000 #keep changing this to get smoother and smoother curve
f_hat_mod=f_hat*indices
PSD_mod= PSD*indices
ifft_sig= np.fft.ifft(f_hat_mod)

plt.figure(2)
plt.xlim(3800,7200)
plt.title("MODIFIED PSD")
plt.plot(freq[L], PSD_mod[L], color= 'brown')
'''
plt.figure(3)
plt.title("MODIFIED SIGNAL- EXTRACTED FROM NOISY")
plt.plot(t, ifft_sig, color='black')


plt.figure(4)
plt.title("MODIFIED SIGNAL- EXTRACTED FROM NOISY-ZOOMED IN")
plt.plot(t, ifft_sig, color='black')
plt.xlim(0,1/100)
plt.ylim(-1000,1000)
'''


print("_______________________________________________________________\n")
###########################################################################

#CONTROL THE PROTOCOL PART DEPENDING ON FREQUENCY
#Establish Connection With Arduino

PSD_list=[]

for x in PSD_mod[L]:
    PSD_list.append(int(x.real))

import serial                               

Arduino_Serial = serial.Serial('COM3',9600)  
print(Arduino_Serial.readline())              


    

        
    # if(x>0):
    #     pos=PSD_list.index(x)

val= max(PSD_list)
pos= PSD_list.index(val)    
print(freq[pos])   
if(3000<freq[pos]<5500):
    input_data="Low Frequency"
     

elif(5600<freq[pos]<8000):
    input_data="High Frequency"

else:
    print("No Problem")
    exit()


print()
print(input_data, "Detected")           
print("Frequency of signal: ", freq[pos])

if (input_data == "High Frequency"):               
    Arduino_Serial.write(Arduino_Serial.write(str.encode('1')))            
    print ("\nFIRE PROTOCOL ACTIVATED")
       
    
if (input_data =="Low Frequency"):                  
    Arduino_Serial.write(Arduino_Serial.write(str.encode('0')))         
    print ("\nINTRUSION PROTOCOL ACTIVATED")

print("\n_______________________________________________")

plt.show()