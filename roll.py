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


root2 = tk.Tk()
root2.title("Subject")
                    # Add a grid
mainframe = Frame(root2)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.pack(pady=200, padx=200)

                    # Create a Tkinter variable
tkvar = StringVar(root2)
choices = {'DSA', 'Java', 'Physics', 'Math', 'Python', 'Microprocessor'}
tkvar.set('......')  # set the default option
popupMenu = OptionMenu(mainframe, tkvar, *choices)
Label(mainframe, text="Choose a Subject").grid(row=1, column=1)
popupMenu.grid(row=2, column=1)

                    # on change dropdown value
def change_dropdown(*args):
    global newsubcode
    newsubcode = tkvar.get()
    print(newsubcode)

rolltext = tk.StringVar()
def display():
    root2.destroy()
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='attendance',
                                            user='root',
                                            password='')

        sql_select_query="""select `count` from `attendance` where `subject_id` in (select `subject_id` from `subject` where `subject_name` = '%s')
                and `student_id` in(select `student_id` from `students` where `enrollment`= '%s')""" % (newsubcode,rolltext.get())

        cursor=connection.cursor()
        cursor.execute(sql_select_query)
        attnd_record = cursor.fetchall()
        attnd_count = 0
        for i in attnd_record:
                attnd_count = i[0]
                print(attnd_count)
                connection.commit()
        new = "The attendance for " + newsubcode + " for Enrollment " + rolltext.get() + " is: " + str(attnd_count)
        popup4 = tk.Tk()
        popup4.wm_title("!")
        popup4.geometry('400x100')
        label2 = tk.Label(popup4, text=new, font=("Verdana",10))
        label2.pack(side="top", fill="x", pady=10)
        B3 = tk.Button(popup4, height=2, width=10, text="Okay", command=popup4.destroy)
        B3.pack()
    except mysql.connector.Error as error:
        connection.rollback()  # rollback if any exception occured

    finally:
                            # closing database connection.
                if (connection.is_connected()):
                        cursor.close()
                        connection.close()
                        print("MySQL connection is closed")

button2 = tk.Button(root2, text="Submit", fg="black",command=display, bg="white", width=10,
                                     height=2, font=('times', 15, ' bold '))
button2.place(x=185, y=350)

roll = tk.Label(root2, text="Enrollment", width=10, height=2, fg="black", bg="white",
                                  font=('times', 15, ' bold '))
roll.place(x=50, y=50)

roll_enter = tk.Entry(root2, width=13,bg="white", fg="black",textvariable=rolltext, font=('times', 30, ' bold '))
roll_enter.place(x=200, y=50)

tkvar.trace('w', change_dropdown)
root2.mainloop()

