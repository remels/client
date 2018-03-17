import requests
import time
import datetime

#w, h = 65, 1442;  # initialization massiv
#timeTempMas = [[0 for x in range(w)] for y in range(h)]
countMinut = 0   
countTimeTemp = 0
timePixel = 30000
timePixelSecond = 0
stringTemp = ''
cicle = 0
fromServer = 0
onLine = 0
firstMinuteSecond = ''
firstPoint = 0
stopTime = 0
temp = 0


######################################
######################################
def cicleTemp():
    
    global w
    global h
    global timeTempMas
    global countMinut
    global countTimeTemp    
    global timePixel    
    global stringTemp
    global strN
    global cicle
    global fromServer    
    global onLine
    global firstMinuteSecond
    global stopTime
    global temp
      
    stringTemp = ''
    
    try:
        tfile=open("/sys/bus/w1/devices/28-0417824691ff/w1_slave")  # read temperature
        ttext=tfile.read()
        tfile.close()
        temp=ttext.split("\n")[1].split(" ")[9]    
        temperature=int(temp[2:])/1000
        temp=int(temperature)
    except:
        pass   

    if temp <= 0:                    
        temp = 200 - (temp * 5)
    else:
        temp = temp * (-5) + 200
#####################################
    now_time = datetime.datetime.now()    #  read time
    now_date = datetime.date.today()
    
    secondPixel = now_time.second
    if secondPixel > 1:
            secondPixel = int(secondPixel / 2)            
    timePixel = (now_time.hour * 1800) + (now_time.minute * 30) + secondPixel + 50
    timePixelSecond = timePixel
#####################################
    dateNow = (str(now_date.day) + str(now_date.month) + now_time.strftime("%y") + '.txt') 
    d = open(dateNow, 'a')   
    #d.write(str(temp)+ " " + str(timePixelSecond) + " ")
    d.write(str(timePixelSecond)+ " " + str(temp) + " ")    # write to file
    d.close()           

######################################
    if onLine == 0:                   
        stringTemp = 'chek'
    else:
        f = open(dateNow, 'r')   # read from file
        myString = f.read()
        f.close()
        myMass = myString.split()        
          
        if len(myMass)<= 60:            
            stringTemp =  ' '.join(myMass)
        else:         
            for number in range(10):
                myMass.append(0)    
            ollElemets = len(myMass)/60
            if ollElemets < fromServer:
                fromServer = ollElemets
                
            i = 0
            myMassRizult = []
            for number in range(60):
                if myMass[fromServer*60 + number] == 0:
                    break
                myMassRizult.append(myMass[fromServer*60 + i])
                i+=1
                
            stringTemp =  ' '.join(myMassRizult)            
    
#########################################    
    try:
        r = requests.post("http://93.171.13.173:8080/client", stringTemp)
        fromServer = int(r.text)
        onLine = 1
        #r = requests.post("http://localhost:8080/client", stringTemp)
        #print(r.text)
        #print(stringTemp)
    except:        
        onLine = 0
        pass
    
############################################
############################################    
   

#for number in range(1000):
while 1:
    cicleTemp()
    time.sleep(2)

            

























