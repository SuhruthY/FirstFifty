import os
import datetime
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from dotenv import load_dotenv


## ---- Fetching the database ---
conn = sqlite3.connect("mycontacts.db")
cur = conn.cursor()


## --- GLOBAL VARIABLES ---
# loading all the variables
load_dotenv()

# get today's date
DATE = datetime.date.today()


## ---- Functions ----
# function that updates the database
def updt_contact():
    global my_updt, person_id, f_name_ntry, l_name_ntry, ph_no_ntry, email_ntry, address_ntry

    first_name, last_name, phone_no, email_ID, address = f_name_ntry.get(), l_name_ntry.get(), ph_no_ntry.get(), email_ntry.get(), address_ntry.get(1.0, "end-1c")

    print(person_id,first_name, last_name, phone_no, email_ID, address )
    [print(type(x)) for x in [person_id,first_name, last_name, phone_no, email_ID, address]]

    try:
        cur.execute(f""" Update People set First_Name = '{first_name}', Last_Name = '{last_name}', Phone_no = '{phone_no}',
        Email_ID = '{email_ID}', Address='{address}' where Person_ID='{person_id}'
        """)
        conn.commit()
        messagebox.showinfo("Sucess", "Contact updated")
        my_updt.destroy()
    except Exception as ex:
        messagebox.showerror("Error", str(ex), icon="warning")

# function to update existing contact
def update(cntct_id):
    global my_updt, person_id, f_name_ntry, l_name_ntry, ph_no_ntry, email_ntry, address_ntry

    my_updt = Toplevel()
    my_updt.title("My Contacts Book")
    my_updt.iconbitmap("./data/icons/contact-book.ico")
    my_updt.geometry(os.environ.get("GEOMETRY"))
    my_updt.resizable(False, False)

    # Create Main Frames
    header = Frame(my_updt, height=100, bg="white")
    header.pack(fill=X)
    base = Frame(my_updt, height=550, bg=os.environ.get("BABYBLUE"))
    base.pack(fill=X)

    # fetching data from database
    user_data = cur.execute(f""" Select * from People where Person_ID = {cntct_id}
    """).fetchone()
    person_id, first_name,last_name, phone_no, email_ID, address = (user_data[i] for i in range(6))

    # Create Main Frames
    # Designing Header Frame
    img = Image.open("./data/icons/reload.png")
    width, height = img.size
    img = img.resize((width // 8, height // 8), Image.ANTIALIAS)
    photoimg = ImageTk.PhotoImage(img)
    img_lbl = Label(header, image=photoimg, bg="white")
    img_lbl.image = photoimg
    img_lbl.place(x=120, y=15)

    heading = Label(header, text="Update Contact", font=os.environ.get("HELVI21"),
                    bg="White", fg=os.environ.get("PEACH"))
    heading.place(x=200, y=40)
    date = Label(header, text="Date: " + str(DATE), font=os.environ.get("ARIAl12"),
                 bg="White", fg=os.environ.get("PEACH"))
    date.place(x=530, y=70)

    # Designing Base Frame
    # Creating required labels
    f_name_lbl = Label(base, text="First Name:", font=os.environ.get("ARIAL12"), bg=os.environ.get("BABYBLUE"))
    l_name_lbl = Label(base, text="Last Name:", font=os.environ.get("ARIAL12"), bg=os.environ.get("BABYBLUE"))
    ph_no_lbl = Label(base, text="Phone Number:", font=os.environ.get("ARIAL12"), bg=os.environ.get("BABYBLUE"))
    email_lbl = Label(base, text="Email Address:", font=os.environ.get("ARIAL12"), bg=os.environ.get("BABYBLUE"))
    address_lbl = Label(base, text="Address:", font=os.environ.get("ARIAL12"), bg=os.environ.get("BABYBLUE"))

    f_name_lbl.place(x=40, y=40)
    l_name_lbl.place(x=40, y=80)
    ph_no_lbl.place(x=40, y=120)
    email_lbl.place(x=40, y=160)
    address_lbl.place(x=40, y=200)

    # Creating required entry boxes
    f_name_ntry = Entry(base, width=50, bd=2)
    l_name_ntry = Entry(base, width=50, bd=2)
    ph_no_ntry = Entry(base, width=50, bd=2)
    email_ntry = Entry(base, width=50, bd=2)
    address_ntry = Text(base, width=50, height=10, bd=2)

    f_name_ntry.place(x=150, y=40)
    l_name_ntry.place(x=150, y=80)
    ph_no_ntry.place(x=150, y=120)
    email_ntry.place(x=150, y=160)
    address_ntry.place(x=150, y=200)

    f_name_ntry.insert(0, first_name)
    l_name_ntry.insert(0, last_name)
    ph_no_ntry.insert(0, phone_no)
    email_ntry.insert(0, email_ID)
    address_ntry.insert(1.0, address)


    updt_prsn_btn = Button(base, text="Update Contact", width=15, font=os.environ.get("ARIAL12"),
                           command=updt_contact)
    updt_prsn_btn.place(x=150, y=400)
