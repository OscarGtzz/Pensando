"""
Created on Tue Jul  6 12:27:29 2021

@author: oscar
"""

import serial
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading  
import pandas as pd


def Lectura():
    def run():
        global switch
        global i
        global df
        global titulo
        arduinostring=arduino.readline()
     
        if (i == 0):
            titulo = nombre.get() + ".csv"
            df = pd.DataFrame(columns = ["GyX","GyY","GyZ","AcX","AcY","AcZ","FSR","Estado"])
            df.to_csv(titulo, index=False)

        while True:
            while (arduino.inWaiting()==0 & switch == True):
                pass

            arduinostring=arduino.readline()
            arduinostring=str(arduinostring.decode().strip('\r\n'))
            dataArray=arduinostring.split(',') 
            index = len(df.index)
            print (dataArray)
           
            df.loc [index] = [
                dataArray[0],
                dataArray[1],
                dataArray[2],
                dataArray[3],
                dataArray[4],
                dataArray[5],
                dataArray[6],
                Estadoactual]
            #print (df)
            df.loc[index:].to_csv(titulo, index= False, mode='a', header=False) 
            
            Graficar(dataArray[0], dataArray[1], dataArray[2], dataArray[3], dataArray[4], dataArray[5],dataArray[6])

            
            if switch == False:  
                break 
            
    thread = threading.Thread(target=run)  
    thread.start()  


def Detener():
    global switch 
    global corre
    corre = 1
    switch = False
    print('Deteniendo')
    estado["state"] = "normal"
    estado.delete(0, END)
    estado.insert(0, "Deteniendo")
    estado.config(state='disabled') 
    iniciarbutton["state"] = "normal"
    estado["state"] = "disable"
    terminarbutton["state"] = "normal"
    

def Iniciar():
    global switch 
    global Estadoactual
    global guardarnombre
    if len(nombre.get()) == 0:
        print("the widget is empty")
        estado["state"] = "normal"
        estado.delete(0, END)
        estado.insert(0, "*** ERROR: Favor de insertar un nombre ***")
        errorlabel.config( bg = '#289995', fg = "red")
        estado["state"] = "disable"
    else:  
        errorlabel.config(bg = "#289995", fg = '#289995')
        switch = True
        estado["state"] = "normal"
        iniciarbutton["state"] = "disabled"
        estado["state"] = "disabled"
        terminarbutton["state"] = "disabled"
        if Estadoactual == "No Escribiendo":
            noEscribiendo()
        else:
            Escribiendo()
        if guardarnombre == 0:
           nombre.config(state='disabled') 
           guardarnombre = 1
        Lectura()


def Salir():
    global salir
    arduino.close()
    if salir == 0:
        root.destroy()
    salir = 1
    
def Escribiendo():
    global switch 
    global Estadoactual
    switch = True
    Escribiendobutton.configure(bg="#eaf558")
    Noescribiendobutton.configure(bg="grey")
    print('Escribiendo y Capturando')
    estado["state"] = "normal"
    estado.delete(0, END)
    estado.insert(0, "Escribiendo")
    Estadoactual = "Escribiendo"
    estado["state"] = "disable"
    
def noEscribiendo():
    global switch 
    global Estadoactual
    Escribiendobutton.configure(bg="grey")
    Noescribiendobutton.configure(bg="#eaf558")
    switch = True
    print('No escribiendo y Capturando')
    estado["state"] = "normal"
    estado.delete(0, END)
    estado.insert(0, "No Escribiendo")
    Estadoactual = "No Escribiendo"
    estado["state"] = "disable"



def animate(dataArray0, dataArray1, dataArray2, dataArray3, dataArray4, dataArray5,dataArray6):
    global z
 
    Gx = float(dataArray0)
    gxyar.append(Gx) 
    Gy = float(dataArray1)
    gyyar.append(Gy)
    Gz = float(dataArray2)
    gzyar.append(Gz)
    Ax = float(dataArray3)
    axyar.append(Ax)
    Ay = float(dataArray4)
    ayyar.append(Ay)
    Az = float(dataArray5)
    azyar.append(Az)
    FSR = float(dataArray6)
    
    if int(FSR) >= 3070 and int(FSR) <= 3100:
           FSR = 4096
           print(FSR)
    fsryar.append(FSR)
    
    xar.append(z)
    
    line.set_data(xar, gxyar)
    line1.set_data(xar, gyyar)
    line2.set_data(xar, gzyar)
    line3.set_data(xar, axyar)
    line4.set_data(xar, ayyar)
    line5.set_data(xar, azyar)
    line6.set_data(xar, fsryar)
    
    if(z >= 300):
        x = z-300
    else:
        x = 0
    axs[0].set_xlim(x, 150+z)
    axs[1].set_xlim(x, 150+z)
    axs[2].set_xlim(x, 150+z)
    z = z+1

    return line, line1, line2, line3, line4, line5, line6

def Graficar(dataArray0, dataArray1, dataArray2, dataArray3, dataArray4, dataArray5,dataArray6):
    
    ani = animation.FuncAnimation(fig, animate(dataArray0, dataArray1, dataArray2, dataArray3, dataArray4, dataArray5,dataArray6), interval=500, blit=True)

root = Tk()
root.geometry('1200x720')
root.title('Pensando')
root.configure(background = '#289995')

#img = ImageTk.PhotoImage(Image.open("C:\Users\oscar\Desktop\dearpygui\Logo_Pensando.JPG"))
#img = ImageTk.PhotoImage(Image.open("Logo_Pensando.JPG"))
#img = PhotoImage(file="C:\Users\oscar\Desktop\dearpygui\Logo_Pensando.JPG") 
#img = img.resize((50, 50), Image.ANTIALIAS)


nombre = Entry(root, width=70, borderwidth=5)
nombre.grid(row =0, column=0, columnspan=3, padx=10, pady=10)
nombre.pack()
#nombre.insert(0, "Nombre del archivo")
nombre.place(x = 10, y = 70, width = 400, height = 40)
nombre.config(font=(20))

estado = Entry(root, width=70, borderwidth=5)
#estado.grid(row =0, column=0, columnspan=3, padx=10, pady=10)
estado.pack()
estado.config(font=("Courier", 20))
estado.insert(0, "Bienvenido")
estado.place(x = 10, y = 320, width = 400, height = 40)
estado.config(font=(20))
estado["state"] = "disable"


nombrelabel = Label(root, text = "Nombre del archivo", bg = "#289995", bd = 100, fg = "white", font = "Castellar")
nombrelabel.pack()
nombrelabel.place(x=5, y = 45, width = 220, height = 20)

estadolabel = Label(root, text = "Estado", bg = "#289995", bd = 100, fg = "white", font = "Castellar")
estadolabel.pack()
estadolabel.place(x=5, y = 295, width = 80, height = 20)

errorlabel = Label(root, text = "^^^ ERROR: Favor de insertar un nombre ^^^", bg = "#289995", bd = 100, fg = '#289995', font = "Castellar")
errorlabel.pack()
errorlabel.place(x=10, y = 250, width = 430, height = 20)



calfsr = 0
Estadoactual = ""
dataArray = []
switch = True
z = 0
guardarnombre = 0
i = 0
salir = 0
titulo = ""
x = 0
xar = []
yar = []
gxyar = []
gyyar = []
gzyar = []
axyar = []
ayyar = []
azyar = []
fsryar = []
Gx = []
Gy = []
Gz = []
Ax = []
Ay = []
Az = []
FSR = []


fig = plt.figure()
gs = fig.add_gridspec(3, hspace=0.1)
axs = gs.subplots(sharex=True, sharey=False)
fig.suptitle('Sensores')

#axs[0] = fig.add_subplot(1, 1, 1)
axs[0].set_ylim(-32768, 32768)
axs[0].set_ylabel("Gyroscopio")

#axs[1] = fig.add_subplot(2, 1, 2)
axs[1].set_ylim(-32768, 32768)
axs[1].set_ylabel("Acelerometro")

#axs[2] = fig.add_subplot(3, 1, 3)
axs[2].set_ylim(0, 4500)
axs[2].set_ylabel("Presion")

line, = axs[0].plot(xar, gxyar, 'r')
line1, = axs[0].plot(xar, gyyar, 'b')
line2, = axs[0].plot(xar, gzyar, 'g')
line3, = axs[1].plot(xar, axyar, 'r')
line4, = axs[1].plot(xar, ayyar, 'g')
line5, = axs[1].plot(xar, azyar, 'b')
line6, = axs[2].plot(xar, fsryar, 'orange')

if(z >= 300):
    x = z-300
else:
    x = 0
axs[0].set_xlim(x, 150+z)
axs[1].set_xlim(x, 150+z)
axs[2].set_xlim(x, 150+z)
z = z+1

for ax in axs:
    ax.label_outer()
"""
********************  COM  ******************************
"""
arduino = serial.Serial('COM3', 74880)
arduino.flush()
arduinostring=arduino.readline()

plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().place(x = 450, y = 10, width = 700,height = 700)

iniciarbutton = Button(root, text="Iniciar", bg ="#5ccc7c", command = Iniciar)
iniciarbutton.pack()
iniciarbutton.place(x=10, y = 120, width = 190, height = 100)
iniciarbutton.config(font=(50))

pausarbutton = Button(root, text="Detener",  bg ="#db8472", command = Detener)
pausarbutton.pack()
pausarbutton.place(x=220, y = 120, width = 190,height = 100)
pausarbutton.config(font=(50))

Escribiendobutton = Button(root, text="Estado: Escribiendo", command = Escribiendo)
Escribiendobutton.pack()   
Escribiendobutton.place(x=10, y = 370, width = 190,height = 100)
Escribiendobutton.config(font=(50))      

Noescribiendobutton = Button(root, text="Estado: No Escribiendo", command = noEscribiendo)
Noescribiendobutton.pack()
Noescribiendobutton.place(x=220, y = 370, width = 190,height = 100)
Noescribiendobutton.config(font=(50))      

terminarbutton = Button(root, text="Terminar y Guardar", bg ="#c99524", fg='black', command = Salir)
terminarbutton.pack()  
terminarbutton.place(x=100, y = 580, width = 190,height = 100)
terminarbutton.config(font=(50))   


root.mainloop()
arduino.close()

if salir == 0:
    salir = 1
    Salir()
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
