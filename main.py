from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
Y_ORANGE="#ffd59e"
BLUE="#4700d8"
NEON_GREEN="#06ff00"
FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter= [random.choice(letters) for letter in range(random.randint(8,10))]

    password_symbols= [random.choice(symbols) for symbol in range (random.randint(2,4))]

    password_number= [random.choice(numbers)for number in range (random.randint(2,4))]

    password_list= password_letter + password_symbols + password_number
    random.shuffle(password_list)

    password ="".join (password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password )
    pyperclip.copy(password)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website= website_entry.get()
    email=email_entry.get()
    password= password_entry.get()

    new_data= {website:
               {"email": email,
                "password" :password,
                }}
    with open("email_data.txt", "w") as email_use:
        email_use.write(email)

    if not website or not email or not password:
        messagebox.showwarning(title="Empty entry", message="Please don't leave any field empty !")

    else:
        try:
             with open("data.json", "r") as file:
                 #read old data
                 data= json.load(file)

        except FileNotFoundError:
             with open("data.json", "w") as file:
               #saving the new data
               json.dump(new_data,file,indent = 4)

        else:
             # update old data with new data
             data.update(new_data)
             with open("data.json", "w") as file:
                   # saving the new data
                   json.dump(data, file, indent=4)

        finally:
             website_entry.delete(0, "end")
             password_entry.delete(0,"end")




##################----------------- SEARCH WEBSITE DATA--------############
def search_web_data():
    website_search= website_entry.get()
    try:
        with open("data.json", "r") as file:
            web_data= json.load(file)
    except FileNotFoundError:
           messagebox.showerror(title="Data Not Found", message="No Data File Found")
    else:
        if website_search in web_data:
           email_use = (web_data[website_search]["email"])
           password_use = (web_data[website_search]["password"])
           messagebox.showinfo(title=f"{website_search} info", message=f"Email:{email_use}\n Password:{password_use}")
        else:
            messagebox.showerror(title="Website Data Not Found", message=f"No Data for {website_search} exist.\n Please try again, website entry is case sensitive")


###----EMAIL SAVER TO EMAIL-ENTRY---###
def email_save():
  try:
      with open ("email_data.txt","r") as file:
          email_use= file.readlines()
          email_entry.insert(0,email_use)
  except FileNotFoundError:
      email_entry.insert(0, "@gmail.com")
      with open("email_data.txt","w") as file:
          if email_entry.get()!="":
             email = email_entry.get()
             file.write(email)










# ---------------------------- UI SETUP ------------------------------- #
window= Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg="white")
canvas= Canvas(height=200, width=200, bg="white")
lock_image= PhotoImage(file='logo.png')
canvas.create_image(100,100, image= lock_image, anchor="center")
canvas.grid(row=0, column=1)

##----website---###

website_label= Label(width=15, text="Website:", font=(FONT_NAME, 12, "normal"), bg="white")
website_label.grid(row=1, column=0)

website_entry= Entry(width=45, fg= BLUE)
website_entry.grid(row=1, column=1, columnspan= 2)
website_entry.focus()

#### ---- email/username---###

email_label= Label(width=15, text="Email/Username:",font=(FONT_NAME, 12, "normal"), bg="white")
email_label.grid(row=2, column=0, columnspan=1)

email_entry= Entry(width= 45, fg= NEON_GREEN)
email_entry.grid(row=2, column=1, columnspan=2)
email_save()

###---password---###
password_label= Label(text="Password:", font=(FONT_NAME, 12, "normal"), bg="white")
password_label.grid(row=3, column=0)


password_entry= Entry(width= 34, text="Enter password here", fg=NEON_GREEN)
password_entry.grid(row=3, column=1, columnspan=1)

generate_password= Button(width=7, text="Generate", font=("Comic", 10, "normal"), bg="white", fg=BLUE,command=generate_password)
generate_password.grid(row=3, column=2,columnspan=1)

#save or search data

save_data= Button(width=7, text="Save", font=("Comic", 10, "normal"), bg="white", fg=RED, highlightthickness=0, command=save)
save_data.grid(row=4, column=2, columnspan=1)

search_data= Button(width=25, text="Find Website Data", font= ("Comic", 10, "normal"), bg="white", fg=RED, highlightthickness=0,command= search_web_data)
search_data.grid(row=4,column=1)

window.mainloop()