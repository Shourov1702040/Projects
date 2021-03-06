from tkinter.ttk import *
from tkinter import *
import datetime
from tkinter.font import Font
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
import cv2
import pickle
from decimal import Decimal
import pandas as pd
from PIL import Image, ImageTk

from progress2 import PSS2

date = datetime.datetime.now().date()
# print(date)
# print(date.strftime("%x"))
date = str(date.strftime("%x"))

class Classification(Toplevel):
    def __init__(self,item_info):
        Toplevel.__init__(self)
        self.geometry('800x650+1000+200')
        self.title("Detect apple disease")
        self.resizable(False, False)


        self.top = Frame(self, height=400,bg='#fff')
        self.top.pack(fill=X)

        self.bottom= Frame(self, height=250)
        self.bottom.pack(fill=X)

        self.auto_value = item_info.split("@")
        # print(self.auto_value)

        #@______________________________________ Menubar ______________________________________@#

        self.my_font = Font(family="Consolas", size=18, weight="bold")
        self.my_font2 = Font(family="Consolas", size=16, weight="bold")
        self.my_font3 = Font(family="Consolas", size=14, weight="bold")

        self.main_menu = Menu(self)
        self.config(menu=self.main_menu)

        self.fileMenu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="File", menu=self.fileMenu, font=self.my_font3)
        self.editMenu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Edit", menu=self.editMenu, font=self.my_font3)

        self.fileMenu.add_command(label="New", font=self.my_font3)
        self.fileMenu.add_command(label="Search", font=self.my_font3)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Open", font=self.my_font3)

        self.saveMenu = Menu(self.fileMenu)
        self.saveMenu.add_command(label="Save", font=self.my_font3)
        self.saveMenu.add_command(label="Save as", font=self.my_font3)

        self.fileMenu.add_cascade(label="Save", menu=self.saveMenu, font=self.my_font3)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", font=self.my_font3)


        #@________________________________ Top frame design ______________________________________@#

        img_jpg = Image.open(self.auto_value[0])
        self.top_image = ImageTk.PhotoImage(img_jpg)

        self.top_image_label = Label(self.top, image = self.top_image,bg='#fff')
        self.top_image_label.place(x=30,y=5)

        self.heading = Label(self.top, text=self.auto_value[1], font='Arial 28 bold',
                             bg='#fff',fg=self.auto_value[3])
        self.heading.place(x=265,y=46)

        self.date_lbl=Label(self.top, text ='Date: '+date, font='Consolas 18 bold', fg='#775D1E',bg='#fff')
        self.date_lbl.place(x=585,y=140)

        self.F_label = Label(self.top, text="Choose an image file to check", font='Consolas 18 bold', bg="#fff",
                             fg="#203d80")
        self.F_label.place(x=10, y=180)

        self.entry_val = StringVar()
        self.path=""
        self.path_entry = Entry(self.top,font='consolas 17 ',width=35,textvariable=self.entry_val,bd=2,bg="#f5f5f5")
        self.path_entry.place(x=12,y=208)

        self.choose_btn = Button(self.top,text="choose",font='consolas 14 bold',width=7,bd=3,command=self.get_file)
        self.choose_btn.place(x=474,y=205)

        self.submit_btn = Button(self.top, text='Submit', font='consolas 17 bold', fg="#fff", bg="#09AD1A", width=12,
                                 bd=3,
                                 command=self.submit_fun)
        self.submit_btn.place(x=595, y=203)

        self.label1 = Label(self.top, text="Fruits type:", font='Consolas 14 bold', bg="#fff")
        self.label1.place(x=10, y=255)
        self.disease_val = StringVar()

        self.disease_label = Label(self.top, font='Arial 15 bold', bg="#fff", textvariable=self.disease_val,
                                   fg="#C20202")
        self.disease_label.place(x=145, y=255)

        self.label2 = Label(self.top, text="Probability:", font='Consolas 14 bold', bg="#fff")
        self.label2.place(x=10, y=290)
        self.acc_val = StringVar()

        self.acc_label = Label(self.top, font='Consolas 14 bold', bg="#fff", textvariable=self.acc_val, fg="#058219")
        self.acc_label.place(x=145, y=290)

        self.label3 = Label(self.top, text="Doctors advice", font='Consolas 14 bold', bg="#fff")
        self.label3.place(x=10, y=330)
        self.solution_btn = Button(self.top, text='Fetch', font='Consolas 14 bold', width=22, bg="#249DB9",
                                   fg="#FFF", command=self.solution)
        self.solution_btn.place(x=10, y=355)

        self.label4 = Label(self.top, text="More symptom", font='Consolas 14 bold', bg="#fff")
        self.label4.place(x=345, y=330)
        self.symptom_btn = Button(self.top, text='Symptoms', font='Consolas 14 bold', width=22, bg="#444491",
                                 fg="#FFF", command=self.symptoms)
        self.symptom_btn.place(x=287, y=355)

        self.label5 = Label(self.top, text="Clear", font='Consolas 14 bold', bg="#fff")
        self.label5.place(x=595, y=330)
        self.clear_btn = Button(self.top, text='Clear', font='Consolas 14 bold', width=9, bg="#d00707", fg="#FFF",
                                command=self.clear_fun)
        self.clear_btn.place(x=563, y=355)

        self.v = ['1x', '1.5x', '2x', '2.5x', '3x', '3.5x', '4x']
        self.cb = Combobox(self.top, values=self.v, font='arial 19 bold', width=4, state='readonly')
        self.cb.set("1x")
        self.cb.place(x=615, y=269)

        self.show_img_btn = Button(self.top, text='show', font='consolas 16 bold', fg="#FFF", bg="#001", width=4,
                                   bd=3, command=self.show_img_fun)
        self.show_img_btn.place(x=702, y=265)

        self.cam_img = PhotoImage(file='icon_image/cam1.png')
        self.cam_button = Button(self.top, image=self.cam_img, bg='#FFF', borderwidth=0, command=self.realtimetest)
        self.cam_button.place(x=700, y=322)

        #@____________________________________ Bottom design _____________________________________@#

        scroll = Scrollbar(self.bottom)
        scroll.pack(side=RIGHT,fill=Y)
        self.text = Text(self.bottom, font='Consolas 15 bold', wrap=WORD, padx=10, pady=10, bd=2,
                        yscrollcommand=scroll.set,bg="#ececec")
        self.text.pack()
        scroll.config(command=self.text.yview)



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  -x- Functions -x- @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

    def preProcessing(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(img)
        img = img / 255
        return img


    # prediction function
    def submit_fun(self):
        if self.path!='' and self.path!="()":
            name_of_item = self.auto_value[2].replace('/', '_')
            name_of_item = name_of_item.split('_')
            current_item = name_of_item[1] + " " + name_of_item[2]
            item_full_info = pd.read_csv('hidden_info.csv', squeeze=True)
            self.item_full_info = item_full_info[item_full_info["item"] == current_item]

            self.catagory = list(self.item_full_info["class"])
            self.pickle_in = open("" + self.auto_value[2], "rb")
            self.model = pickle.load(self.pickle_in)

            pg = PSS2()

            self.imgOriginal = cv2.imread(self.path)
            self.img = np.asarray(self.imgOriginal)
            self.img = cv2.resize(self.img, (32, 32))
            self.img = self.preProcessing(self.img)

            self.img = self.img.reshape(1, 32, 32, 1)
            self.class_id = int(self.model.predict_classes(self.img))

            self.predictions = self.model.predict(self.img)
            self.probVal = np.amax(self.predictions)

            self.probVal = Decimal(float(self.probVal * 100))
            self.probVal = round(self.probVal, 2)
            self.ac = str(self.probVal)

            print(self.class_id, " catagory = ", self.catagory[self.class_id])
            self.disease_val.set(self.catagory[self.class_id])
            self.acc_val.set(self.ac + "%")

            show_img_size = self.cb.get().split('x')
            show_img_size = float(show_img_size[0])
            self.imgOriginal = cv2.resize(self.imgOriginal, (int(self.imgOriginal.shape[1] * show_img_size),
                                                             int(self.imgOriginal.shape[0] * show_img_size)))
            if self.probVal > 0.65:
                cv2.putText(self.imgOriginal, str(self.catagory[self.class_id]), (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 12, 255), 2)
                cv2.putText(self.imgOriginal, "acc = " + self.ac + '%', (5, 120), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 255), 2)

            cv2.imshow("Original Image", self.imgOriginal)
            cv2.waitKey(5000)
            if cv2.waitKey(1) == 13:
                cv2.destroyAllWindows()
            cv2.destroyAllWindows()

        else:
            messagebox.showerror("Some error", "You haven\'t choose any image")

    def get_file(self):
        dir = filedialog.askopenfilename(parent=self,title='Choose a file')
        self.path = str(dir)
        self.entry_val.set(self.path)

    def clear_fun(self):
        self.text.delete(1.0, END)
        # print(self.path)

    def solution(self):
        self.text.delete(1.0, END)

        self.sol = list(list(self.item_full_info["sol"]))
        no_comma_str = self.sol[self.class_id].replace('#',',')
        string_t = ''
        for i in no_comma_str.split('@'):
            string_t +=i+'\n'

        self.text.insert(INSERT,string_t)

    def symptoms(self):
        self.text.delete(1.0, END)

        self.sol = list(list(self.item_full_info["symptom"]))
        no_comma_str = self.sol[self.class_id].replace('#',',')
        string_t = ''
        for i in no_comma_str.split('@'):
            string_t +=i+'\n'

        self.text.insert(INSERT,string_t)


    def show_img_fun(self):

        if self.path!='' and self.path!="()":
            show_img_size = self.cb.get().split('x')
            show_img_size = float(show_img_size[0])
            self.img = cv2.imread(self.path)
            self.img = cv2.resize(self.img, (int(self.img.shape[1] * show_img_size),
                                                             int(self.img.shape[0] * show_img_size)))
            cv2.imshow("Your selected image",self.img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showerror("Some error","You haven\'t choose any image")

    def realtimetest(self):
        name_of_item = self.auto_value[2].replace('/', '_')
        name_of_item = name_of_item.split('_')
        current_item = name_of_item[1] + " " + name_of_item[2]
        item_full_info = pd.read_csv('hidden_info.csv', squeeze=True)
        self.item_full_info = item_full_info[item_full_info["item"] == current_item]

        self.catagory = list(self.item_full_info["class"])
        self.pickle_in = open("models/apple_fruit_Model.p", "rb")
        self.model = pickle.load(self.pickle_in)

        self.cap = cv2.VideoCapture(0)
        while True:
            success,self.imgOriginal = self.cap.read()
            self.img = np.asarray(self.imgOriginal)
            self.img = cv2.resize(self.img, (32, 32))
            self.img = self.preProcessing(self.img)

            self.img = self.img.reshape(1, 32, 32, 1)
            self.class_id = int(self.model.predict_classes(self.img))

            self.predictions = self.model.predict(self.img)
            self.probVal = np.amax(self.predictions)

            self.probVal = Decimal(float(self.probVal * 100))
            self.probVal = round(self.probVal, 2)
            self.ac = str(self.probVal)
            self.disease_val.set(self.catagory[self.class_id])
            self.acc_val.set(self.ac + "%")

            if self.probVal > 0.65:
                cv2.putText(self.imgOriginal, str(self.catagory[self.class_id]), (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 12, 255), 2)
                cv2.putText(self.imgOriginal, "acc = " + self.ac + '%', (5, 120), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 255), 2)

            cv2.imshow("Original Image", self.imgOriginal)
            if cv2.waitKey(1) == 13:
                break
        self.cap.release()
        cv2.destroyAllWindows()

