from tkinter import Tk, Label, Frame, Entry, Button, messagebox
from tkinter.ttk import Combobox
from captcha_test import generate_captcha
from PIL import Image, ImageTk
import time, random
from table_creation import generate
from email_test import send_openacn_ack
import sqlite3

# Create table if not exists
generate()

# ----------------- DATETIME LABEL -----------------
def show_dt():
    dt = time.strftime("%A %d-%b-%Y %r")
    dt_lbl.configure(text=dt)
    dt_lbl.after(1000, show_dt)

# ----------------- IMAGE SLIDESHOW -----------------
list_imgs = ['images/logo1.jpg', 'images/logo2.png', 'images/logo3.jpg', 'images/logo4.jpg', 'images/logo.jpg']
def image_animation():
    index = random.randint(0, 4)
    img = Image.open(list_imgs[index]).resize((250, 95))
    imgtk = ImageTk.PhotoImage(img, master=root)
    logo_lbl = Label(root, image=imgtk)
    logo_lbl.place(relx=0, rely=0)
    logo_lbl.image = imgtk
    logo_lbl.after(500, image_animation)

# ----------------- ROOT WINDOW -----------------
root = Tk()
root.state('zoomed')
root.configure(bg='pink')

title_lbl = Label(root, text="Banking Automation", fg='blue', bg='pink', font=('Arial', 50, 'bold', 'underline'))
title_lbl.pack()

dt_lbl = Label(root, font=('Arial', 15), bg='pink')
dt_lbl.pack(pady=5)
show_dt()

img = Image.open("images/logo.jpg").resize((250, 115))
imgtk = ImageTk.PhotoImage(img, master=root)

logo_lbl = Label(root, image=imgtk)
logo_lbl.place(relx=0, rely=0)
image_animation()

footer_lbl = Label(root, font=('Arial', 20, 'bold'), fg='blue', bg='pink', text="Developed By-\n Pankaj Rawat @8810431227")
footer_lbl.pack(side='bottom')

# ----------------- MAIN SCREEN -----------------
def main_screen():
    def refresh_captcha():
        new_captcha = generate_captcha()
        captcha_value_lbl.configure(text=new_captcha)

    frm = Frame(root, highlightbackground='brown', highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0, rely=.12, relwidth=1, relheight=.8)

    def forgot():
        frm.destroy()
        fp_screen()

    def new_user():
        frm.destroy()
        new_user_screen()

    def login():
        utype = acntype_cb.get()
        uacn = acnno_e.get()
        upass = pass_e.get()

        if utype == "Admin":
            frm.destroy()
            admin_screen()
        else:
            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'select * from accounts where acn_acno=? and acn_pass=?'
            curobj.execute(query, (uacn, upass))
            row = curobj.fetchone()
            if row == None:
                messagebox.showerror("Login", "Invalid ACN/PASS")
            else:
                frm.destroy()
                user_screen(row[0], row[1])

    acntype_lbl = Label(frm, text='ACN Type', font=('Arial', 20, 'bold'), bg='powder blue')
    acntype_lbl.place(relx=.3, rely=.1)

    acntype_cb = Combobox(frm, values=['User', 'Admin'], font=('Arial', 20, 'bold'))
    acntype_cb.current(0)
    acntype_cb.place(relx=.45, rely=.1)

    acnno_lbl = Label(frm, text='🔑ACN', font=('Arial', 20, 'bold'), bg='powder blue')
    acnno_lbl.place(relx=.3, rely=.2)

    acnno_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    acnno_e.place(relx=.45, rely=.2)
    acnno_e.focus()

    pass_lbl = Label(frm, text='🔒 Pass', font=('Arial', 20, 'bold'), bg='powder blue')
    pass_lbl.place(relx=.3, rely=.3)

    pass_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5, show='*')
    pass_e.place(relx=.45, rely=.3)

    captcha_lbl = Label(frm, text='Captcha', font=('Arial', 20, 'bold'), bg='powder blue')
    captcha_lbl.place(relx=.3, rely=.4)

    captcha_value_lbl = Label(frm, text=generate_captcha(), fg='green', font=('Arial', 20, 'bold'))
    captcha_value_lbl.place(relx=.45, rely=.4)

    refresh_btn = Button(frm, text="refresh 🔄", command=refresh_captcha)
    refresh_btn.place(relx=.6, rely=.4)

    captcha_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    captcha_e.place(relx=.45, rely=.5)

    submit_btn = Button(frm, text="Login", command=login, width=17, bg='pink', bd=5, font=('Arial', 20, 'bold'))
    submit_btn.place(relx=.45, rely=.6)

    fp_btn = Button(frm, text="Forgot Pass", command=forgot, bg='pink', bd=5, font=('Arial', 18, 'bold'))
    fp_btn.place(relx=.45, rely=.7)

    new_btn = Button(frm, text="New User", command=new_user, bg='pink', bd=5, font=('Arial', 18, 'bold'))
    new_btn.place(relx=.58, rely=.7)

# ----------------- FORGOT PASSWORD SCREEN -----------------
def fp_screen():
    frm = Frame(root, highlightbackground='brown', highlightthickness=2)
    frm.configure(bg='green')
    frm.place(relx=0, rely=.12, relwidth=1, relheight=.8)

    def back():
        frm.destroy()
        main_screen()

    back_btn = Button(frm, text="back", bg='pink', bd=5, font=('Arial', 20, 'bold'), command=back)
    back_btn.place(relx=0, rely=0)

    acnno_lbl = Label(frm, text='🔑ACN', font=('Arial', 20, 'bold'), bg='powder blue')
    acnno_lbl.place(relx=.3, rely=.2)

    acnno_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    acnno_e.place(relx=.45, rely=.2)
    acnno_e.focus()

    email_lbl = Label(frm, text='📧Email', font=('Arial', 20, 'bold'), bg='powder blue')
    email_lbl.place(relx=.3, rely=.3)

    email_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    email_e.place(relx=.45, rely=.3)

    sub_btn = Button(frm, text="Submit", bg='pink', bd=5, font=('Arial', 20, 'bold'))
    sub_btn.place(relx=.5, rely=.4)

# ----------------- NEW USER SCREEN -----------------
def new_user_screen():
    frm = Frame(root, highlightbackground='brown', highlightthickness=2)
    frm.configure(bg='lightyellow')
    frm.place(relx=0, rely=.12, relwidth=1, relheight=.8)

    def back():
        frm.destroy()
        main_screen()

    back_btn = Button(frm, text="Back", command=back, bg='pink', bd=5, font=('Arial', 20, 'bold'))
    back_btn.place(relx=0, rely=0)

    Label(frm, text="New User Registration", font=('Arial', 25, 'bold'), bg='lightyellow', fg='blue').pack(pady=10)

    name_lbl = Label(frm, text='Name', font=('Arial', 20, 'bold'), bg='lightyellow')
    name_lbl.place(relx=.3, rely=.2)
    name_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    name_e.place(relx=.45, rely=.2)

    email_lbl = Label(frm, text='Email', font=('Arial', 20, 'bold'), bg='lightyellow')
    email_lbl.place(relx=.3, rely=.3)
    email_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    email_e.place(relx=.45, rely=.3)

    mob_lbl = Label(frm, text='Mobile', font=('Arial', 20, 'bold'), bg='lightyellow')
    mob_lbl.place(relx=.3, rely=.4)
    mob_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    mob_e.place(relx=.45, rely=.4)

    dob_lbl = Label(frm, text='DOB', font=('Arial', 20, 'bold'), bg='lightyellow')
    dob_lbl.place(relx=.3, rely=.5)
    dob_e = Entry(frm, font=('Arial', 20, 'bold'), bd=5)
    dob_e.place(relx=.45, rely=.5)

    def register():
        uname = name_e.get()
        uemail = email_e.get()
        umob = mob_e.get()
        udob = dob_e.get()
        upass = generate_captcha().replace(' ', '')
        uopendate = time.strftime("%A %d-%b-%Y")

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'insert into accounts values(null,?,?,?,?,?,?,?,?,?)'
        curobj.execute(query, (uname, upass, uemail, umob, '-', '-', udob, 0, uopendate))
        conobj.commit()
        curobj.execute("select max(acn_acno) from accounts")
        uacn = curobj.fetchone()[0]
        conobj.close()

        send_openacn_ack(uemail, uname, uacn, upass)
        messagebox.showinfo("Registration", "Account created successfully and details sent to your email.")
        frm.destroy()
        main_screen()

    submit_btn = Button(frm, text="Register", command=register, bg='lightgreen', bd=5, font=('Arial', 20, 'bold'))
    submit_btn.place(relx=.45, rely=.65)

# ----------------- START APP -----------------
main_screen()
root.mainloop()
