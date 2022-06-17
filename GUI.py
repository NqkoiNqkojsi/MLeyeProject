import tkinter
import video_streaming as vst
isRunning=False
label1="Start"
taze = tkinter.IntVar(1)
vibr = tkinter.IntVar(0)
def StartStopVideo():
    isRunning=not isRunning
    if isRunning==True:
        label1="Stop"
        vst.Main_Run(vibr.get())
    else:
        label1="Start"
        vst.isActive()
        

m = tkinter.Tk()
w = tkinter.Canvas(m, width=1280, height=780)
w.pack()
button = tkinter.Button(m, text=label1, width=25, command=StartStopVideo())
button.pack()
C1=tkinter.Checkbutton(m, text='taze', variable=taze)
C2=tkinter.Checkbutton(m, text='vibrate', variable=vibr)
C1.pack()
C2.pack()
m.mainloop()