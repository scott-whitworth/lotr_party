#

# Respond to incoming serial connections
# Plays corresponding sounds

import serial # Be able to read the serial port
#pip3 install pyserial

#SRC: https://stackoverflow.com/questions/17657103/play-wav-file-in-python
import pyaudio
import wave
#pip3 install pyaudio
#pip3 install wave

serialPort = "COM3"


#TODO: it is probably possible to overlap this if we are careful in the main loop

#WAV file Play
def playFile(audioFile, curStream):
    #Open the wave file:
    curfile = wave.open(audioFile,"rb")

    chunk = 1024

    #read data  
    data = curfile.readframes(chunk)  
  
    #play stream  
    while data:  
        curStream.write(data)  
        data = curfile.readframes(chunk)  
  
    #stop stream  
    #curStream.stop_stream()  
    #curStream.close() 

    return


print("Potatoes Python Code")

#Serial Port Set Up
print("Opening Port...")
serIn = serial.Serial(serialPort,115200, timeout=0.5) #TODO: Not sure what I want to do with this timeout
print("Opened port: " + serIn.name)


#PyAudio Setup
#open a wav format music  
curfile = wave.open("../sound/what_we_need_is_a_few_good_taters.wav","rb")  
#instantiate PyAudio  
pa = pyaudio.PyAudio()  
#open stream  
stream = pa.open(format = pa.get_format_from_width(curfile.getsampwidth()),  
                channels = curfile.getnchannels(),  
                rate = curfile.getframerate(),  
                output = True) 

# Infinite loop (ctrl+C to close)
while True:
    curLine = serIn.readline().decode("utf-8") #Grab the line from serial and decode to string

    if(len(curLine) > 0):
        print("CurrentLine: " + curLine)
        if(curLine[0:3] == "CAP"): # Check to see if the message is a Capacitive touch message (the debug messages won't fit this)
            curCap = curLine[4] #Grab just the index (will only work for one-digit numbers)
            #Match to the correct index
            match curCap:
                case '0':
                    print("Zero")
                    playFile("../sound/what_we_need_is_a_few_good_taters.wav",stream)
                case '1':
                    print("One")
                    playFile("../sound/boil_em.wav",stream)
                case '2':
                    print("Two")
                    playFile("../sound/mash_em.wav",stream)
                case '3':
                    print("Three")
                    playFile("../sound/only_one_way_to_eat.wav",stream)
                case '4':
                    print("Four")
                    playFile("../sound/potatoes.wav",stream)
                case '5':
                    print("Five")
                    playFile("../sound/stick_em_in_a_stew.wav",stream)
                case '6':
                    print("Six")
                    playFile("../sound/what_taters_precious.wav",stream)
                case _:
                    print("Match Error on " + curCap)
        else :
            print("Error on: " + curLine[0:3])
    

