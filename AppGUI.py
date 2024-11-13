# Imports
from tkinter import messagebox
import tkinter as tk
import mysql.connector
from dbClass import *
from tkinter import filedialog
import smtplib

# Class to create tkinter window
class GUI:

    # All fields are safely initialized
    def __init__(self):
        
        # Loading the passwords from the database
        self.password_list = ContactDb.loadPasses(self)

        # Making a login window
        authentication  = tk.Tk()
        authentication.geometry("200x200")
        authentication.resizable(False,False)
        authentication.title("AUTHENTICATION")
        self.authentication = authentication

        # Window Icon
        self.securityIcon = tk.PhotoImage(file=r"\download-removebg-preview.png")
        self.authentication.wm_iconphoto(False, self.securityIcon)

        self.authenticationLbl = tk.Label(authentication,text="LOGIN")
        self.authenticationLbl.pack(pady=5)

        self.usernameLbl = tk.Label(authentication,text="Username")
        self.usernameLbl.pack(pady=5)

        self.usernameBox= tk.Entry(authentication)
        self.usernameBox.pack(pady=5)

        self.passcodeLbl = tk.Label(authentication,text="Password")
        self.passcodeLbl.pack(pady=5)

        self.passcodeBox= tk.Entry(authentication)
        self.passcodeBox.pack(pady=5)

        # self.authenticate checks the username and passcode user has provided
        self.signinBtn = tk.Button(authentication,text="Sign In", command=self.authenticate)
        self.signinBtn.pack(pady=5)

        # Initializing username, password, self.valid_login determines whether the main application opens
        self.username = self.password_list[2]
        self.passcode = self.password_list[1]
        self.valid_login = None

        self.authentication.mainloop()

        # If username and password are valid, open the app
        if (self.valid_login):
        
            # Making and adjusting the tk window
            application = tk.Tk()
            application.geometry('720x600')
            application.title("Section 9 Contact Management Program")
            application.configure(bg="white")
            application.resizable(False, False)
            self.application = application

            # Window icon
            icon = tk.PhotoImage(file=r"")
            self.application.wm_iconphoto(False, icon)

            # Make sure it is stored in memory, this is where records are stored
            self.records = []
            self.postRecordEval = []

            # Bool for database connection (False at beginning because user has not connected yet) and other toggle buttons
            self.commit = False
            self.connected = False
            self.update = False

            # Making the menu for the application
            appMenu = tk.Menu(application)

            # Submenu within main menu
            helpMenu = tk.Menu(appMenu, tearoff=0)
            helpMenu.add_command(label="How to Use", command=self.openHelpMenu)
            helpMenu.add_command(label="About", command=self.openAboutMenu)

            # Making a settings menu
            settings = tk.Menu(appMenu, tearoff=0)

            # Adding a theme submenu to the settings menu
            theme = tk.Menu(settings, tearoff=0)
            theme.add_command(label="Light Mode", command=self.light_mode)
            theme.add_command(label="Dark Mode", command=self.dark_mode)
            settings.add_cascade(label="Theme", menu=theme)
            settings.add_command(label="Copy Current Contact", command=self.copyCurrentContact)
            settings.add_command(label="Export all contacts",command=self.exportAllContacts)
            settings.add_command(label="See Password Info",command=self.passwordInfoWindow)
            settings.add_command(label="Database Info",command=self.databaseInfoWindow)
            settings.add_command(label="Feedback",command=self.feedbackWindow)
            settings.add_separator()
            settings.add_command(label="EXIT",command=self.exitTheApp)

            # Adding settings and help to the menubar
            appMenu.add_cascade(label="Settings", menu=settings)
            appMenu.add_cascade(label="Help", menu=helpMenu)

            # Putting the Menu in
            application.config(menu=appMenu)

            # Widgets that will allow the user to interact with the GUI
            self.mainlbl = tk.Label(application, text="Contacts Management", font=("bahnschrift", 20), bg="white")
            self.mainlbl.pack(pady=20)

            # First name text label
            self.firstNameLbl = tk.Label(application, text="First Name", font=("georgia", 14), bg="white")
            self.firstNameLbl.pack(pady=10)

            # Displays first name from db
            self.firstNameBox = tk.Text(application, width=20, height=1, bg="#d9e3ec", font=("georgia", 15))
            self.firstNameBox.pack(pady=7)

            # Last name text label
            self.lastNameLbl = tk.Label(application, text="Last Name", font=("georgia", 14), bg="white")
            self.lastNameLbl.pack(pady=10)

            # last name from record displayed here
            self.lastNameBox = tk.Text(application, width=20, height=1, bg="#d9e3ec", font=("georgia", 15))
            self.lastNameBox.pack(pady=7)

            # Says phone num
            self.phoneNumLbl = tk.Label(application, text="Phone Number", font=("georgia", 14), bg="white")
            self.phoneNumLbl.pack(pady=10)

            # Displayed here
            self.phoneNumBox = tk.Text(application, width=20, height=1, bg="#d9e3ec", font=("georgia", 15))
            self.phoneNumBox.pack(pady=7)
            
            # Says Email
            self.emailLbl = tk.Label(application, text="Email", font=("georgia", 14), bg="white")
            self.emailLbl.pack(pady=10)

            # Displayed here (email)
            self.emailBox = tk.Text(application, width=25, height=1, bg="#d9e3ec", font=("georgia", 15))
            self.emailBox.pack(pady=7)

            # Creating a Frame within the window to place the connect, etc buttons
            self.btnFrame = tk.Frame(application)
            self.btnFrame.place(x=20, y=500)

            # Connect to database (toggle button)
            self.connectBtn = tk.Button(self.btnFrame, text="Connect", command=self.connectionManager, width=10, height=2)
            self.connectBtn.grid(row=13, column=0, padx=10, pady=10)

            # User adds a contact
            self.addContactBtn = tk.Button(self.btnFrame, text="Add New", command=self.addContact, width=10, height=2)
            self.addContactBtn.grid(row=13, column=1, padx=10, pady=10)
            
            # Move back one record
            self.previousContactBtn = tk.Button(self.btnFrame, text="Prev. Contact", command=self.prevRecord, width=12, height=2)
            self.previousContactBtn.grid(row=13, column=2, padx=10, pady=10)

            # Move to next record
            self.nextBtn = tk.Button(self.btnFrame, text="Next Contact", command=self.nextRecord, width=12, height=2)
            self.nextBtn.grid(row=13, column=3, padx=10, pady=10)

            # Delete record
            self.delBtn = tk.Button(self.btnFrame, text="Delete Contact", command=self.delContact, width=14, height=2)
            self.delBtn.grid(row=13, column=4, padx=10, pady=10)

            # Update the current record
            self.updateBtn = tk.Button(self.btnFrame, text="Update Contact", command=self.updates,width=14,height=2)
            self.updateBtn.grid(row=13,column=5,padx=10,pady=10)

            # The x close button that is there becaues of the window mananger instead of tk is disabled, user is then forced to use my exit command in the menu
            application.protocol("WM_DELETE_WINDOW", self.doNothing)

            self.application.mainloop()


    # Do nothing (used in testing)
    def doNothing(self):
        pass
    
    # Turn on dark mode
    def dark_mode(self):
        self.application.configure(bg="#303034")
        self.mainlbl.configure(bg="#303034", fg="white")
        self.firstNameLbl.configure(fg="white", bg="#303034")
        self.lastNameLbl.configure(fg="white", bg="#303034")
        self.phoneNumLbl.configure(fg="white", bg="#303034")
        self.emailLbl.configure(fg="white", bg="#303034")

    # Turn on light mode
    def light_mode(self):
        self.application.configure(bg="white")
        self.mainlbl.configure(bg="white", fg="black")
        self.firstNameLbl.configure(bg="white", fg="black")
        self.lastNameLbl.configure(bg="white", fg="black")
        self.phoneNumLbl.configure(bg="white", fg="black")
        self.emailLbl.configure(bg="white", fg="black")

    


    # To handle the connection
    def connectionManager(self):
        
        # Try this
        try: 
            # if self.connected is equal to false
            if(not self.connected):

                # Database class method to connect, feeding in passcode from the password manager
                ContactDb.connect(self,self.password_list[0])

                # Switch the boolean for the toggle
                self.connected = True
                self.connectBtn.config(text="Disconnect")

                # Message for the user
                messagebox.showinfo(title="Database Connection", message="Connected to database")

                # Load first record into window
                self.load()


            # if self.connected == True
            else:

                # Switch for toggle
                self.connected = False
                self.connectBtn.config(text="Connect")

                # Disconnect
                ContactDb.disconnect(self)

                # Clear the text boxes and records list
                self.clearBox()
                self.records.clear()
                self.postRecordEval.clear()

                # Message for user
                messagebox.showinfo(title="Database disconnected", message="Disconnect from database")

        # If connection fails, message including the sql error will be displayed
        except mysql.connector.Error as err:
            messagebox.showwarning(title="Database Error", message=err)

    # User can add a contact (Crud)
    def addContact(self):

        # If self.commit is false
        if (not self.commit):

            # Clear the text boxes so user can fill in the new contact details
            self.clearBox()
            self.addContactBtn.configure(text="Commit")

            # For toggle functionality
            self.commit = True


        else:

            # After user has filled in details, get text from the boxes
            firstName = self.firstNameBox.get("1.0", "end-1c")
            lastName = self.lastNameBox.get("1.0", "end-1c")
            phoneNum = self.phoneNumBox.get("1.0", "end-1c")
            email = self.emailBox.get("1.0", "end-1c")

            # For toggle
            self.commit = False
            self.addContactBtn.configure(text="Add New")
            self.records.clear()

            # Try to insert values into the database
            try:
                ContactDb.create(self,firstName,lastName,phoneNum,email)

                # Message that the person has been added. {} adding person's name
                messagebox.showinfo(message="{} has been added to your contacts and database has been reloaded".format(firstName), title="Database Info")

                # loading once more
                self.load()

            # Error message + reload
            except mysql.connector.Error as err:
                messagebox.showwarning(title="Database Error", message=err)
                self.load()


    # User can delete a contact (cruD)
    def delContact(self):
        
        # Getting everything in the text boxes
        self.dltFirstName = self.firstNameBox.get("1.0", "end-1c")
        self.dltLastName = self.lastNameBox.get("1.0", "end-1c")
        self.dltPhoneNum = self.phoneNumBox.get("1.0", "end-1c")
        self.dltEmail = self.emailBox.get("1.0", "end-1c")

        # Finding the length of those ^
        self.lenFirstName = len(self.dltFirstName)
        self.lenLastName = len(self.dltLastName)
        self.lenPhoneNum = len(self.dltPhoneNum)
        self.lenEmail = len(self.dltEmail)

        # Deletion will occur only if the text fields are longer than 0 characters and if database is connected
        if (self.lenFirstName > 0 and self.lenLastName > 0 and self.lenPhoneNum > 0 and self.lenEmail > 0 and self.connected == True):

            # Building a confirmation window to make sure the user wants to delete the record
            self.confirmation = tk.Tk()
            self.confirmation.geometry("300x200")
            self.confirmation.resizable(False,False)
            self.confirmation.title("CONFIRMATION")        
            
            # Adding an attribute of the record in the confirmation message
            self.deleteLbl = tk.Label(self.confirmation, text="Must you delete {}?".format(self.dltFirstName))
            self.deleteLbl.pack()
            
            self.deleteBtn = tk.Button(self.confirmation, text="Delete", command=self.delRecord)
            self.deleteBtn.pack()

            self.cancelDltBtn = tk.Button(self.confirmation, text="Cancel", command=self.closeConfirmWindow)
            self.cancelDltBtn.pack()
            
            # Running it
            self.confirmation.mainloop()

        else:
            # if the text fields are empty or if self.connected = False
            messagebox.showwarning(title="Database Error", message="Not connected to database or no record selected")
        
    # Actual command to delete record, for button in confirmation window
    def delRecord(self):

        # It will send the text to the ContactDb class and from there the record will be deleted
        try:
            self.confirmation.destroy()
            ContactDb.delete(self, self.dltFirstName, self.dltLastName, self.dltPhoneNum, self.dltEmail)
            messagebox.showinfo(message="{} Successfully deleted. Database Reloaded".format(self.dltFirstName), title="Database Info")
            self.load()
        
        # If something goes wrong
        except mysql.connector.Error as err:
            messagebox.showwarning(title="Database Error", message=err)
            self.load()
        
    # To close the confirmation window for deletions, for cancel btn
    def closeConfirmWindow(self):
        self.confirmation.destroy()

    # Clear all text boxes, very useful
    def clearBox(self):
        self.firstNameBox.delete("1.0", "end-1c")
        self.lastNameBox.delete("1.0", "end-1c")
        self.phoneNumBox.delete("1.0", "end-1c")
        self.emailBox.delete("1.0", "end-1c")

    # Loading records on connect
    def load(self):
        
        # Clear boxes first
        self.clearBox()
        self.records.clear()
        self.postRecordEval.clear()
        self.Recnumber = ContactDb.getNumRecords(self)[0]


        # Setting self.NUMBER to 0, used when switching between records
        self.NUMBER = 0

        # Used in for loop below to append records to list
        num = 1

        # Appending records to self.records = [] in a for loop 
        for x in range(0,self.Recnumber):
            self.records.append(ContactDb.getRecord(self, num))
            num = num + 1

        # Filters the list for NoneType records and adds the real records to another list, self.postRecordEval = []
        for item in self.records:
            if (item != None):
                self.postRecordEval.append(item)

        # Taking the length and calibrating the highestIndex, it is the top index and once the last record is displayed the user wont be able to scroll to the next
        lenRecords = len(self.postRecordEval)
        self.NUMBERFIX = list(range(0,lenRecords))
        self.highestIndex = self.NUMBERFIX[-1]

        # Getting the values from 1st tuple in the list and displaying it to the user after connecting
        self.List = self.postRecordEval[self.NUMBER]
        self.insertFirstName = self.List[1]
        self.insertLastName = self.List[2]
        self.insertPhoneNum = self.List[3]
        self.insertEmail = self.List[4]
        self.firstNameBox.insert("insert", self.insertFirstName)
        self.lastNameBox.insert("insert", self.insertLastName)
        self.phoneNumBox.insert("insert", self.insertPhoneNum)
        self.emailBox.insert("insert", self.insertEmail)

    # User can switch between records (go forward)
    def nextRecord(self):


        # If record displayed on screen currently is of the highestIndex the user can't go any further
        if (self.NUMBER >= self.highestIndex or self.connected == False):
            self.doNothing() # Pass
            self.NUMBER = self.NUMBER

        # If it is lower than the highestIndex
        else:

            # Next record
            self.NUMBER = self.NUMBER + 1

            # Getting the next record and displaying after clearing the text boxes
            self.List = self.postRecordEval[self.NUMBER]
            self.clearBox()

            # Getting values from tuple (records are returned in tuples from database)
            self.insertFirstName = self.List[1]
            self.insertLastName = self.List[2]
            self.insertPhoneNum = self.List[3]
            self.insertEmail = self.List[4]
            self.firstNameBox.insert("insert", self.insertFirstName)
            self.lastNameBox.insert("insert", self.insertLastName)
            self.phoneNumBox.insert("insert", self.insertPhoneNum)
            self.emailBox.insert("insert", self.insertEmail)
            self.NUMBER = self.NUMBER
        

    # User can go to the previous record 
    def prevRecord(self):
        
        # If the index is lower than zero, user will not be able to go back further
        if (self.NUMBER <= 0 or self.connected == False):
            self.doNothing() # Pass
            self.NUMBER = self.NUMBER

        # Else, go back as regular
        else:
            self.NUMBER = self.NUMBER - 1

            # Choosing the previous record and clearing the text boxes before displaying
            self.List = self.postRecordEval[self.NUMBER]
            self.clearBox()
            self.insertFirstName = self.List[1]
            self.insertLastName = self.List[2]
            self.insertPhoneNum = self.List[3]
            self.insertEmail = self.List[4]
            self.firstNameBox.insert("insert", self.insertFirstName)
            self.lastNameBox.insert("insert", self.insertLastName)
            self.phoneNumBox.insert("insert", self.insertPhoneNum)
            self.emailBox.insert("insert", self.insertEmail)

    # (crUd) User can update displayed record
    def updates(self):
        
        # self.update for toggle functionality, only executes if connection exists
        if (not self.update and self.connected == True):

            # Getting values from text boxes
            updateFirstName = self.firstNameBox.get("1.0", "end-1c")
            updateLastName = self.lastNameBox.get("1.0", "end-1c")
            updatePhoneNum = self.phoneNumBox.get("1.0", "end-1c")
            updateEmail = self.emailBox.get("1.0", "end-1c")

            # Getting the id of the selected record
            self.identifier = (ContactDb.getId(self,updateFirstName,updateLastName,updatePhoneNum,updateEmail))[0]
            self.update = True
            self.updateBtn.config(text="Commit")

        else:
            
            # Trying to update
            try:

                # Getting values from boxes
                updateFirstName = self.firstNameBox.get("1.0", "end-1c")
                updateLastName = self.lastNameBox.get("1.0", "end-1c")
                updatePhoneNum = self.phoneNumBox.get("1.0", "end-1c")
                updateEmail = self.emailBox.get("1.0", "end-1c")
                self.updateBtn.config(text="Update Contact")
                self.update = False

                # ContactDb class does the job and message box sends a message that {firstName} is updated
                ContactDb.update(self, updateFirstName,updateLastName,updatePhoneNum,updateEmail, self.identifier)
                messagebox.showinfo(title="Database Update", message="{} updated. Disconnect, then reconnect to see updated records.".format(updateFirstName))

                # Reload and load after clearing lists
                self.load()

            # Something goes horribly wrong, message with error message from sql is sent
            except mysql.connector.Error as err:
                messagebox.showinfo(title="Database Error", message=err)
                self.load()

    # Open help menu
    def openHelpMenu(self):
        messagebox.showinfo(title="How to use",message="How to use. Connect to database to access you contacts. Click add new then type in details, press commit to add to database. Press update and change the record displayed, then press commit to update. MAY HAVE TO RELOAD DATABASE TO SEE UPDATED CONTACT. Press DELETE to delete. Have Fun!")

    def openAboutMenu(self):
        messagebox.showinfo(title="INFO",message="""VERSION 1.74387SJK354KLM33
CREATOR: SOHAMERSON""")

    # Exit app
    def exitTheApp(self):
        self.application.destroy()

    # Export the contact that is currently being displayed to the string
    def copyCurrentContact(self):

        # Getting the values of the record currently displayed
        exportFirstName = self.firstNameBox.get("1.0", "end-1c")
        exportLastName = self.lastNameBox.get("1.0", "end-1c")
        exportPhoneNum = self.phoneNumBox.get("1.0", "end-1c")
        exportEmail = self.emailBox.get("1.0", "end-1c")

        lenExportFirstName = len(exportFirstName)
        lenExportLastName = len(exportLastName)
        lenExportPhoneNum = len(exportPhoneNum)
        lenExportEmail = len(exportEmail)

        if (lenExportFirstName and lenExportLastName and lenExportPhoneNum and lenExportEmail > 0) and (self.connected == True):
            # Putting into clipboard
            self.application.clipboard_clear()
            self.application.clipboard_append(exportFirstName + ", ")
            self.application.clipboard_append(exportLastName + ", ")
            self.application.clipboard_append(exportPhoneNum + ", ")
            self.application.clipboard_append(exportEmail)

            # Letting the user know it has been copied
            messagebox.showinfo(title="Info", message="Contact copied to clipboard")

        else:
            messagebox.showwarning(title="ERROR", message="Not connected to database or text fields found empty")

    # Export them all by saving the list of records to a txt file
    def exportAllContacts(self):
        
        if (self.postRecordEval is not None) and (len(self.postRecordEval) > 0) and (self.connected == True):
            try:

                # Opens the save file dialog
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])

                # Checks to see that the user hasn't cancelled or file is empty
                if (file_path):
                    
                    # Opens the file in write mode, with makes sure the file is properly closed
                    with open(file_path,"w") as open_file:
                        
                        # Every record is appended to the text file
                        for record in self.postRecordEval:
                            open_file.write(str(record) + ", ")

                    # Letting the user know
                    messagebox.showinfo(title="Export Info",message="Saved to {}".format(file_path))

            # if something goes horribly wrong, send the error message to the user
            except Exception as err:
                messagebox.showwarning(title="Error",message=err)

        else:
            messagebox.showwarning(title="ERROR",message="No records available. Try connecting to database") 

    # Authentication
    def authenticate(self):

        # Getting the username and passcode user has typed
        user = self.usernameBox.get()
        password = self.passcodeBox.get()

        # if it matches up, let the user through
        if (user == self.username and password == self.passcode):
            self.valid_login = True
            self.authentication.destroy()
        
        # Else, give them an error message
        else:
            self.valid_login = False
            self.usernameBox.delete("0", "end")
            self.passcodeBox.delete("0", "end")
            messagebox.showwarning(title="ERROR", message="Incorrect username or password")

    def passwordInfoWindow(self):

        # Creating a window to display password info
        self.userPassword = tk.Tk()
        self.userPassword.geometry("200x200")
        self.userPassword.resizable(False,False)
        self.userPassword.title("Passcode Info")

        promptLbl = tk.Label(self.userPassword,text="Your passcode",font=("Georgia",16,"underline"))
        promptLbl.pack(pady=10)
        
        self.passwordLbl = tk.Label(self.userPassword,text=self.passcode,font=("Georgia", 20),bg="black",fg="white")
        self.passwordLbl.pack(pady=30)

        self.changeBtn = tk.Button(self.userPassword, text="Alter Password", command=self.updatePassWin)
        self.changeBtn.pack(pady=10)

        self.userPassword.mainloop()


    def databaseInfoWindow(self):

        # If database connection is true, create a window to display various pieces of information regarding the database
        if (self.connected):
            info = tk.Tk()
            info.geometry("200x200")
            info.resizable(False,False)
            info.title("DATABASE INFO")

            schemaLbl = tk.Label(info, text="Database: ")
            schemaLbl.pack(pady=10)

            hostLbl = tk.Label(info, text="Host: Local Host")
            hostLbl.pack(pady=10)

            self.code = tk.Label(info, text="********")
            self.code.pack(pady=10)

            # Hover attributes for the passcode label, when the cursor is over it it will show the passcode, otherwise it'll show *******
            self.code.bind("<Enter>",self.onHover)
            self.code.bind("<Leave>",self.offHover)

            tableLbl = tk.Label(info,text="Table: contacts")
            tableLbl.pack(pady=10)

            info.mainloop()

        else:
            messagebox.showinfo(title="ERROR",message="DATABASE NOT CONNECTED")
    
    # HOVER FUNCTIONS FOR DATABASE INFO WINDOW
    def onHover(self, event):
        self.code.config(text="",cursor="hand2")

    def offHover(self,event):
        self.code.config(text="", cursor="")

    def sendFeedbackEmail(self,msg,user):

        # Server host + port
        host_name = "smtp.gmail.com"
        port_num = 587

        # Some info
        from_email = ""
        to_email = ""
        password_email = self.password_list[3]

        # Message that will be sent + parameters
        message = """Subject: Feedback from user
Hi Soham,
        
{}
        
Thanks,
{}""".format(msg,user)

        # Store smtplob.SMPT class which takes two parameters into the object smtp, which we will act upon
        smtp = smtplib.SMTP(host=host_name,port=port_num)

        # .ehlo will ping the server and make sure all is up and running.
        smtp.ehlo()

        # Establish the tls connection with the server (to send mail securely)
        smtp.starttls()

        # Login to the server
        smtp.login(user=from_email,password=password_email)

        # Send the mail
        smtp.sendmail(from_email,to_email,message)

    
    def feedbackWindow(self):

        # Creating a little interface in which the user can send feedback
        self.feedback = tk.Tk()
        self.feedback.geometry("300x350")
        self.feedback.resizable(False,False)
        self.feedback.title("SEND FEEDBACK")

        self.from_who_lbl = tk.Label(self.feedback,text="User")
        self.from_who_lbl.pack(pady=10)

        # User types in their name here
        self.from_who_box = tk.Text(self.feedback, height=1,width=20)
        self.from_who_box.pack(pady=10)

        self.messageLbl = tk.Label(self.feedback,text="Your message")
        self.messageLbl.pack(pady=10)

        # User types in the message here
        self.message_box = tk.Text(self.feedback,width=20,height=10)
        self.message_box.pack(pady=10)

        sendBtn = tk.Button(self.feedback, command=self.sendIt, text="Send")
        sendBtn.pack(pady=10)

        self.feedback.mainloop()

    def sendIt(self):

        # Gets the text values
        sender = self.from_who_box.get("1.0","end-1c")
        message = self.message_box.get("1.0","end-1c")

        # Length of those values
        lenSenderName = len(sender)
        lenMessage = len(message)

        # if the fields aren't empty it will proceed to send the email through self.sendFeedbackEmail
        if (lenSenderName > 0) and (lenMessage > 0):

            try:

                # Send the message
                self.sendFeedbackEmail(message,sender)
                self.feedback.destroy()
                messagebox.showinfo(title="SUCCESS",message="Feedback Sent, thanks.")

            # If something goes wrong such as no internet connection
            except Exception as err:
                messagebox.showinfo(title="ERROR",message=err)
                self.feedback.destroy()

        else:

            # If fields are found to be empty
            messagebox.showwarning(title="ERROR",message="Fill both fields please")

    # When the user presses alter button this window will pop up and it will provide an interface to change the passcode
    def updatePassWin(self):

        # Destroys the show password window
        self.userPassword.destroy()

        self.changePswdWin = tk.Tk()
        self.changePswdWin.geometry("300x200")
        self.changePswdWin.resizable(False,False)
        self.changePswdWin.title("CHANGE PASSWORD")

        self.change_lbl = tk.Label(self.changePswdWin, text="Type in new password")
        self.change_lbl.pack(pady=15)

        self.change_box = tk.Entry(self.changePswdWin, width=25)
        self.change_box.pack(pady=15)

        self.alter_pass_btn = tk.Button(self.changePswdWin,text="Alter",command=self.updatePass)
        self.alter_pass_btn.pack(pady=10)

        self.changePswdWin.mainloop()

    # Button will execute this command
    def updatePass(self):

        # getting the password the user typed in
        var = self.change_box.get()

        # checks to see if the user actually did type in anything
        if (len(var) > 0):

            # if so, contacts the database and updates the password
            ContactDb.changePass(self,var)

            self.changePswdWin.destroy()

            # Resets self.passcode
            self.passcode = ContactDb.loadPasses(self)[1]

        else:
            # if user didn't type anything
            messagebox.showinfo(title="ERROR",message="Type in a new password")
