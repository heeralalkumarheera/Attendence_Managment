"""
╔══════════════════════════════════════════════════════════════════╗
║     ATTENDANCE MANAGEMENT SYSTEM - FACE RECOGNITION              ║
║                                                                  ║
║  📌 ADMIN CREDENTIALS CONFIGURATION                              ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  To change admin username/password, go to Line 553-554           ║
║  Search for: "# Admin Credentials - Change username"            ║
║                                                                  ║
║  Current Credentials:                                            ║
║  Username: Heeralal                                              ║
║  Password: Heera@1234                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
#we use tkinter to create GUI (Graphical User Interface)
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
from config import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    ATTENDANCE_DIR,
    CASCADE_PATH,
    MODEL_PATH,
    STUDENT_CSV,
    TRAINING_DIR,
    ensure_data_dirs,
    ensure_student_csv,
)
from components.admin_panel import admin_panel as admin_panel_component
from utils.validators import is_digit_input
from utils.logger import log_info

# Ensure required folders and base CSV exist
ensure_data_dirs()
ensure_student_csv()
log_info("Main attendance UI started")

# Window is our Main frame of system
window = tk.Tk()
window.title("Attendance Management System - Face Recognition")
window.state('zoomed')  # Maximize window
window.configure(background='#1e3a5f')  # Modern dark blue background

# GUI for manually fill attendance
# Manual Attendance

def manually_fill():
    global sb
    sb = tk.Tk()
    #Input Subject Name
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='grey80')

    def err_screen_for_subject():

        def ec_delete():
            ec.destroy()
        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        
        ec.title('Warning!!')
        ec.configure(background='snow')
        Label(ec, text='Please enter your subject name!!!', fg='red',
              bg='white', font=('times', 16, ' bold ')).pack()
        Button(ec, text='OK', command=ec_delete, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",
               font=('times', 15, ' bold ')).place(x=90, y=50)
    #Fill Attendance
    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        # Creatting csv of attendance

        # Create table for Attendance
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        global subb
        subb = SUB_ENTRY.get()
        DB_table_name = str(subb + "_" + Date + "_Time_" +
                            Hour + "_" + Minute + "_" + Second)

        import pymysql.connections

        # Connect to the database
        try:
            global cursor
            connection = pymysql.connect(
                host='localhost', user='root', password='', db='manually_fill_attendance')
            cursor = connection.cursor()
        except Exception as e:
            print(e)
        #except pymysql.MySQLError as e:
         #     print(f"Database connection failed: {e}")
        sql = "CREATE TABLE " + DB_table_name + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                         ENROLLMENT varchar(100) NOT NULL,
                         NAME VARCHAR(50) NOT NULL,
                         DATE VARCHAR(20) NOT NULL,
                         TIME VARCHAR(20) NOT NULL,
                             PRIMARY KEY (ID)
                             );
                        """

        try:
            cursor.execute(sql)  # for create a table
        except Exception as ex:
            print(ex)  #

        if subb == '':
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            # MFW.iconbitmap('AMS.ico')
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry('880x470')
            MFW.configure(background='grey80')

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                # errsc2.iconbitmap('AMS.ico')
                errsc2.title('Warning!!')
                errsc2.configure(background='grey80')
                Label(errsc2, text='Please enter Student & Enrollment!!!', fg='black', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="black", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="black", bg="grey",
                           font=('times', 15))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="black", bg="grey",
                                font=('times', 15))
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, validate='key',
                                 bg="white", fg="black", font=('times', 23))
            ENR_ENTRY['validatecommand'] = (
                ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(
                MFW, width=20, bg="white", fg="black", font=('times', 23))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            # get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == '':
                    err_screen1()
                elif STUDENT == '':
                    err_screen1()
                else:
                    time = datetime.datetime.fromtimestamp(
                        ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    Insert_data = "INSERT INTO " + DB_table_name + \
                        " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(ENROLLMENT), str(
                        STUDENT), str(Date), str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                    except Exception as e:
                        print(e)
                    ENR_ENTRY.delete(first=0, last=22)
                    STUDENT_ENTRY.delete(first=0, last=22)

            def create_csv():
                import csv
                cursor.execute("select * from " + DB_table_name + ";")
                csv_name = str(ATTENDANCE_DIR / f"Manually_Attendance_{DB_table_name}.csv")
                
                with open(csv_name, "w") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(
                        [i[0] for i in cursor.description])  # write headers
                    csv_writer.writerows(cursor)
                    O = "CSV created Successfully"
                    Notifi.configure(text=O, bg="Green", fg="white",
                                     width=33, font=('times', 19, 'bold'))
                    Notifi.place(x=180, y=380)
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + subb)
                root.configure(background='grey80')
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=18, height=1, fg="black", font=('times', 13, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            Notifi = tk.Label(MFW, text="CSV created Successfully", bg="Green", fg="white", width=33,
                              height=2, font=('times', 19, 'bold'))

            c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="white", bg="black", width=10,
                                     height=1,
                                     activebackground="white", font=('times', 15, ' bold '))
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="white", bg="black", width=10,
                                      height=1,
                                      activebackground="white", font=('times', 15, ' bold '))
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="black", bg="SkyBlue1", width=20,
                                 height=2,
                                 activebackground="white", font=('times', 15, ' bold '))
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(MFW, text="Convert to CSV", command=create_csv, fg="black", bg="SkyBlue1", width=20,
                                 height=2,
                                 activebackground="white", font=('times', 15, ' bold '))
            MAKE_CSV.place(x=570, y=300)

            def attf():
                import subprocess
                abs_path = ATTENDANCE_DIR
                subprocess.Popen(r'explorer "' + str(abs_path) + '"')

            attf = tk.Button(MFW,  text="Check Sheets", command=attf, fg="white", bg="black",
                             width=12, height=1, activebackground="white", font=('times', 14, ' bold '))
            attf.place(x=730, y=410)

            MFW.mainloop()

    SUB = tk.Label(sb, text="Enter Subject : ", width=15, height=2,
                   fg="black", bg="grey80", font=('times', 15, ' bold '))
    SUB.place(x=30, y=100)

    global SUB_ENTRY

    SUB_ENTRY = tk.Entry(sb, width=20, bg="white",
                         fg="black", font=('times', 23))
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(sb, text="Fill Attendance", command=fill_attendance, fg="black", bg="SkyBlue1", width=20, height=2,
                                       activebackground="white", font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()

# For clear textbox


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
    # sc1.iconbitmap('AMS.ico')
    sc1.title('Warning!!')
    sc1.configure(background='grey80')
    Label(sc1, text='Enrollment & Name required!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc1, text='OK', command=del_sc1, fg="black", bg="lawn green", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# Error screen2


def del_sc2():
    sc2.destroy()


def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    # sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='grey80')
    Label(sc2, text='Please enter your subject name!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="lawn green", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# For take images for datasets


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
            detector = cv2.CascadeClassifier(str(CASCADE_PATH))
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
                    cv2.imwrite(str(TRAINING_DIR / f"{Name}.{Enrollment}.{sampleNum}.jpg"), gray)
                    print("Images Saved for Enrollment :")
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                #
                # # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break


            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(
                text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)


# for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        sub = tx.get()
        now = time.time()  # For calculate seconds of video
        future = now + 20
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                try:
                    recognizer.read(str(MODEL_PATH))
                except:
                    e = 'Model not found,Please train model'
                    Notifica.configure(
                        text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                    Notifica.place(x=20, y=250)

                harcascadePath = str(CASCADE_PATH)
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv(str(STUDENT_CSV))
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
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(
                                ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [
                                Id, aa, date, timeStamp]
                            cv2.rectangle(
                                im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y),
                                        font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(
                                im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y),
                                        font, 1, (0, 25, 255), 4)
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = str(ATTENDANCE_DIR / f"{Subject}_{date}_{Hour}-{Minute}-{Second}.csv")
                attendance = attendance.drop_duplicates(
                    ['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)

                # Create table for Attendance
                date_for_DB = datetime.datetime.fromtimestamp(
                    ts).strftime('%Y_%m_%d')
                DB_Table_name = str(
                    Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
                import pymysql.connections

                # Connect to the database
                try:
                    global cursor
                    connection = pymysql.connect(
                        host='localhost', user='root', password='', db='Face_reco_fill')
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                sql = "CREATE TABLE " + DB_Table_name + """
                (ID INT NOT NULL AUTO_INCREMENT,
                 ENROLLMENT varchar(100) NOT NULL,
                 NAME VARCHAR(50) NOT NULL,
                 DATE VARCHAR(20) NOT NULL,
                 TIME VARCHAR(20) NOT NULL,
                     PRIMARY KEY (ID)
                     );
                """
                # Now enter attendance in Database
                insert_data = "INSERT INTO " + DB_Table_name + \
                    " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                VALUES = (str(Id), str(aa), str(date), str(timeStamp))
                try:
                    cursor.execute(sql)  # for create a table
                    # For insert data into table
                    cursor.execute(insert_data, VALUES)
                except Exception as ex:
                    print(ex)  #

                M = 'Attendance filled Successfully'
                Notifica.configure(text=M, bg="Green", fg="white",
                                   width=33, font=('times', 15, 'bold'))
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='grey80')
                cs = fileName
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=10, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)

    # windo is frame for subject chooser
    windo = tk.Tk()
    # windo.iconbitmap('AMS.ico')
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='grey80')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                        height=2, font=('times', 15, 'bold'))

    def Attf():
        import subprocess
        abs_path = ATTENDANCE_DIR
        subprocess.Popen(r'explorer "' + str(abs_path) + '"')

    attf = tk.Button(windo,  text="Check Sheets", command=Attf, fg="white", bg="black",
                     width=12, height=1, activebackground="white", font=('times', 14, ' bold '))
    attf.place(x=430, y=255)

    sub = tk.Label(windo, text="Enter Subject : ", width=15, height=2,
                   fg="black", bg="grey", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="white",
                  fg="black", font=('times', 23))
    tx.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="white", command=Fillattendances, bg="SkyBlue1", width=20, height=2,
                       activebackground="white", font=('times', 15, ' bold '))
    fill_a.place(x=250, y=160)
    windo.mainloop()


def admin_panel():
    win = tk.Tk()
    # win.iconbitmap('AMS.ico')
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='grey80')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        # Admin Credentials - Change username and password below
        if username == 'Heeralal':
            if password == 'Heera@1234':
                win.destroy()
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background='grey80')

                cs = str(STUDENT_CSV)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=10, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="red", fg="white",
                             width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)

        else:
            valid = 'Incorrect ID or Password'
            Nt.configure(text=valid, bg="red", fg="white",
                         width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)

    Nt = tk.Label(win, text="Attendance filled Successfully", bg="Green", fg="white", width=40,
                  height=2, font=('times', 19, 'bold'))
    # Nt.place(x=120, y=350)

    un = tk.Label(win, text="Enter username : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black",
                       font=('times', 23))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white",
                       fg="black", font=('times', 23))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="SkyBlue1", width=20,
                      height=2,
                      activebackground="Red", command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()


# For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier(str(CASCADE_PATH))
    try:
        global faces, Id
        faces, Id = getImagesAndLabels(str(TRAINING_DIR))
    except Exception as e:
        l = 'please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3",
                               width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save(str(MODEL_PATH))
    except Exception as e:
        q = 'Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3",
                               width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="olive drab",
                           width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)


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


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
# window.iconbitmap('AMS.ico')


def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

# Header Frame
header_frame = tk.Frame(window, bg='#2c5f8d', height=120)
header_frame.pack(fill='x')

message = tk.Label(header_frame, text="🎓 ATTENDANCE MANAGEMENT SYSTEM", 
                   bg="#2c5f8d", fg="white", 
                   font=('Arial', 36, 'bold'), pady=20)
message.pack()

sub_message = tk.Label(header_frame, text="Powered by Face Recognition Technology", 
                       bg="#2c5f8d", fg="#a8d5ff", 
                       font=('Arial', 14, 'italic'))
sub_message.pack()

Notification = tk.Label(window, text="✓ System Ready", bg="#28a745", fg="white", width=40,
                        height=2, font=('Arial', 14, 'bold'), relief='flat')

# Input Section Frame
input_frame = tk.Frame(window, bg='#1e3a5f')
input_frame.pack(pady=30)

lbl = tk.Label(input_frame, text="📋 Enrollment ID:", width=18, height=2,
               fg="white", bg="#2c5f8d", font=('Arial', 14, 'bold'), relief='ridge', bd=2)
lbl.grid(row=0, column=0, padx=10, pady=10)


def testVal(inStr, acttyp):
    return is_digit_input(inStr, acttyp)


txt = tk.Entry(input_frame, validate="key", width=25, bg="white",
               fg="#2c5f8d", font=('Arial', 18), relief='solid', bd=2)
txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
txt.grid(row=0, column=1, padx=10, pady=10)

lbl2 = tk.Label(input_frame, text="👤 Student Name:", width=18, fg="white",
                bg="#2c5f8d", height=2, font=('Arial', 14, 'bold'), relief='ridge', bd=2)
lbl2.grid(row=1, column=0, padx=10, pady=10)

txt2 = tk.Entry(input_frame, width=25, bg="white",
                fg="#2c5f8d", font=('Arial', 18), relief='solid', bd=2)
txt2.grid(row=1, column=1, padx=10, pady=10)

clearButton = tk.Button(input_frame, text="🗑️ Clear", command=clear, fg="white", bg="#dc3545",
                        width=12, height=1, activebackground="#c82333", font=('Arial', 12, 'bold'),
                        relief='raised', bd=3, cursor='hand2')
clearButton.grid(row=0, column=2, padx=10, pady=10)

clearButton1 = tk.Button(input_frame, text="🗑️ Clear", command=clear1, fg="white", bg="#dc3545",
                         width=12, height=1, activebackground="#c82333", font=('Arial', 12, 'bold'),
                         relief='raised', bd=3, cursor='hand2')
clearButton1.grid(row=1, column=2, padx=10, pady=10)

# Button Panel Frame
button_frame = tk.Frame(window, bg='#1e3a5f')
button_frame.pack(pady=40)

# Row 1 - Main Action Buttons
row1_frame = tk.Frame(button_frame, bg='#1e3a5f')
row1_frame.pack(pady=10)

takeImg = tk.Button(row1_frame, text="📸 CAPTURE IMAGES", command=take_img, fg="white", bg="#17a2b8",
                    width=22, height=3, activebackground="#138496", font=('Arial', 13, 'bold'),
                    relief='raised', bd=4, cursor='hand2')
takeImg.grid(row=0, column=0, padx=15, pady=10)

trainImg = tk.Button(row1_frame, text="🧠 TRAIN MODEL", fg="white", command=trainimg, bg="#6f42c1",
                     width=22, height=3, activebackground="#5a32a3", font=('Arial', 13, 'bold'),
                     relief='raised', bd=4, cursor='hand2')
trainImg.grid(row=0, column=1, padx=15, pady=10)

FA = tk.Button(row1_frame, text="✅ AUTO ATTENDANCE", fg="white", command=subjectchoose,
               bg="#28a745", width=22, height=3, activebackground="#218838", font=('Arial', 13, 'bold'),
               relief='raised', bd=4, cursor='hand2')
FA.grid(row=0, column=2, padx=15, pady=10)

# Row 2 - Secondary Buttons
row2_frame = tk.Frame(button_frame, bg='#1e3a5f')
row2_frame.pack(pady=10)

quitWindow = tk.Button(row2_frame, text="📝 MANUAL ATTENDANCE", command=manually_fill, fg="white",
                       bg="#fd7e14", width=22, height=3, activebackground="#e8590c", font=('Arial', 13, 'bold'),
                       relief='raised', bd=4, cursor='hand2')
quitWindow.grid(row=0, column=0, padx=15, pady=10)

AP = tk.Button(row2_frame, text="👥 VIEW STUDENTS", command=lambda: admin_panel_component(window), fg="white",
               bg="#20c997", width=22, height=3, activebackground="#1aa179", font=('Arial', 13, 'bold'),
               relief='raised', bd=4, cursor='hand2')
AP.grid(row=0, column=1, padx=15, pady=10)

window.mainloop()
