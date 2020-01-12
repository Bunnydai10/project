import tkinter as tk
from tkinter import *
from plyer import notification

win = tk.Tk()
win.title("Signup")
win.geometry('880x420')
win.configure(background='snow')
usernametext = tk.StringVar()
passwordtext = tk.StringVar()

def signup():
        win.destroy()
        popup = tk.Tk()
        popup.wm_title("!")
        popup.geometry('300x100')
        label = tk.Label(popup, text='Teacher successfully registered', font=("Verdana", 12))
        label.pack(side="top", fill="x", pady=40)
        B1 = tk.Button(popup, height=2,width=10,text="Okay", command=popup.destroy)
        B1.pack()
        popup.mainloop()
        import mysql.connector
        from mysql.connector import Error
        from mysql.connector import errorcode
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='attendance',
                                                 user='root',
                                                 password='')
            sql_insert_query = """ INSERT INTO `teacher` (`username`,`password`) VALUES (%s,%s)"""
            VALUES = (str(usernametext.get()), str(passwordtext.get()))
            cursor = connection.cursor()
            result = cursor.execute(sql_insert_query, VALUES)
            connection.commit()

        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured

        finally:
            # closing database connection.
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

sun = tk.Label(win, text="Username", width=15, height=2, fg="black", bg="white",font=('times', 15, ' bold '))
sun.place(x=30, y=50)

spw = tk.Label(win, text="Password", width=15, height=2, fg="black", bg="white",font=('times', 15, ' bold '))
spw.place(x=30, y=150)

sun_entr = tk.Entry(win, width=20, bg="white", fg="black", textvariable=usernametext, font=('times', 23, ' bold '))
sun_entr.place(x=290, y=55)

spw_entr = tk.Entry(win, width=20, show="*", bg="white", fg="black", textvariable=passwordtext,font=('times', 23, ' bold '))
spw_entr.place(x=290, y=155)

signup = tk.Button(win, text="Sign Up", fg="black", bg="white", width=20, command=signup,height=2, font=('times', 15, ' bold '))
signup.place(x=290, y=250)

win.mainloop()





