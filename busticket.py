import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3
import time

headlabelfont = ("Calibri", 15, 'bold')
labelfont = ('Calibri', 14)
entryfont = ('Calibri', 12)


connector = sqlite3.connect('busbooking.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS BUS_DATA (TICKET_NUMBER INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, DOD TEXT, DESTINATION, FARE TEXT)"
)

def reset_fields():
   global name_strvar, email_strvar, contact_strvar, dod, destination_strvar, fare_strvar, seats_strvar

   for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'destination_strvar', 'fare_strvar', 'seats_strvar']:
       exec(f"{i}.set('')")
   dod.set_date(datetime.datetime.now().date())


def reset_form():
   global tree
   tree.delete(*tree.get_children())

   reset_fields()


def display_records():
   tree.delete(*tree.get_children())

   curr = connector.execute('SELECT * FROM BUS_DATA')
   data = curr.fetchall()

   for records in data:
       tree.insert('', END, values=records)

def add_record():
   global name_strvar, email_strvar, contact_strvar, dod, destination_strvar, fare_strvar, seats_strvar

   name = name_strvar.get()
   email = email_strvar.get()
   contact = contact_strvar.get()
   DOD = dod.get_date()
   destination = destination_strvar.get()
   fare = fare_strvar.get()
   seats = seats_strvar.get()
   
   if not name or not email or not contact or not DOD or not destination or not fare:
       mb.showerror('Error!', "Please fill all the missing fields!!")
   else:
       try:
           connector.execute(
           'INSERT INTO BUS_DATA (NAME, EMAIL, PHONE_NO, DOD, DESTINATION, FARE) VALUES (?,?,?,?,?,?)', (name, email, contact, DOD, destination, fare)
           )
           connector.commit()
           mb.showinfo('Record added', f"Record of {name} was successfully added")
           reset_fields()
           display_records()
       except:
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')

 
def remove_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]

       tree.delete(current_item)

       connector.execute('DELETE FROM BUS_BOOKING WHERE TIKCET_NUMBER=%d' % selection[0])
       connector.commit()

       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

       display_records()


def view_record():
   global name_strvar, email_strvar, contact_strvar, dod, destination_strvar, fare_strvar, seats_strvar

   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]

   date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))

   name_strvar.set(selection[1]); email_strvar.set(selection[2])
   contact_strvar.set(selection[3]); destination_strvar.set(selection[4])
   dod.set_date(date); fare_strvar.set(selection[6])
   seats_strvar.set(selection[8])


def overallsales():
    connector = sqlite3.connect('busbooking.db')
    cursor = connector.cursor()

    cursor.execute("SELECT SUM(fare) AS total_amount FROM BUS_DATA")
    result = cursor.fetchone()
    total_amount = result[0]

    mb.showinfo("Total Amount", "Overall total sales is: PHP " + str(total_amount) + '.00')


main = Tk()
main.title('BUS BOOKING SYSTEM')
main.geometry('1300x600')
main.resizable(0, 0)

lf_bg = '#6666CD' # bg color for the left_frame
cf_bg = '#7676EE' # bg color for the center_frame

name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
destination_strvar = StringVar()
fare_strvar = StringVar()
time_strvar = StringVar()
seats_strvar = StringVar()

Label(main, text="BUS BOOKING SYSTEM", font=headlabelfont, bg='#5F5F9E', fg='LightCyan').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

Label(left_frame, text="Name", font=labelfont, bg=lf_bg, ).place(relx=0.375, rely=0.002)
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.10)
Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.21)
Label(left_frame, text="Date of Departure", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.47)
Label(left_frame, text="Destination", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.33)
Label(left_frame, text="Fare", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.6)
Label(left_frame, text="Seats", font=labelfont, bg=lf_bg).place(x=50, rely=0.70)


Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=50, rely=0.05)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=50, rely=0.15)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=50, rely=0.26)
Entry(left_frame, width=19, textvariable=fare_strvar, font=entryfont).place(x=50, rely=0.65)
OptionMenu(left_frame, destination_strvar, 'Baguio (BUS NO.1)', 'Ifugao (BUS NO.2)', 'Nueva Vizcaya (BUS NO.3').place(x=50, rely=0.39, relwidth=0.5)
Entry(left_frame, width=19, textvariable=seats_strvar, font=entryfont).place(x=50, rely=0.75)


dod = DateEntry(left_frame, font=("Arial", 12), width=15)
dod.place(x=50, rely=0.52)

seats = ["A1", "A2", "A3", "A4", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"
"B9", "B10", "B11", "B12"]

def reserve_seat():
    selected_seat = seat_var.get()
    if selected_seat in seats:
        seats.remove(selected_seat)
        mb.showinfo("Seat Reservation", "Seat reserved!")
    else:
        mb.showinfo("Seat Reservation", "Seat not available")

seat_var = StringVar(value="availabe seats")
OptionMenu(center_frame, seat_var, *seats).place(relx=0.20, rely=0.50)

reserve_button = Button(center_frame, text="Reserve", command=reserve_seat).place(relx=0.27, rely=0.56) 

Button(left_frame, text='Confirm Boooking', font=labelfont, command=add_record, width=24).place(relx=0.015, rely=0.85)

Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.10)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.20)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.30)
Button(center_frame, text='Total Sales', font=labelfont, command=overallsales, width=15).place(relx=0.1, rely=0.40)

class Clock:
    def __init__(self):
        self.time1 = ''
        self.time2 = time.strftime('%H:%M:%S %p  %A  %x')
        self.mFrame = Frame()
        self.mFrame.pack(side=BOTTOM,expand=NO,fill=X)

        self.watch = Label(self.mFrame, text=self.time2, font=('Arial',10,'bold'))
        self.watch.pack()

        self.changeLabel() #first call it manually

    def changeLabel(self): 
        self.time2 = time.strftime('%H:%M:%S %p  %A  %x')
        self.watch.configure(text=self.time2)
        self.mFrame.after(1500, self.changeLabel) #it'll call itself continuously

Label(right_frame, text='BOOKING DETAILS', font=headlabelfont, bg='#7A7AC5', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=("Ticket Number", "Name", "Email Address", "Contact Number", "Date of Departure", "Destination", "Fare", "Seats"))


tree.heading('Ticket Number', text='Ticket', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Date of Departure', text='Departure', anchor=CENTER)
tree.heading('Destination', text= 'Destination', anchor=CENTER)
tree.heading('Fare', text= 'Fare', anchor=CENTER)
tree.heading('Seats', text='Seats', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=100, stretch=NO)
tree.column('#6', width=150, stretch=NO)
tree.column('#7', width=40, stretch=NO)
tree.column('#8', width=40, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()


Clock()
main.update()
main.mainloop()