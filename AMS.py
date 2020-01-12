import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time

#####Window is our Main frame of system
window = tk.Tk()
window.title("Attendance System Using Face Recognition")
window.geometry('1024x600')
window.configure(background='dark blue')
####GUI for manually fill attendance

##For clear textbox
def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)
def del_sc1():
    sc1.destroy()
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Warning!!')
    sc1.configure(background='snow')
    Label(sc1,text='Enrollment & Name required!',fg='black',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc1,text='OK',command=del_sc1,fg="black"  ,bg="white"  ,width=9  ,height=1,font=('times', 15, ' bold ')).place(x=90,y= 50)

##Error screen2
def del_sc2():
    sc2.destroy()
def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    Label(sc2,text='Please enter your subject name!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc2,text='OK',command=del_sc2,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

###For take images for datasets
def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 200:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            import mysql.connector
            from mysql.connector import Error
            from mysql.connector import errorcode
            try:
                connection = mysql.connector.connect(host='localhost',
                                                     database='attendance',
                                                     user='root',
                                                     password='')
                sql_insert_query = """ INSERT INTO `students`
                                      (`Enrollment`, `Name`) VALUES (%s,%s)"""
                VALUES = (str(Enrollment),str(Name))
                cursor = connection.cursor()
                result = cursor.execute(sql_insert_query,VALUES)
                connection.commit()
                print("Record inserted successfully into student table")
            except mysql.connector.Error as error:
                connection.rollback()  # rollback if any exception occured
                print("Failed inserting record into student table {}".format(error))
            finally:
                # closing database connection.
                if (connection.is_connected()):
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")

            popup2 = tk.Tk()
            popup2.wm_title("!")
            popup2.geometry('300x100')
            label2 = tk.Label(popup2, text="Image Saved", font=("Verdana", 10))
            label2.pack(side="top", fill="x", pady=10)
            B2 = tk.Button(popup2, height=2, width=10, text="Okay", command=popup2.destroy)
            B2.pack()
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)

            # adding student info to the database
            import mysql.connector
            from mysql.connector import Error
            from mysql.connector import errorcode
            try:
                connection = mysql.connector.connect(host='localhost',
                                                     database='attendance',
                                                     user='root',
                                                     password='')
                sql_insert_query = """ INSERT INTO `student`
                                      (`Enrollment`, `Name`) VALUES (1,'Scott')"""
                cursor = connection.cursor()
                result = cursor.execute(sql_insert_query)
                connection.commit()
                print("Record inserted successfully into python_users table")
            except mysql.connector.Error as error:
                connection.rollback()  # rollback if any exception occured
                print("Failed inserting record into python_users table {}".format(error))
            finally:
                # closing database connection.
                if (connection.is_connected()):
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")


###for choose subject and fill attendance
def subjectchoose():
    root = tk.Tk()
    root.title("Subject")
    # Add a grid
    mainframe = Frame(root)
    mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)
    mainframe.pack(pady = 200, padx = 200)

    # Create a Tkinter variable
    tkvar = StringVar(root)
    choices = {'DSA','Java','Physics','Math','Python','Microprocessor'}
    tkvar.set('......') # set the default option
    popupMenu = OptionMenu(mainframe, tkvar, *choices)
    Label(mainframe, text="Choose a Subject").grid(row = 1, column = 1)
    popupMenu.grid(row = 2, column =1)

    # on change dropdown value
    def change_dropdown(*args):
        global subcode
        subcode= tkvar.get()
        print(subcode)

    frame = tk.Frame(root)
    frame.pack()
    button = tk.Button(frame,text="Choose",width=20,height=3,fg="black",bg="white",command=Fillattendances)
    button.pack(side=tk.LEFT)

    # link function to change dropdown
    tkvar.trace('w', change_dropdown)
    root.mainloop()


def Fillattendances():
    sub = subcode
    now = time.time()  ###For calculate seconds of video
    future = now + 15
    if time.time() < future:
        if sub == '':
            err_screen1()
        else:
            recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
            try:
                recognizer.read("TrainingImageLabel\Trainner.yml")
            except:
                e = 'Model not found,Please train model'
                Notifica = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                                        height=3, font=('times', 17, 'bold'))
                Notifica.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                Notifica.place(x=20, y=250)

            harcascadePath = "haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(harcascadePath)
            df = pd.read_csv("StudentDetails\StudentDetails.csv")
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ['Enrollment', 'Name', 'Date', 'Time']
            attendance = pd.DataFrame(columns=col_names)
            while True:
                ret, im = cam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                for (x, y, w, h) in faces:
                    global Id

                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if (conf < 70):
                        print(conf)
                        global Subject
                        global aa
                        global date
                        global timeStamp
                        Subject = subcode
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        aa = df.loc[df['Enrollment'] == Id]['Name'].values
                        global tt
                        tt = str(Id) + "-" + aa
                        En = '15624031' + str(Id)
                        attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
                    else:
                        retut = 'Unknown'
                        tt = str(retut)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                if time.time() > future:
                    break

                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                cv2.imshow('Filling attedance..', im)
                key = cv2.waitKey(30) & 0xff
                if key == 27:
                    break

            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            print(Id)
            # inserting attendance
            import mysql.connector
            from mysql.connector import Error
            from mysql.connector import errorcode
            try:

                connection = mysql.connector.connect(host='localhost',
                                                     database='attendance',
                                                     user='root',
                                                     password='')

                cursor = connection.cursor()
                print("Id is",Id)
                sql_select_query = """select `student_id` from `students` where `enrollment`= %s """ % (Id)

                # sbu="""select `subject_id` from `subject` where `subject_name`= '%s'""" % (subcode)
                cursor.execute(sql_select_query)
                records = cursor.fetchall()
                stud_id = 0
                for i in records:
                    stud_id = i[0]
                    print(stud_id)

                sql_select = """select `subject_id` from `subject` where `subject_name`= '%s' """ % (subcode)
                print(sql_select)
                print("Sub code",subcode)
                cursor.execute(sql_select)
                records1 = cursor.fetchall()
                print(13)
                for j in records1:
                    sub_id = j[0]
                    print("Subject id ",sub_id)

                print(sub_id)
                print(stud_id)
                sql_final ="""select `id`,`count` from `attendance` where `subject_id`=%s and `student_id`='%s'""" % (sub_id, stud_id)
                cursor.execute(sql_final)
                records2= cursor.fetchall()
                att_id = 0
                count=1
                for k in records2:
                    att_id = k[0]
                    count = k[1]
                print("attendance_id", att_id)
                print("count", count)

                if len(records2) == 0:
                    sql_insert_query = """INSERT INTO `attendance` (`student_id`,`subject_id`, `count`) VALUES (%s,%s,%s)"""
                    VALUES = (str(stud_id),str(sub_id),count)
                    cursor.execute(sql_insert_query,VALUES)

                else:
                    count+=1
                    sql_update_query= """update `attendance` set `count` = %s where `id`=%s""" % (count,att_id)
                    cursor.execute(sql_update_query)
                connection.commit()
                connection.close()

                print("Record inserted successfully into attendance table")
            except mysql.connector.Error as error:
                connection.rollback()  # rollback if any exception occured
                print("Failed inserting record into attendance table")
            finally:
                # closing database connection.
                if (connection.is_connected()):
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")


def admin_panel():
    win = tk.Tk()
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='snow')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'user' :
            if password == 'user':
                win.destroy()
                import tkinter
                root = tk.Tk()
                root.title("Logged In")
                root.geometry('880x420')
                def view():
                    root.destroy()
                    os.system('python roll.py')

                view = tk.Button(root, text="View Attendance",command=view, fg="black", bg="white", width=20,
                                  height=2, font=('times', 15, ' bold '))
                view.place(x=290, y=150)
                def teacher():
                    root.destroy()
                    os.system('python teacher.py')
                create = tk.Button(root, text="Create Teacher's Account", command= teacher, fg="black", bg="white", width=20,
                                  height=2, font=('times', 15, ' bold '))
                create.place(x=290, y=250)

                root.mainloop()

            else:
                print('Incorrect ID or Password')
        else:
            print('Incorrect ID or Password')

    un = tk.Label(win, text="Username", width=15, height=2, fg="black", bg="white",
                          font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Password", width=15, height=2, fg="black", bg="white",
                          font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black", font=('times', 23, ' bold '))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20,show="*", bg="white", fg="black", font=('times', 23, ' bold '))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="black", bg="white", width=10, height=1,
                         font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="black", bg="white", width=10, height=1,
                   font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="white", width=20,
                       height=2,
                       command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)


    win.mainloop()

###For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces,Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l='please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel\Trainner.yml")
    except Exception as e:
        q='Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Student Registered"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=150, y=400)
    windel.destroy()

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

def registration():
    global windel
    windel = tk.Tk()
    windel.title("Register Student")
    windel.geometry('1024x600')
    ENR = tk.Label(windel, text="Enter Enrollment", width=20, height=2, fg="black", bg="white",
                   font=('times', 15, ' bold '))
    ENR.place(x=200, y=200)

    global txt
    txt = tk.Entry(windel, validate="key", width=20, bg="white", fg="black", font=('times', 25, ' bold '))
    txt.place(x=550, y=200)

    lbl2 = tk.Label(windel, text="Enter Name", width=20, fg="black", bg="white", height=2, font=('times', 15, ' bold '))
    lbl2.place(x=200, y=300)

    global txt2
    txt2 = tk.Entry(windel, width=20, bg="white", fg="black", font=('times', 25, ' bold '))
    txt2.place(x=550, y=300)

    takeImg = tk.Button(windel, text="Take Images",command=take_img,fg="black", bg="white", width=20, height=3,
                        font=('times', 15, ' bold '))
    takeImg.place(x=400, y=400)

    trainImg = tk.Button(windel, text="Register Student",command=trainimg,fg="black", bg="white", width=20, height=3,
                        font=('times', 15, ' bold '))
    trainImg.place(x=400, y=500)

    windel.mainloop()

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                      height=3, font=('times', 17, 'bold'))

message = tk.Label(window, text="Attendance System Using Face Recognition", bg="white", fg="black", width=45,
                   height=3, font=('times', 25, 'bold '))
message.place(x=50, y=20)

AP = tk.Button(window, text="Register Student",command=registration,fg="black"  ,bg='white'  ,width=15 ,height=5,font=('times', 15, ' bold '))
AP.place(x=100, y=200)

FA = tk.Button(window, text="Attendance",command=subjectchoose,fg="black",bg="white"  ,width=15  ,height=5,font=('times', 15, ' bold '))
FA.place(x=400, y=200)

AP = tk.Button(window, text="Admin Log In",command=admin_panel,fg="black"  ,bg="white"  ,width=15 ,height=5 ,font=('times', 15, ' bold '))
AP.place(x=700, y=200)

window.mainloop()
