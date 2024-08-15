# Imports
import mysql.connector


class ContactDb:
    
    # Connecting to the database in MySQL
    def connect(self, pswd):

            # Storing the database connection into the object mydb
            self.mydb = mysql.connector.connect(
                host="",
                user="",
                password=pswd,
                database=""
            )

            # Making the cursor
            self.myCursor = self.mydb.cursor(buffered=True)

            
    # Disconnect from the database
    def disconnect(self):
        self.mydb.close()

    # (Crud) Creating a new person/row in the sql table 
    def create(self, fn, ln, pn, em):   
        self.myCursor.execute("INSERT INTO contacts(FirstName, LastName, phoneNum, email) VALUES ('{}','{}',{},'{}');".format(fn,ln,pn,em))
        self.mydb.commit()

    # Deleting selected row from GUI from database
    def delete(self, fn,ln,pn,em):
        self.myCursor.execute("DELETE FROM contacts WHERE FirstName = '{}' AND LastName = '{}' AND phoneNum = {} AND email = '{}';".format(fn,ln,pn,em))
        self.mydb.commit()

    # Get the max id from table
    def getNumRecords(self):
        self.myCursor.execute("SELECT max(Id) FROM contacts;")
        self.mydb.commit()
        return self.myCursor.fetchall()[0]

    # Get record based on Id  
    def getRecord(self,num):
        self.myCursor.execute("SELECT * FROM contacts WHERE Id = {};".format(num))
        self.mydb.commit()
        for x in self.myCursor:
            return x

    # Getting Id of a record
    def getId(self, var1,var2,var3,var4):
        self.myCursor.execute("SELECT Id FROM contacts WHERE FirstName = '{}' AND LastName = '{}' AND phoneNum = {} AND email = '{}';".format(var1,var2,var3,var4))
        self.mydb.commit()
        return self.myCursor.fetchall()[0]
    
   #  Updating a record
    def update(self, var1,var2,var3,var4,Id):
        self.myCursor.execute("UPDATE contacts SET FirstName = '{}' WHERE Id = {};".format(var1,Id))
        self.myCursor.execute("UPDATE contacts SET LastName = '{}' WHERE Id = {};".format(var2,Id))
        self.myCursor.execute("UPDATE contacts SET phoneNum = {} WHERE Id = {};".format(var3,Id))
        self.myCursor.execute("UPDATE contacts SET email = '{}' WHERE Id = {};".format(var4,Id))
        self.mydb.commit()

    # Connecting to the password database
    def loadPasses(self):

        # Storing the database connection into the object mydb2
        self.mydb2 = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Omsai01*",
            database="pythonPasses"
        )

        # Making the cursor
        self.myCursor2 = self.mydb2.cursor(buffered=True)

        # Pulling the passwords and returning to the GUI
        self.myCursor2.execute("SELECT dbPass, contactsPass, contactsUser, emailPass FROM password WHERE Id = 1;")
        self.mydb2.commit()
        return self.myCursor2.fetchall()[0]
    
    # User can change the login password
    def changePass(self, pswd):
        self.myCursor2.execute("UPDATE password SET contactsPass = '{}' WHERE Id = 1;".format(pswd))
        self.mydb2.commit()
    
    
