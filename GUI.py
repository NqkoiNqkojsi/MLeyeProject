import tkinter
import video_streaming as vst
vst.Setup()
label1="Start"
m = tkinter.Tk()
taze = tkinter.IntVar()
vibr = tkinter.IntVar()
def StartStopVideo():
    isRunning=vst.ControlVideo(vibr.get())
    if isRunning==True:
        label1="Stop"
    else:
        label1="Start"


label2=tkinter.Label(m, text='IP')
e1 = tkinter.Entry(m)
label2.pack()
e1.pack()
but = tkinter.Button(m, text="Set", width=10, command=vst.SetIp(e1.get()))
but.pack()
w = tkinter.Canvas(m, width=1280, height=780)
w.pack()
button = tkinter.Button(m, text=label1, width=25, command=StartStopVideo())
button.pack()
C1=tkinter.Checkbutton(m, text='taze', variable=taze)
C2=tkinter.Checkbutton(m, text='vibrate', variable=vibr)
C1.pack()
C2.pack()
m.mainloop()