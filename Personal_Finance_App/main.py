#File name:     main.py
#Description:   Contains a personal finance management application. see documentation for more details
#Author(s):     Connor Weldy, Nozomu Ohno, Michael Laramie

#IMPORTS
import sys #for .ui files interacting with computer system
from PyQt5.uic import loadUi #for loading .ui files
from PyQt5 import QtCore, QtWidgets, QtGui #overaching qt widgets
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QMessageBox, QStackedWidget, QWidget, QVBoxLayout #for all the various qt widgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice #for Pie chart and other charts 
from PyQt5.QtGui import QPainter, QPen, QIcon #for Qt styling
from PyQt5.QtCore import Qt #for base level Qt functions and styling
from sqlfunctions import * #functions I created
from datetime import date, datetime #for managing dates

#######################
###-----CLASSES-----###
#######################

#Class Name: WelcomeScreen
#Inherits:   QDialog (from Qt library)
#Purpose:    object for a welcome screen. Uses welcomescreen.ui along with various
#            methods and functions to access other screens and functionality of the app
class WelcomeScreen(QDialog):
    #Constructor for Welcome Screen
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        #load welcomescreen user interface
        loadUi("./userinterfaces/welcomescreen.ui", self)

        #if Log In button is pressed execture function gotologin()
        self.buttonLogIn.clicked.connect(self.goToLogInScreen)

        #if Create New User button is clicked, execute function go to createnewuserscreen()
        self.buttonCreateNewUser.clicked.connect(self.goToCreateNewUserScreen)

    #Name:      goToLogInScreen
    #Purpose:   adds a login screen instance to the stacked widget, displays the login screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget  
    def goToLogInScreen(self):
        #creating instance of LoginScreen class
        login = LoginScreen()
        #adding instance to the stack
        widget.addWidget(login)
        #setting the index to the newly added instance
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    #Name:      goToLogInScreen
    #Purpose:   adds a create new user instance to the stacked widget, displays the create new user screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget 
    def goToCreateNewUserScreen(self):
        #creating instance of NewUserScreen class
        newUser = NewUserScreen()
        #adding instance to the stack
        widget.addWidget(newUser)
        #setting the index of the stack to the newly added instance in order to display that new instance
        widget.setCurrentIndex(widget.currentIndex()+1)

#Class Name: NewUserScreen
#Inherits:   QDialog (from Qt library)
#Purpose:    object for a new user screen. Uses newuser.ui along with various
#            methods and functions to access other screens and functionality of the app
class NewUserScreen(QDialog):
    #Constructor
    def __init__(self):
        super(NewUserScreen, self).__init__()
        #load newuserscreen user interface
        loadUi("./userinterfaces/newuser.ui", self)

        #Hide text for password field, built in QtWidget function
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        #Hide text for confirm password field, built in QtWidget function
        self.lineEditConfirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        #if create new user button is clicked, execute createUserFunc()
        self.buttonCreateNewUser.clicked.connect(self.createUserFunc)

        #if go to sign in button is clicked, execture goToLoginScreen()
        self.buttonGoToLogin.clicked.connect(self.goToLoginScreen)

    #Name:      goToLogInScreen 
    #Purpose:   adds a login screen instance to the stacked widget, displays the login screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget 
    def goToLoginScreen(self):
        #creating LoginScreen instance
        login = LoginScreen()
        #Adding instance to the stacked widget
        widget.addWidget(login)
        #Setting the instance to the newly added instance
        widget.setCurrentIndex(widget.currentIndex() + 1)

    #Name:      createUserFunc
    #Purpose:   inserts a new user into the Database Server, allowing a new log in
    #Args:      self
    #Returns:   void - new user is created, goes to log in screen
    def createUserFunc(self):
        #gathering user input and storing into variables
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        confirmPassword = self.lineEditConfirmPassword.text()
        email = self.lineEditEmail.text()
        firstName = self.lineEditFirstName.text()
        middleInitial = self.lineEditMiddleInitial.text()
        lastName = self.lineEditLastName.text()

        #Checking user input:
        if (len(username) == 0) or (len(password) == 0) or (len(confirmPassword) == 0) or (len(email) == 0) or \
        (len(firstName) == 0) or (len(lastName) == 0) :
            #if user did not enter information in all of the fields
            #display error
            self.labelError.setText("Missing required field.")
        
        else: #user entered information in all of the fields
            #excuting sql to determine if username already exists
            #sql for retrieveing password of the given user inputted username
            sqlUsername = "SELECT Username FROM Users WHERE Username = '" + username + "'"
            databaseUsername = "" #temporary username that will retrieve the username associated with the inputted username
            tupleUsername = executeSQL(sqlUsername)
            for row in tupleUsername: #parsing the cursor object
                databaseUsername = row.Username #set equal to the username
        
            #check if username already exists
            if len(databaseUsername) == 0: #username does not exist
                #then check if the passwords match
                if password == confirmPassword: #passwords match
                    #sql for retrieving the next userid
                    sqlID = "Select Max(Id) as userid From Users" #sql for getting the max userid number
                    tupleID = executeSQL(sqlID) #executing that sql
                    for row in tupleID: #parse through cursor
                        userId = row.userid #set equal to that id
                    userId += 1 #add one to that id to make a new unique user id
                    #sql for inserting the new user into the database
                    sqlInsert = "INSERT INTO Users (ID, Fname, Minit, Lname, Email, Username, Password) \
                        VALUES (" + str(userId) + ", '" + firstName + "', '" + middleInitial + "', '" + lastName + "', '" + email \
                        + "', '" + username + "', '" + password + "');"
                    insertSQL(sqlInsert) #executing the insert
                    self.goToLoginScreen() #now the user is created, go to the login screen
                else: #passwords dont match
                    #display error
                    self.labelError.setText("Passwords do not match.")
            else: #username already exists
                #display error message
                self.labelError.setText("Username already exists. Please try a different Username")
                
#Class Name: LoginScreen
#Inherits:   QDialog (from Qt library)
#Purpose:    object for a login screen. Uses login.ui along with various
#            methods and functions to access other screens and functionality of the app
class LoginScreen(QDialog):
    #Constructor
    def __init__(self):
        super(LoginScreen, self).__init__()
        #load login screen user interface
        loadUi("./userinterfaces/login.ui", self)

        #hide text for password field using built in QtWidget function
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        #Log in button is pressed, execute loginFunc()
        self.buttonLogIn.clicked.connect(self.loginFunc)

        #If create new user button is pressed, execute goto create new user
        self.buttonCreateNewUser.clicked.connect(self.goToCreateNewUserScreen)
    
    #Name:      goToCreateNewUserScreen 
    #Purpose:   adds a new user screen instance to the stacked widget, displays the new user screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget 
    def goToCreateNewUserScreen(self):
        #creating newuserscreen instance
        newUser = NewUserScreen()
        #adding instance to the stacked widget
        widget.addWidget(newUser)
        #setting the index to the newly added instance
        widget.setCurrentIndex(widget.currentIndex()+1)

    #Name:      goToAccountScreen 
    #Purpose:   adds an account screen instance to the stacked widget, displays the accounts screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def goToAccountScreen(self):
        #creating accout screen instance
        account = AccountScreen()
        #adding instance to the stacked widget
        widget.addWidget(account)
        #setting the index to the newly added instance
        widget.setCurrentIndex(widget.currentIndex()+1)

    #Name:      loginFunc 
    #Purpose:   Tests if a user entered correct information. if they did, then go to the accounts screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget if login successful, otherwise displays an error
    def loginFunc(self):
        #creating username and password variable. they equal the text inputted by the user from the lineEditUsername and lineEditPassword
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()

        #checking user inputs
        if (len(username) == 0) or (len(password) == 0) : #if user leaves username or password fields empty
            #display error message
            self.labelIncorrectField.setText("Missing username or password.")
        else: #user inputted info in both fields
            #sql for retrieveing password of the given user inputted username
            sqlPassword = "SELECT * FROM Users WHERE Username = '" + username + "'"
            tuplePassword = executeSQL(sqlPassword) #execute the sql statement
            dataBasePassword = "" #temp variable for the retrieved password
            for row in tuplePassword: #parse through the cursor object
                dataBasePassword = row.Password #set the temp variable to the password column of the row
                
            #checking if the username works for the password inputted
            if (len(dataBasePassword) == 0): #username does not exist
                #display an error
                self.labelIncorrectField.setText("Username/Password does not exist")
            else: #username password exists, compares password retrieved by database to the user inputted password
                if dataBasePassword == password: #correct password
                    #setting global user id to use on the next application screens
                    #sql fo getting the global user id
                    sqlID = "SELECT ID FROM Users WHERE Username = '" + username + "'"
                    tupleID = executeSQL(sqlID) #execute the sql
                    for row in tupleID: #parsing the cursor
                        global gUserId #used to modify a global variable
                        gUserId = row.ID #global variable set to the user id
                    #user is signed in and global used id is set. now login
                    self.goToAccountScreen() #go to new accounts screen
                else: #incorrect password
                    #display error
                    self.labelIncorrectField.setText("Incorrect password for username: " + username)

#Class Name: NewAccountPopUp
#Inherits:   QDialog (from Qt library)
#Purpose:    object for a new account pop up. Uses newAccount.ui along with various
#            methods and functions to access other screens and functionality of the app
class NewAccountPopUp(QDialog):
    #Constructor
    def __init__(self):
        super(NewAccountPopUp, self).__init__()
        #loading newaccount ui
        loadUi("./userinterfaces/newAccount.ui",self)
        
        #when new account button is clicked go to create new account function
        self.buttonCreateNewAccount.clicked.connect(self.createNewAccount)

    #Name:      createNewAccount
    #Purpose:   Tests whether inputted variables are within the domain of an account, if so inserts a new account
    #Args:      self
    #Returns:   inserts a new account in the database if user input satisfies the domain, otherwise displays error
    def createNewAccount(self):
        #retrieving user input and setting to variables 
        accountType = self.comboboxAccountType.currentText()
        accountName = self.lineEditAccountName.text()
        notes = self.lineEditDetails.text()
        
        #sql for retrieving the next account id to assign to the new account
        sqlaccountID = "Select Max(AccountID) as accountId From Accounts"
        tupleID = executeSQL(sqlaccountID) #execute the sql
        accountId = 0
        for row in tupleID: #parse the cursor object
            accountId = row.accountId #assign to temp var
        accountId += 1 #increment the id by 1
        creationDate = date.today() #get the creation date - whenever user is editing

        #checking user input
        if (len(accountName) == 0 or len(notes) == 0):#if any fields are missing
            #display an error
            self.labelError.setText("Missing required field. Please fill in all fields.")
        else : #otherwise
            #sql to check if the account name is unique to their user
            sqlDatabaseAccountName = "SELECT AccountDetail.Account_Name FROM Accounts, AccountDetail WHERE Accounts.UserID = " + str(gUserId) + " AND Accounts.AccountID = AccountDetail.AccountID AND AccountDetail.Account_Name = \'" + accountName + "\';"
            tupleAccountName = executeSQL(sqlDatabaseAccountName) #execute the sql
            databaseAccountName = "" #temp variable
            for row in tupleAccountName: #parse the curosr
                databaseAccountName = row.Account_Name 

            #if the length of the retrieved name is 0 then it does not exist - the account name that was entered was not found in the database
            if len(databaseAccountName) == 0: #account does not exist
                #sql for inserting new account
                sqlInsertNewAccount = "INSERT INTO AccountDetail VALUES(\'"+ accountName + "\', \'" + accountType + "\', " + str(accountId) + ", \'" + str(creationDate) + "\', 0, \'" + notes + "\'); INSERT INTO Accounts VALUES(" + str(accountId) + ", " + str(gUserId) + ");"
                insertSQL(sqlInsertNewAccount) #insert the account 
                #self.labelError.setText("Created new account. Please close window.")
                widget.currentWidget().comboBoxAccountSelector.addItem(accountName) #add the new account to the account selector drop down on the account screen page
                widget.currentWidget().accountsWidget.hide() #close the window after inserting
            else : #does exist
                #display error
                self.labelError.setText("Account with name: \"" + accountName + "\" already exists.")

#Class Name: AccountScreen
#Inherits:   QDialog (from Qt library)
#Purpose:    object for the account screen. Uses account.ui along with various
#            methods and functions to access other screens and functionality of the app
class AccountScreen(QDialog):
    # Handle high resolution displays:  source: https://stackoverflow.com/questions/43904594/pyqt-adjusting-for-different-screen-resolution
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    #creating instance of another application inorder to handle pop up screens
    accountsApp = QApplication(sys.argv)
    accountsWidget = QStackedWidget()
    accountsWidget.setWindowTitle("New Account")
    accountsWidget.setWindowIcon(QtGui.QIcon('moneyicon.png'))
    
    #Constructor
    def __init__(self):
        super(AccountScreen, self).__init__()
        #load newuserscreen user interface
        loadUi("./userinterfaces/account.ui", self)
        
        #sql for generating username in top corner of screen
        usernameSQL = "SELECT Username FROM Users WHERE ID = '" + str(gUserId) + "'"
        tupleUsername = executeSQL(usernameSQL) #execute the sql
        locUsername = "" #temp var
        for row in tupleUsername: #parse through the cursor
            locUsername = row.Username  #temp var set to new variable
        self.labelUsername.setText(locUsername) #displaying username to screen

        #getting todays date
        todaysDate = date.today()
        displayDate = todaysDate.strftime("%B %d, %Y")
        self.labelTimeDate.setText(displayDate) #displaying todays date to screen

        #SQL for retrieving the accounts of the user        
        sqlGetAccounts = "SELECT AccountDetail.Account_Name FROM AccountDetail, Accounts WHERE Accounts.UserID = " + str(gUserId) + " AND Accounts.AccountID = AccountDetail.AccountID;"
        tupleGetAccounts = executeSQL(sqlGetAccounts) #executing the sql
        for row in tupleGetAccounts: #parsing through the cursor
            self.comboBoxAccountSelector.addItem(row.Account_Name) #adding the account name to the account selector drop down
            
        #if the go button is pressed then execute goToAccountDetailsScreen
        self.buttonGo.clicked.connect(self.goToAccountDetailsScreen)
        
        #if the create new account button is clicked, then execute the popUpCreateNewAccount function
        self.buttonCreateNewAccount.clicked.connect(self.popUpCreateNewAccount)

        #if sign out button is clicked, go to sign in screen
        self.buttonSignOut.clicked.connect(self.goToWelcomeScreen)
    
    #Name:      popUpCreateNewAccount
    #Purpose:   adds a newaccount screen pop up screen instance to the stacked widget for accounts, goes to that new page
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def popUpCreateNewAccount(self):
        newaccount = NewAccountPopUp() #creating instance
        self.accountsWidget.addWidget(newaccount) #adding to accountsWidget application
        self.accountsWidget.setCurrentIndex(self.accountsWidget.currentIndex() + 1) #on that app, go to the right index
        self.accountsWidget.show() #show the app
        
    #Name:      goToWelcomeScreen
    #Purpose:   adds a welcome screen instance to the stacked widget, displays welcome screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def goToWelcomeScreen(self):
        welcome = WelcomeScreen() #creating instance of welcome screen
        widget.addWidget(welcome) #adding that instance to the widget
        widget.setCurrentIndex(widget.currentIndex()+1) #go to the welcome screen
        self.accountsWidget.hide() #closes any open pop up windows

    #Name:      goToAccountDetailsScreen
    #Purpose:   adds an goals screen instance to the stacked widget, displays the goals screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def goToAccountDetailsScreen(self):
        #retrieving data from the account selector combo box
        countComboBox = self.comboBoxAccountSelector.count()
        if  countComboBox == 0: #if there are no accounts in the combo box
            self.labelError.setText("First create an account.")
        else: #there are accounts
            #retrieve the name of the current account on the combo box            
            accountName = self.comboBoxAccountSelector.currentText()
            #sql for retrieving the account id of that account name
            sqlGetGAccountId = "SELECT AccountID FROM AccountDetail WHERE Account_Name = \'" + accountName + "\';"
            tupleAccountID = executeSQL(sqlGetGAccountId) #executing that sql
            for row in tupleAccountID: #parse through the cursor
                global gAccountId #global used for changing global variables
                gAccountId = row.AccountID #setting the global variable account id so future screens can be attached to this account id
            accountDetails = AccountDetailsScreen() #creating instance of accountDetails screen
            widget.addWidget(accountDetails) #adding that screen to the widget
            widget.setCurrentIndex(widget.currentIndex()+1) #going to that screen
            self.accountsWidget.hide() #closes any open pop up windows

#Class Name: NewTransactionPopUp
#Inherits:   QDialog (from Qt library)
#Purpose:    object for a new transaction. Uses newTransaction.ui along with various
#            methods and functions to access other screens and functionality of the app
class NewTransactionPopUp(QDialog):
    #Constructor
    def __init__(self):
        super(NewTransactionPopUp, self).__init__()
        #loading user interface
        loadUi("./userinterfaces/newTransaction.ui",self)
        #setting guards for date of new transaction
        today = date.today() #getting todays gate
        oldestDate = datetime(1950, 1, 1) #making oldest available date 1/1/1950
        self.dateEditTransactionDate.setDate(today) #default date that appears is today
        self.dateEditTransactionDate.setMinimumDate(oldestDate) #oldest date set to 1/1/1950
        self.dateEditTransactionDate.setMaximumDate(today) #maximum date is today - no future transactions
        self.dateEditTransactionDate.setCalendarPopup(True) #making it calendar instead of normal date selector
        #setting guards for amount of transaction
        self.doubleSpinBoxAmount.setMaximum(999999999.99)
        self.doubleSpinBoxAmount.setMinimum(0)
        self.doubleSpinBoxAmount.setValue(0)
        
        #if new transaction button is clicked then execute new transaction function
        self.buttonCreateNewTransaction.clicked.connect(self.newTransaction)
    
    #Name:      newTransaction
    #Purpose:   inserts a new transaction to the database if required fields are filled out appropriately
    #Args:      self
    #Returns:   adds a transaction to the database and closes the pop up window
    def newTransaction(self):
        #retrieving values from user input
        transAmount = self.doubleSpinBoxAmount.value()
        transType = self.comboBoxTransactionType.currentText()
        tDate = self.dateEditTransactionDate.date() 
        transDate = tDate.toString(QtCore.Qt.ISODate) #creating a date type for transaction date
        transCategory = self.lineEditCategory.text() 

        #checks if any of the fields are empty
        if len(str(transAmount)) == 0 or len(transType) == 0 or len(str(transDate)) == 0 or len(transCategory) == 0:
            #fields are missing
            #display error
            self.labelError.setText("Missing fields. Try again.")
        else: #otherwise:
            #check if withdrawal or deposit
            if transType == "Withdrawal": #transaction type is withdrawal.
                transAmount = transAmount * -1 #then change the transaction amount to negative
            #for retrieving the next transaction id
            sqlTransId = "SELECT MAX(TransID) as transId FROM Transactions"
            tupleTransId = executeSQL(sqlTransId) #execute sql
            transId = 0 #creating temp var
            for row in tupleTransId: #parsing through the cursor
                transId = row.transId
            transId += 1 #incrementing the id by 1
            #sql for inserting the new transaction into the transaction table
            sqlInsertNewTransaction = "INSERT INTO Transactions VALUES("+ str(transId) + ", " + str(gAccountId) + ", " + str(transAmount) + ", \'" + transCategory + "\', \'" + transDate + "\');"
            insertSQL(sqlInsertNewTransaction) #execute the insert sql
            #self.labelError.setText("Created new transaction. Closing window.")
            widget.currentWidget().transactionWidget.hide() #close the pop up window
            widget.currentWidget().tableWidgetTransactions.setRowCount(0) #clear the transaction table
            widget.currentWidget().generateTransactionTable() #generate the transaction table
            
#Class Name: DeleteTransactionPopUp
#Inherits:   QDialog (from Qt library)
#Purpose:    object for a deleting a transaction on a new screen. Uses deleteTransaction.ui along with various
#            methods and functions to access other screens and functionality of the app
class DeleteTransactionPopUp(QDialog):
    #constructor
    def __init__(self):
        super(DeleteTransactionPopUp, self).__init__()
        #loading user interface
        loadUi("./userinterfaces/deleteTransaction.ui",self)

        #setting constraints on the transaction id
        self.spinBoxTransactionId.setMaximum(999999999)
        self.spinBoxTransactionId.setMinimum(30000)
        self.spinBoxTransactionId.setValue(30000)
        
        #if delete transaction is clicked, delete the transaction
        self.buttonDeleteTransaction.clicked.connect(self.deleteTransaction)
    
    #Name:      deleteTransaction 
    #Purpose:   deletes a transaction based off user inputted transaction id number
    #Args:      self
    #Returns:   deletes a transaction from the database
    def deleteTransaction(self):
        #retrieving the transaction id from user input
        transId = self.spinBoxTransactionId.value()
        #sql for seeing if the transaction is "owned" by the user
        sqlRetrieveTransId = "SELECT TransID FROM Transactions WHERE TransID = " + str(transId) + " AND AccountID = " + str(gAccountId)
        tupleRetrievedTransId = executeSQL(sqlRetrieveTransId) #executing the sql
        retrievedTransId = 0 #temp var 
        for row in tupleRetrievedTransId: #parsing through the cursor
            retrievedTransId = row.TransID #setting temp var to the transaction id
        
        #check if the transaction is "owned" by the user
        if retrievedTransId == transId: #user owns the transaction
            #sql for actually delete the transaction
            sqlDeleteTrans = "DELETE FROM Transactions WHERE TransID = " + str(transId)
            insertSQL(sqlDeleteTrans) #execute the delete statement (using insertSQl achieves the same purpose)
            #self.labelError.setText("Deleted Transaction. Closing Window.")
            widget.currentWidget().transactionWidget.hide() #hide the pop up window
            widget.currentWidget().tableWidgetTransactions.setRowCount(0) #clear the transaction table
            widget.currentWidget().generateTransactionTable() #regenerate the transaction table
        else: #user does not "own" the transaction
            #display error
            self.labelError.setText("Transaction ID does not exist.")

#Class Name: AccountDetailsScren
#Inherits:   QDialog (from Qt library)
#Purpose:    object for a seeing account details. Uses accountdetails.ui along with various
#            methods and functions to access other screens and functionality of the app
#Notes:      There is also another "app" built from within this class to have functionality for
#            deleting and creating new transactions
class AccountDetailsScreen(QDialog):
    # Handle high resolution displays:  source: https://stackoverflow.com/questions/43904594/pyqt-adjusting-for-different-screen-resolution
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    #creating app for the pop up 
    transactionApp = QApplication(sys.argv)
    transactionWidget = QStackedWidget()
    #setting window title and window icon
    transactionWidget.setWindowTitle("New Transaction")
    transactionWidget.setWindowIcon(QtGui.QIcon('moneyicon.png'))
    
    # constructor
    def __init__(self):
        super(AccountDetailsScreen, self).__init__()
        #load newuserscreen user interface
        loadUi("./userinterfaces/accountdetails.ui", self)
        
        #for generating username
        usernameSQL = "SELECT Username FROM Users WHERE ID = '" + str(gUserId) + "'"
        tupleUsername = executeSQL(usernameSQL) #execute the sql
        locUsername = "" #temp var
        for row in tupleUsername: #iterate through cursor
            locUsername = row.Username #setting the username to temp var
        self.labelUsername.setText(locUsername) #displaying the username
        
        #getting todays date
        todaysDate = date.today()
        displayDate = todaysDate.strftime("%B %d, %Y")
        self.labelTimeDate.setText(displayDate)

        #SQL for retrieveing account name
        accountNameSQL = "SELECT Account_Name FROM AccountDetail WHERE AccountID = " + str(gAccountId)
        tupleAccountName = executeSQL(accountNameSQL) #executing the sql
        locAccountName = "" #temp var
        for row in tupleAccountName: #iterating through the cursor
            locAccountName = row.Account_Name #setting temp var to retrieved variable
        self.labelAccountName.setText(locAccountName) #setting display to the acccount name
     
        #Sql for displaying the date created
        sqlDateCreated = "SELECT CreationDate FROM AccountDetail WHERE AccountID = " + str(gAccountId)
        tupleDateCreated = executeSQL(sqlDateCreated) #executing the sql
        locDateCreated = "" #temp var
        for row in tupleDateCreated: #iterating through the cursor
            locDateCreated = row.CreationDate #setting temp var to retrieved var
        dateCreated = datetime.strptime(locDateCreated, '%Y-%m-%d') #getting date in correct type
        self.labelDate.setText(dateCreated.strftime("%B %d, %Y")) #display date in correct style

        #Setting up guards for the spinBoxYear
        currentYear = todaysDate.year #getting todays year
        self.spinBoxYear.setMinimum(1950) #setting minimum date to 1950
        self.spinBoxYear.setMaximum(currentYear) #setting max year to current year
        self.spinBoxYear.setValue(currentYear) #setting current display to current year

        #if back to accounts button is pressed, go to function goToAccountScreen
        self.buttonBackToAccounts.clicked.connect(self.goToAccountScreen)
        #if new transaction button is pressed, go to function popUpNewTransaction
        self.buttonNewTransaction.clicked.connect(self.popUpNewTransaction)
        #If delete button is pressed, go to function popUpDeleteTransaction
        self.buttonMoreDetails.clicked.connect(self.goToAccountMonthScreen)
        #if delete button is pressed, go to function popUpDeleteTransaction
        self.buttonDelete.clicked.connect(self.popUpDeleteTransaction)
        #if delete button is pressed, go to function popUpDeleteTransaction
        self.buttonGoals.clicked.connect(self.goToGoals)

        self.generateTransactionTable() #genearte the transaction table

    #Name:      goToGoals
    #Purpose:   adds an goals screen instance to the stacked widget, displays the goals screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def goToGoals(self):
        goals = AccountGoalsScreen() #instance created
        widget.addWidget(goals) #added to stack
        widget.setCurrentIndex(widget.currentIndex()+1) #go to that new instance
        self.transactionWidget.hide() #closing any open pop ups

    #Name:      goToAccountMonthScreen
    #Purpose:   adds an account month screen instance to the stacked widget, displays the account month screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def goToAccountMonthScreen(self):
        #setting global variable of the month/date/year for accessing more information on the account
        global gDateMonth
        gyear = self.spinBoxYear.value() #retreiving the year
        gmonthWord = self.comboBoxMonth.currentText() #retrieving the month
        gmonthNum = 0
        #switch for changing the word into a number
        if gmonthWord == "January": gmonthNum = 1
        elif gmonthWord == "February" : gmonthNum = 2
        elif gmonthWord == "March" : gmonthNum = 3
        elif gmonthWord == "April" : gmonthNum = 4
        elif gmonthWord == "May" : gmonthNum = 5
        elif gmonthWord == "June" : gmonthNum = 6
        elif gmonthWord == "July" : gmonthNum = 7
        elif gmonthWord == "August" : gmonthNum = 8
        elif gmonthWord == "September" : gmonthNum = 9
        elif gmonthWord == "October" : gmonthNum = 10
        elif gmonthWord == "November" : gmonthNum = 11
        else : gmonthNum = 12
        gdate = 15 #set to 15 - middle of the month
        #creating date with the generated year, month and date values
        gDateMonth = date(gyear, gmonthNum, gdate)
        #creating instance of account month screen
        monthScreen = AccountMonthScreen()
        widget.addWidget(monthScreen) #adding month sreen to widget
        widget.setCurrentIndex(widget.currentIndex()+1) #going to that instance
        self.transactionWidget.hide() #closing any open pop ups
    
    #Name:      generateTransactionTable
    #Purpose:   Used for updating the transaction table on the screen
    #Args:      self
    #Returns:   an updated transaction table with the transactions for a specific account
    def generateTransactionTable(self):
        #retrieving the transactions from the database
        sqlTransactions = "SELECT * FROM Transactions WHERE AccountID = " + str(gAccountId)
        tupleTransactions = executeSQL(sqlTransactions)
        for row in tupleTransactions: #iterating through each instance of the transactions
            transId = row.TransID #the transaction id 
            tDate = row.Date #the transaction date
            trDate = datetime.strptime(tDate, '%Y-%m-%d') #setting date to datetime.date format
            transDate = trDate.strftime('%m/%d/%y') #for displaying the date in a better way

            transAmount = row.Amount #transaction amount
            transCategory = row.Category #the category of the transaction
            transType = "" #temp variable for transaction type
            if transAmount < 0: #if amount is less than zero
                transType = "Withdrawal"
            else: #amount is greater than zero
                transType = "Deposit"
            transAmount = round(abs(transAmount), 2) #rounding the transaction amount - also absolute value

            #updating each row/column in the table with the correct information
            rowPosition = self.tableWidgetTransactions.rowCount()
            self.tableWidgetTransactions.insertRow(rowPosition)
            self.tableWidgetTransactions.setItem(rowPosition,0, QtWidgets.QTableWidgetItem(str(transId)))
            self.tableWidgetTransactions.setItem(rowPosition,1, QtWidgets.QTableWidgetItem(transDate))
            self.tableWidgetTransactions.setItem(rowPosition,2, QtWidgets.QTableWidgetItem(str(transAmount)))
            self.tableWidgetTransactions.setItem(rowPosition,3, QtWidgets.QTableWidgetItem(transType))
            self.tableWidgetTransactions.setItem(rowPosition,4, QtWidgets.QTableWidgetItem(transCategory))

            #SQL for display the current account total
            sqlCurrentTotal = "SELECT sum(amount) as total FROM Transactions WHERE AccountID = " + str(gAccountId)
            tupleCurrentTotal = executeSQL(sqlCurrentTotal) #executing the sql
            locCurrentTotal = 0 #temp var
            for row in tupleCurrentTotal: #iterating throught the cursor
                locCurrentTotal = row.total #settig temp var to retrieved variable
            if locCurrentTotal == None: #if there are no transactions for the account
                self.labelCurrentTotal.setText("$0.00")  #display zero
            else: #there are transactions
                self.labelCurrentTotal.setText("$" + str(round(locCurrentTotal, 2))) #display that number with two decimals
        
    #Name:      popUpDeleteTransaction
    #Purpose:   adds delete transaction pop up screen instance to the stacked widget for transactions, goes to that new page
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def popUpDeleteTransaction(self):
        self.transactionWidget.hide() #closing any open pop ups
        deleteTransaction = DeleteTransactionPopUp() #instance created
        self.transactionWidget.addWidget(deleteTransaction) #add the widget
        self.transactionWidget.setCurrentIndex(self.transactionWidget.currentIndex() + 1) #setting current index to new instance
        self.transactionWidget.show() #showing the new pop up screen

    #Name:      popUpNewTransaction
    #Purpose:   adds new transaction pop up screen instance to the stacked widget for transactions, goes to that new page
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def popUpNewTransaction(self):
        self.transactionWidget.hide() #closing any open pop ups
        newTransaction = NewTransactionPopUp() #instance created
        self.transactionWidget.addWidget(newTransaction) #add the widget
        self.transactionWidget.setCurrentIndex(self.transactionWidget.currentIndex() + 1) #setting current index to that widget
        self.transactionWidget.show() #showing the new pop up screen

    #Name:      goToAccountScreen
    #Purpose:   adds an account screen instance to the stacked widget, displays the account screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def goToAccountScreen(self):
        account = AccountScreen() #instance created
        widget.addWidget(account) #added to stack
        widget.setCurrentIndex(widget.currentIndex()+1) #go to that new instance
        self.transactionWidget.hide() #closing any open pop ups

#Class Name: AccountGoalsScreen
#Inherits:   QDialog (from Qt library)
#Purpose:    Under Construction. Would have user be able to set specific budgeting goals for an account
class AccountGoalsScreen(QDialog):
    def __init__(self):
        super(AccountGoalsScreen, self).__init__()
        #load newuserscreen user interface
        loadUi("./userinterfaces/accountgoals.ui", self)
        
        #for generating username
        usernameSQL = "SELECT Username FROM Users WHERE ID = '" + str(gUserId) + "'"
        tupleUsername = executeSQL(usernameSQL) #execute the sql
        locUsername = "" #temp var
        for row in tupleUsername: #iterate through cursor
            locUsername = row.Username #setting the username to temp var
        self.labelUsername.setText(locUsername) #displaying the username
        
        #getting todays date
        todaysDate = date.today()
        displayDate = todaysDate.strftime("%B %d, %Y")
        self.labelTimeDate.setText(displayDate)

        #if go back to account details page is selected, execute goToAccountsDetail()
        self.buttonBackToAccountDetails.clicked.connect(self.goToAccountDetails)
    
    #Name:      goToAccountDetails 
    #Purpose:   adds an account details screen instance to the stacked widget, displays the account detail screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def goToAccountDetails(self):
        #creating instance
        accountDetails = AccountDetailsScreen()
        widget.addWidget(accountDetails) #adding instance to the stack
        widget.setCurrentIndex(widget.currentIndex()+1) #setting the index to that new instance


#Class Name: AccountMonthScreen
#Inherits:   QDialog (from Qt library)
#Purpose:    object for a login screen. Uses accountMonth.ui along with various
#            methods and functions to access other screens and functionality of the app
class AccountMonthScreen(QDialog):
    #Constructor
    def __init__(self):
        super(AccountMonthScreen, self).__init__()
        #load newuserscreen user interface
        loadUi("./userinterfaces/accountMonth.ui", self)

        #if back to account details button is clicked, go to account details screen
        self.buttonBackToAccountDetails.clicked.connect(self.goToAccountDetails)

        #setting the month/year label to the month and year the user selected
        self.labelMonth.setText(gDateMonth.strftime('%B %Y'))

        #for generating username
        usernameSQL = "SELECT Username FROM Users WHERE ID = '" + str(gUserId) + "'"
        tupleUsername = executeSQL(usernameSQL) #exeuting the sql
        locUsername = "" #temp var
        for row in tupleUsername: #iterating through the cursor object
            locUsername = row.Username #setting temp var to retrieved var
        self.labelUsername.setText(locUsername) #display the username
        
        #getting todays date
        todaysDate = date.today()
        displayDate = todaysDate.strftime("%B %d, %Y")
        self.labelTimeDate.setText(displayDate) #displaying the date

        #Sql for generating the account name label
        sqlAccountName = "SELECT Account_Name FROM AccountDetail WHERE AccountID = " + str(gAccountId)
        tupleAccountName = executeSQL(sqlAccountName) # executing the sql
        locAccountName = "" #temporarty variable
        for row in tupleAccountName: #iterator through the cursor object
            locAccountName = row.Account_Name #setting the temporary variable to the retrieved variable
        self.labelAccountName.setText(locAccountName) #setting the label the retrieved account name

        #Sql for generating the current account total
        sqlCurrentTotal = "SELECT sum(amount) as total FROM Transactions WHERE AccountID = " + str(gAccountId)
        tupleCurrentTotal = executeSQL(sqlCurrentTotal) #executing the sql
        locCurrentTotal = 0 #temporary variable for the current total
        for row in tupleCurrentTotal: #iterating through the cursor
            locCurrentTotal = row.total #setting the temp var to the retrieved variable
        if locCurrentTotal == None: #if there are no transactions for the account
            self.labelCurrentDollarTotal.setText("$0.00")  #display zero
        else: #there are transactions
            self.labelCurrentDollarTotal.setText("$" + str(round(locCurrentTotal, 2))) #display that number with two decimals

        #Sql for generating total monthly deposit
        sqlMonthlyTotalDeposit = "SELECT sum(Amount) as monthlyDeposit FROM Transactions WHERE Amount > 0 AND AccountID = " + str(gAccountId) + " AND Date <= (SELECT EOMONTH(\'" + str(gDateMonth) + "\'))AND Date >= (SELECT DATEADD(Day, 1, EOMONTH(\'" + str(gDateMonth) + "\', -1) ) );"
        tupleMonthlyTotalDeposit = executeSQL(sqlMonthlyTotalDeposit)  #execute the sql
        locMonthDeposit = 0 #temporary variable for the total
        for row in tupleMonthlyTotalDeposit: #iterating through the cursor
            locMonthDeposit = row.monthlyDeposit #setting the temp var to the retrieved variable
        if locMonthDeposit == None: #if there are no deposits
            self.labelMonthlyDeposits.setText("$0.00") #dispaly $0.00
        else: #there are deposits
            self.labelMonthlyDeposits.setText("$" + str(round(locMonthDeposit, 2))) #display $ amount

        #Sql for generating total monthly withdrawals
        sqlMonthlyTotalSpent = "SELECT sum(Amount) as monthlySpent FROM Transactions WHERE Amount < 0 AND AccountID = " + str(gAccountId) + " AND Date <= (SELECT EOMONTH(\'" + str(gDateMonth) + "\')) AND Date >= (SELECT DATEADD(Day, 1, EOMONTH(\'" + str(gDateMonth) + "\', -1) ) );"
        tupleMonthlyTotalSpent = executeSQL(sqlMonthlyTotalSpent)
        locMonthSpent = 0 #temporary variable for the total
        for row in tupleMonthlyTotalSpent: #iterating through the cursor
            locMonthSpent = row.monthlySpent #setting the temp var to the retrieved variable
        if locMonthSpent == None: #if there are no withdrawals
            self.labelMonthlyWithdrawals.setText("$0.00") #display $0.00
        else: #there are withdrawals
            self.labelMonthlyWithdrawals.setText("$" + str(round(locMonthSpent, 2))) #display $ amount

        # Creating a pie chart
        series = QPieSeries()
        #Sql for retrieving the categories and there respective dollar amount for the month
        sqlCategorySpending = "SELECT Category, SUM(ABS(Amount)) AS total FROM Transactions WHERE Amount < 0 AND AccountID = " + str(gAccountId) + " AND Date <= (SELECT EOMONTH(\'" + str(gDateMonth) + "\')) AND Date >= (SELECT DATEADD(Day, 1, EOMONTH(\'" + str(gDateMonth) + "\', -1) ) ) GROUP BY Category ORDER BY total desc; "
        tupleCategorySpend = executeSQL(sqlCategorySpending) #execute the sql

        myCategoryList = [] #creating a list to have the categories - used for labels on the pie chart
        for row in tupleCategorySpend: #iterating through the pie chart
            myCategoryList.append(row.Category) #adding the category to the list
            series.append(row.Category, row.total)  #adding the category and respective total to the pie chart
        #the pie chart will automatically calculate the percentages of the categories
        
        if len(myCategoryList) > 0: 
            #slice for styling and creating labels/percentages
            iterator = 0 #iterator used for iterating through the catgory list
            for slice in series.slices(): #for every slice in the pie
                #set the label to the percentage - category
                slice.setLabel("{:.1f}%".format(100 * slice.percentage()) + " - " + myCategoryList[iterator])
                slice.setLabelVisible(True)
                iterator += 1

            #For exploding the largest pie slice:
            my_slice = series.slices()[0] #should be the biggest slice
            my_slice.setExploded(True) #exploding this to true
            my_slice.setLabelVisible(True) #setting the label as visible
            my_slice.setPen(QPen(Qt.blue, 4)) #Blue 
            my_slice.setBrush(Qt.blue) #blue pt 2

            #create QChart object for the pie chart to exist in
            chart = QChart()
            chart.addSeries(series) #adding the pie series to the chart
            chart.setAnimationOptions(QChart.SeriesAnimations) #fun animation for gits and shiggles
            chart.setTitle("Categorical Spending for the Month") #chart title
            chart.setTheme(QChart.ChartThemeBlueIcy) #theme of the chart

            # create QChartView object and add chart in their
            chartview = QChartView(chart)
            self.layoutPieChart.addWidget(chartview) #adding the chartview to the actual screen
            #creating highest category sql
            sqlHighestCategory = "SELECT TOP 1 Category FROM (SELECT Category, SUM(abs(Amount)) AS total FROM Transactions  WHERE AccountID = " + str(gAccountId) + " AND Date <= (SELECT EOMONTH(\'" + str(gDateMonth) + "\')) AND Date >= (SELECT DATEADD(Day, 1, EOMONTH(\'" + str(gDateMonth) + "\', -1) ) ) GROUP BY Category HAVING sum(amount) < 0) as t  ORDER BY total desc; "
            tupleHighCategory = executeSQL(sqlHighestCategory) #execute the sql
            highCat = "" #temp var
            for row in tupleHighCategory: #iterate through the cursor object
                highCat = row.Category #setting temp variable to the variable retrieved
            self.labelHighCategory.setText(highCat) #displaying the highest category
        else:
            self.labelHighCategory.setText("No withdrawals for this month.")

        
        
    #Name:      goToAccountDetails 
    #Purpose:   adds an account details screen instance to the stacked widget, displays the account detail screen
    #Args:      self
    #Returns:   adds a widget to the stack and goes to that new widget
    def goToAccountDetails(self):
        #creating instance
        accountDetails = AccountDetailsScreen()
        widget.addWidget(accountDetails) #adding instance to the stack
        widget.setCurrentIndex(widget.currentIndex()+1) #setting the index to that new instance


#######################
#####-----MAIN-----####
#######################

# Handle high resolution displays:  source: https://stackoverflow.com/questions/43904594/pyqt-adjusting-for-different-screen-resolution
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


#Global varibales that will store the user's sign in information, account id, and the month they choose
#these are all used for jumping across screens
gUserId = ""
gAccountId = ""
gDateMonth = ""

#Creating and application
app = QApplication(sys.argv)

#creating first instance of welcome screen
welcome = WelcomeScreen()
#creating a stacked widget to hold several pages
widget = QStackedWidget()

#adding the instance of welcome screen to the stacked widget
widget.addWidget(welcome)
widget.setWindowTitle("LOW Financial Management") #set title of the window
widget.setWindowIcon(QtGui.QIcon('./userinterfaces/moneyicon.png')) #set the icon of the window
widget.showMaximized()
widget.showMinimized()
widget.show() #show the actual widget

try:
    sys.exit(app.exec_())
except:
    print("Exiting")