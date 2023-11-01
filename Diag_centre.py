import tkinter as tk
import tkinter.scrolledtext as st
module_found = False

try:
    import pymysql as mc
    module_found = True
except ModuleNotFoundError:
    try:
        import mysql.connector as mc
        module_found = True
    except ModuleNotFoundError:
        defwin = tk.Tk()
        defwin.config(bg='firebrick')
        defwin.geometry('1200x700+200+50')
        defmsg = st.ScrolledText(defwin, font=('Consolas', 50, 'bold'), bg='wheat', fg='brown')
        defmsg.place(relheight=0.9, relwidth=0.9, relx=0.05, rely=0.05)
        defmsg.insert('end', 'Please install \n\npymysql module or \n\nmysql.connector module')
        defwin.mainloop()

# TCS Project - Diagnostic Centre Management System.
# Team name - REBORN
# Team Members - Mukesh Padmanabhan, Niranjan Balakumar, Aswin
# School - DAV School, Adambakkam
# Consolas and Jetbrains Mono
# executes the application , only if suitable modules are found
if module_found:
    dbwindow = tk.Tk()
    dbwindow.title('Database Set-up')
    dbwindow.geometry('1600x800+0+0')

    dbframe = tk.Frame(dbwindow, bg='orange', bd=20)
    dbframe.place(relx=0, rely=0, relheight=1, relwidth=0.45)
    dbframe1 = tk.Frame(dbwindow, bg='Firebrick', bd=20)
    dbframe1.place(relx=0.45, rely=0, relheight=1, relwidth=0.55)

    outputbox = st.ScrolledText(dbframe, bg='Navy', fg='Gold', font=('Consolas', 30, 'bold'), wrap='word')
    outputbox.place(relheight=1, relwidth=1)
    prompt = "Welcome User! Before beginning the application, kindly provide credentials of the MySQL database for" \
             " use in maintaining the Diagnostic Centre's Database . Clear existing inputs if you wish to enter a new" \
             " value.\n\n\n We hope you read the file 'README.txt'. If not, please read it before usage!"

    outputbox.insert('end', prompt)

    dbunamelabel = tk.Label(dbframe1, fg='dark slate gray', bg='light cyan', font=('Consolas', 20), text='MySQL Username:')
    dbpwdlabel = tk.Label(dbframe1, fg='dark slate gray', bg='light cyan', font=('Consolas', 20), text='MySQL Password:')
    dbhostlabel = tk.Label(dbframe1, fg='dark slate gray', bg='light cyan', font=('Consolas', 20), text='MySQL Host:')
    dbdblabel = tk.Label(dbframe1, fg='dark slate gray', bg='light cyan', font=('Consolas', 20), text='Database Name:')

    dbunameentry = tk.Entry(dbframe1, fg='dodger blue', bg='azure', font=('Consolas', 20))
    dbpwdentry = tk.Entry(dbframe1, fg='dodger blue', bg='azure', font=('Consolas', 20), show='*')
    dbhostentry = tk.Entry(dbframe1, fg='dodger blue', bg='azure', font=('Consolas', 20))
    dbdbentry = tk.Entry(dbframe1, fg='dodger blue', bg='azure', font=('Consolas', 20))

    dbunameentry.insert(0, 'root')
    dbhostentry.insert(0, 'localhost')
    dbdbentry.insert(0, 'diagnostic_centre')

    dbunamelabel.place(relwidth=0.4475, relx=0.035, relheight=0.15, rely=0)
    dbunameentry.place(relwidth=0.4475, relx=0.5175, relheight=0.15, rely=0)
    dbpwdlabel.place(relwidth=0.4475, relx=0.035, relheight=0.15, rely=0.2165)
    dbpwdentry.place(relwidth=0.4475, relx=0.5175, relheight=0.15, rely=0.2165)
    dbhostlabel.place(relwidth=0.4475, relx=0.035, relheight=0.15, rely=0.433)
    dbhostentry.place(relwidth=0.4475, relx=0.5175, relheight=0.15, rely=0.433)
    dbdblabel.place(relwidth=0.4475, relx=0.035, relheight=0.15, rely=0.6495)
    dbdbentry.place(relwidth=0.4475, relx=0.5175, relheight=0.15, rely=0.6495)

    dbbutton = tk.Button(dbframe1, bg='Gainsboro', fg='Black', text='Submit', font=('Jetbrains Mono', 30),
                         command=lambda: connect())
    dbbutton.place(relheight=0.1, relwidth=0.5, relx=0.25, rely=0.8625)

    patfile = open('Patient File.txt', 'r+')
    docfile = open('Doctor File.txt', 'r+')

    def connect():
        ''' Establishes connection to flat files before and after application usage to retrieve and store data '''
        db = mc.connect(host=str(dbhostentry.get()), user=str(dbunameentry.get()), passwd=str(dbpwdentry.get()))
        dbcur = db.cursor()
        dbcur.execute('CREATE DATABASE IF NOT EXISTS %s' % str(dbdbentry.get()))
        dbcur.execute('USE %s' % str(dbdbentry.get()))
        db.commit()
        dbwindow.destroy()
        application(db, dbcur)
        # The following part takes care of file handling: saving existing data to the opened file and closing it
        # Files have been opened at read and write mode; previous data should be overwritten with new data from table
        patfile.close()
        docfile.close()
        # Caution should be exercised while using w+ mode as it overwrites existing data during initiation
        patfile1 = open('Patient File.txt', 'w+')
        docfile1 = open('Doctor File.txt', 'w+')
        dbcur.execute('SELECT * FROM PATIENTS')
        for a in dbcur:
            patfile1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
                a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11]))
        dbcur.execute('SELECT * FROM DOCTORS')
        for a in dbcur:
            docfile1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
                a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11]))
        pass

    def application(mydb, mydbcur):
        ''' Main application code '''
        # These two strings are responsible for the creation of the two tables Doctors and Patients
        doc_table_creation_query = 'CREATE TABLE IF NOT EXISTS Doctors(Name varchar(30), Titles varchar(51), Gender varchar(5),' \
                                   ' Date_of_Birth date, Qualifications varchar(50), Salary decimal(10,2),' \
                                   ' Medical_License_No int(11) PRIMARY KEY, Center_Id int(11), Address varchar(50),' \
                                   ' Contact_No bigint, Email_ID varchar(20), Date_of_Joining date)'

        pat_table_creation_query = 'CREATE TABLE IF NOT EXISTS Patients(Reg_No int(11) PRIMARY KEY, Reg_Date date, Name varchar(30),' \
                                   'Gender varchar(5), Date_of_Birth date, Address varchar(50), Contact_No bigint, Hospital varchar(20),' \
                                   'Test_Date date, Test_Type varchar(50), Handling_Doctor varchar(30), Fees decimal(10,2))'

        mydbcur.execute(doc_table_creation_query)
        mydbcur.execute(pat_table_creation_query)

        patlist = []
        # The following part takes care of file handling-to open existing files and load data
        for b in patfile:
            patlist.append(b.split(sep='\t'))
        for a in patlist:
            query = 'INSERT INTO PATIENTS VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            values = (int(a[0]), str(a[1]), str(a[2]), str(a[3]), str(a[4]), str(a[5]), int(a[6]), str(a[7]), str(a[8]),
                      str(a[9]), str(a[10]), float(a[11]))
            try:
                mydbcur.execute(query, values)
            except mc.IntegrityError:
                pass
        del patlist

        doclist = []

        for c in docfile:
            doclist.append(c.split(sep='\t'))
        for d in doclist:
            query = 'INSERT INTO DOCTORS VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            values = (str(d[0]), str(d[1]), str(d[2]), str(d[3]), str(d[4]), float(d[5]), int(d[6]), int(d[7]), str(d[8]),
                      int(d[9]), str(d[10]), str(d[11]))
            try:
                mydbcur.execute(query, values)
            except mc.IntegrityError:
                pass
        del doclist

        mydb.commit()

        def login(x):
            '''Handles login through separate GUI window'''
            x = x.lower()
            try:
                def button_1():
                    '''View Doctors from database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('View Doctors')
                    win.config(bg='dark green')
                    win.geometry('950x700+300+50')

                    output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                    output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

                    mydbcur.execute('SELECT * FROM Doctors')
                    data = ''
                    j = 0
                    for a in mydbcur:
                        data += ' Name : %s\n Title : %s\n Gender : %s\n Date of Birth : %s\n Qualifications : %s\n' \
                                ' Salary : %s\n Medical License No. : %s\n Center ID : %s\n Address : %s\n Contact No. : %s\n' \
                                ' Email ID : %s\n Date of Joining : %s\n \n\n' % (
                                    a[0].lower().capitalize(), a[1].lower().capitalize(),
                                    a[2].upper(), a[3], a[4], float(a[5]), int(a[6]),
                                    int(a[7]), a[8], int(a[9]), a[10], a[11])
                        j += 1

                    output.insert('end', 'Number of Doctors : %s \n\n\n' % j + data)

                    win.mainloop()

                def button_2():
                    '''View Patients from database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('View Patients')
                    win.config(bg='gold')
                    win.geometry('950x700+300+50')

                    output = st.ScrolledText(win, fg='saddle brown', bg='wheat', font=('Consolas', 20))
                    output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

                    mydbcur.execute('SELECT * FROM Patients')
                    data = ''
                    i = 0
                    for a in mydbcur:
                        data += ' Registration Number : %s\n Registration Date : %s\n Name : %s\n Gender : %s\n Date of Birth : %s\n' \
                                ' Address : %s\n Contact No. : %s\n Hospital : %s\n Test Date : %s\n Test Type : %s\n' \
                                ' Handling Doctor : %s\n Fees : %s\n\n\n ' % (
                                    int(a[0]), a[1], a[2].lower().capitalize(), a[3].upper(),
                                    a[4], a[5], int(a[6]), a[7].lower().capitalize(), a[8],
                                    a[9], a[10].lower().capitalize(), float(a[11]))
                        i += 1

                    output.insert('end', 'Number of Patients : %s \n\n\n' % i + data)

                    win.mainloop()

                def button_3():
                    '''Delete Doctors from database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Delete Doctors')
                    win.config(bg='sea green')
                    win.geometry('950x700+300+50')

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit', font=('Jetbrains Mono', 20),
                                       command=lambda: docdel())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    entry1 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 30))

                    label1 = tk.Label(win, bg='#ADFF2F', fg='teal', font=('Jetbrains Mono', 30),
                                      text='Enter Medical License\n number of doctor\n to be deleted')

                    label1.place(relwidth=0.8, relheight=0.35, relx=0.1, rely=0.05)

                    entry1.place(relwidth=0.8, relheight=0.35, relx=0.1, rely=0.45)

                    def docdel():
                        mydbcur.execute('DELETE FROM DOCTORS WHERE  Medical_License_No=%s' % int(entry1.get()))
                        mydb.commit()
                        win.destroy()

                    win.mainloop()

                def button_4():
                    '''Delete Patients from database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Delete Patients')
                    win.config(bg='deep sky blue')
                    win.geometry('950x700+300+50')

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit', font=('Jetbrains Mono', 20),
                                       command=lambda: patdel())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    entry1 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 30))

                    label1 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 30),
                                      text='Enter Registration\n number of patient\n to be deleted')

                    label1.place(relwidth=0.8, relheight=0.35, relx=0.1, rely=0.05)

                    entry1.place(relwidth=0.8, relheight=0.35, relx=0.1, rely=0.45)

                    def patdel():
                        mydbcur.execute('DELETE FROM PATIENTS WHERE Reg_No=%s' % int(entry1.get()))
                        mydb.commit()
                        win.destroy()

                    win.mainloop()

                def button_5():
                    '''Search Doctors from database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Search Doctors')
                    win.config(bg='sea green')
                    win.geometry('950x700+300+50')

                    label1 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 25),
                                      text='Medical\nLicense No')
                    label2 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 25), text='Centre ID')

                    label1.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.2)
                    label2.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.6)

                    entry1 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 25))
                    entry2 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 25))

                    entry1.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.2)
                    entry2.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.6)

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit',
                                       font=('Jetbrains Mono', 20), command=lambda: docsearch())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    def docsearch():
                        if len(entry1.get()) != 0 and len(entry2.get()) != 0:
                            mln = int(entry1.get())
                            cid = int(entry2.get())
                            mydbcur.execute(
                                'SELECT * FROM DOCTORS WHERE Medical_License_No = %s AND Center_Id = %s' % (mln, cid))
                            data = ''
                            for a in mydbcur:
                                data += ' Name : %s\n Title : %s\n Gender : %s\n Date of Birth : %s\n' \
                                        ' Qualifications : %s\n Salary : %s\n Medical License No. : %s\n' \
                                        ' Center ID : %s\n Address : %s\n Contact No. : %s\n Email ID : %s\n' \
                                        ' Date of Joining : %s\n \n\n' % (
                                            a[0].lower().capitalize(), a[1].lower().capitalize(),
                                            a[2].upper(), a[3], a[4], float(a[5]), int(a[6]), int(a[7]),
                                            a[8], int(a[9]), a[10], a[11])
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        elif len(entry1.get()) != 0:
                            mln = int(entry1.get())
                            mydbcur.execute('SELECT * FROM DOCTORS WHERE Medical_License_No = %s' % mln)
                            data = ''
                            for a in mydbcur:
                                data += ' Name : %s\n Title : %s\n Gender : %s\n Date of Birth : %s\n' \
                                        ' Qualifications : %s\n Salary : %s\n Medical License No. : %s\n' \
                                        ' Center ID : %s\n Address : %s\n Contact No. : %s\n Email ID : %s\n' \
                                        ' Date of Joining : %s\n \n\n' % (
                                            a[0].lower().capitalize(), a[1].lower().capitalize(),
                                            a[2].upper(), a[3], a[4], float(a[5]), int(a[6]), int(a[7]),
                                            a[8], int(a[9]), a[10], a[11])
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        elif len(entry2.get()) != 0:
                            cid = int(entry2.get())
                            mydbcur.execute('SELECT * FROM DOCTORS WHERE Center_Id = %s' % cid)
                            data = ''
                            for a in mydbcur:
                                data += ' Name : %s\n Title : %s\n Gender : %s\n Date of Birth : %s\n' \
                                        ' Qualifications : %s\n Salary : %s\n Medical License No. : %s\n' \
                                        ' Center ID : %s\n Address : %s\n Contact No. : %s\n Email ID : %s\n' \
                                        ' Date of Joining : %s\n \n\n' % (
                                            a[0].lower().capitalize(), a[1].lower().capitalize(),
                                            a[2].upper(), a[3], a[4], float(a[5]), int(a[6]), int(a[7]),
                                            a[8], int(a[9]), a[10], a[11])
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        else:
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', 'Enter at least one valid data!')

                    win.mainloop()

                def button_6():
                    '''Add tests for patients to database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Add Tests For Patients')
                    win.config(bg='deep sky blue')
                    win.geometry('950x700+300+50')

                    label1 = tk.Label(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 25),
                                      text='Registration\nNumber')
                    label2 = tk.Label(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 25), text='Tests to be added')

                    label1.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.2)
                    label2.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.6)

                    entry1 = tk.Entry(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 25))
                    entry2 = tk.Entry(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 25))

                    entry1.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.2)
                    entry2.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.6)

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit',
                                       font=('Jetbrains Mono', 20), command=lambda: tests())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    def tests():
                        regno = int(entry1.get())
                        testr = str(entry2.get())
                        mydbcur.execute('SELECT Test_Type FROM Patients WHERE Reg_No = %s' % regno)
                        for a in mydbcur:
                            testr += ', ' + a[0]
                        mydbcur.execute("UPDATE Patients SET Test_Type = '%s' " % testr)
                        mydb.commit()
                        win.destroy()

                def button_7():
                    '''Search Doctors from database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Search Doctors')
                    win.config(bg='sea green')
                    win.geometry('950x700+300+50')

                    label1 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 25), text='Name : ')
                    label2 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 25), text='Contact NO.')

                    label1.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.2)
                    label2.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.6)

                    entry1 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 25))
                    entry2 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 25))

                    entry1.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.2)
                    entry2.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.6)

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit',
                                       font=('Jetbrains Mono', 20), command=lambda: docsearch())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    def docsearch():
                        if len(entry1.get()) != 0 and len(entry2.get()) != 0:
                            name = str(entry1.get())
                            cno = int(entry2.get())
                            mydbcur.execute('SELECT * FROM DOCTORS WHERE Name = %s AND Contact_NO = %s' % (name, cno))
                            data = ''
                            for a in mydbcur:
                                data += ' Name : %s\n Title : %s\n Gender : %s\n Date of Birth : %s\n' \
                                        ' Qualifications : %s\n Salary : %s\n Medical License No. : %s\n' \
                                        ' Center ID : %s\n Address : %s\n Contact No. : %s\n Email ID : %s\n' \
                                        ' Date of Joining : %s\n \n\n' % (
                                            a[0].lower().capitalize(), a[1].lower().capitalize(),
                                            a[2].upper(), a[3], a[4], float(a[5]), int(a[6]), int(a[7]),
                                            a[8], int(a[9]), a[10], a[11])
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        elif len(entry1.get()) != 0:
                            name = str(entry1.get())
                            mydbcur.execute('SELECT * FROM DOCTORS WHERE Name = %s' % name)
                            data = ''
                            for a in mydbcur:
                                data += ' Name : %s\n Title : %s\n Gender : %s\n Date of Birth : %s\n' \
                                        ' Qualifications : %s\n Salary : %s\n Medical License No. : %s\n' \
                                        ' Center ID : %s\n Address : %s\n Contact No. : %s\n Email ID : %s\n' \
                                        ' Date of Joining : %s\n \n\n' % (
                                            a[0].lower().capitalize(), a[1].lower().capitalize(),
                                            a[2].upper(), a[3], a[4], float(a[5]), int(a[6]), int(a[7]),
                                            a[8], int(a[9]), a[10], a[11])
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        elif len(entry2.get()) != 0:
                            cno = int(entry2.get())
                            mydbcur.execute('SELECT * FROM DOCTORS WHERE Contact_NO = %s' % cno)
                            data = ''
                            for a in mydbcur:
                                data += ' Name : %s\n Title : %s\n Gender : %s\n Date of Birth : %s\n' \
                                        ' Qualifications : %s\n Salary : %s\n Medical License No. : %s\n' \
                                        ' Center ID : %s\n Address : %s\n Contact No. : %s\n Email ID : %s\n' \
                                        ' Date of Joining : %s\n \n\n' % (
                                            a[0].lower().capitalize(), a[1].lower().capitalize(),
                                            a[2].upper(), a[3], a[4], float(a[5]), int(a[6]), int(a[7]),
                                            a[8], int(a[9]), a[10], a[11])
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        else:
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='teal', bg='green yellow', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', 'Enter at least one valid data!')

                    win.mainloop()

                def button_8():
                    '''Modify/Add patients details to database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Modify/Add Patients')
                    win.config(bg='deep sky blue')
                    win.geometry('950x700+300+50')

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit', font=('Jetbrains Mono', 20),
                                       command=lambda: patsub())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    entry1 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry2 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry3 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry4 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry5 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry6 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry7 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry8 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry9 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry10 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry11 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))
                    entry12 = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 15))

                    label1 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15),
                                      text='Registration\nNumber')
                    label2 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15),
                                      text='Reg Date\n(YYYY-MM-DD)')
                    label3 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='Patient\'s\nName')
                    label4 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='Gender\n(M/F/O)')
                    label5 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='DOB\n(YYYY-MM-DD)')
                    label6 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='Address')
                    label7 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='Contact NO.')
                    label8 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='Hospital')
                    label9 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15),
                                      text='Test Date\n(YYYY-MM-DD)')
                    label10 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='Test Type')
                    label11 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='Handling\nDoctor')
                    label12 = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 15), text='Fees')

                    entry1.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.0375)
                    entry2.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.0375)
                    entry3.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.175)
                    entry4.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.175)
                    entry5.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.3125)
                    entry6.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.3125)
                    entry7.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.45)
                    entry8.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.45)
                    entry9.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.5875)
                    entry10.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.5875)
                    entry11.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.725)
                    entry12.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.725)

                    label1.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.0375)
                    label2.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.0375)
                    label3.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.175)
                    label4.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.175)
                    label5.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.3125)
                    label6.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.3125)
                    label7.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.45)
                    label8.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.45)
                    label9.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.5875)
                    label10.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.5875)
                    label11.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.725)
                    label12.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.725)

                    def patsub():
                        regno = int(entry1.get())
                        regdate = str(entry2.get())
                        name = str(entry3.get().lower().capitalize())
                        gen = str((entry4.get()).upper())
                        dob = str(entry5.get())
                        add = str(entry6.get())
                        cno = int(entry7.get())
                        hosp = str(entry8.get().lower().capitalize())
                        tdate = str(entry9.get())
                        ttype = str(entry10.get())
                        doc = str(entry11.get().lower().capitalize())
                        fees = float(entry12.get())
                        query = """INSERT INTO patients VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY
                        UPDATE Reg_Date=%s, Name=%s, Gender=%s, Date_of_Birth=%s, address=%s, contact_no=%s, hospital=%s,
                        test_date=%s, test_type=%s, handling_doctor=%s, fees=%s """
                        val = (regno, regdate, name, gen, dob, add, cno, hosp, tdate, ttype, doc, fees,
                               regdate, name, gen, dob, add, cno, hosp, tdate, ttype, doc, fees)
                        mydbcur.execute(query, val)
                        mydb.commit()
                        win.destroy()

                    win.mainloop()

                def button_9():
                    '''Modify/Add doctors details to database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Modify/Add Doctors')
                    win.config(bg='sea green')
                    win.geometry('950x700+300+50')

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit', font=('Jetbrains Mono', 20),
                                       command=lambda: docsub())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    entry1 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry2 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry3 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry4 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry5 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry6 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry7 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry8 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry9 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry10 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry11 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))
                    entry12 = tk.Entry(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 15))

                    label1 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15),
                                      text='Doctor\'s\nName')
                    label2 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15),
                                      text='Title\n(Duty Type)')
                    label3 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15),
                                      text='Gender\n(M/F/O)')
                    label4 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15),
                                      text='DOB\n(YYYY-MM-DD)')
                    label5 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15),
                                      text='Qualifications')
                    label6 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15), text='Salary')
                    label7 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15),
                                      text='Medical\nLicense No.')
                    label8 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15), text='Centre ID')
                    label9 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15), text='Address')
                    label10 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15), text='Contact No.')
                    label11 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15), text='Email ID')
                    label12 = tk.Label(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 15),
                                       text='DOJ\n(YYYY-MM-DD)')

                    entry1.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.0375)
                    entry2.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.0375)
                    entry3.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.175)
                    entry4.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.175)
                    entry5.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.3125)
                    entry6.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.3125)
                    entry7.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.45)
                    entry8.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.45)
                    entry9.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.5875)
                    entry10.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.5875)
                    entry11.place(relwidth=0.2, relheight=0.1, relx=0.28, rely=0.725)
                    entry12.place(relwidth=0.2, relheight=0.1, relx=0.76, rely=0.725)

                    label1.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.0375)
                    label2.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.0375)
                    label3.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.175)
                    label4.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.175)
                    label5.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.3125)
                    label6.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.3125)
                    label7.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.45)
                    label8.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.45)
                    label9.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.5875)
                    label10.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.5875)
                    label11.place(relwidth=0.2, relheight=0.1, relx=0.04, rely=0.725)
                    label12.place(relwidth=0.2, relheight=0.1, relx=0.52, rely=0.725)

                    def docsub():
                        name = str((entry1.get()).lower().capitalize())
                        title = str(entry2.get())
                        gen = str((entry3.get()).upper())
                        dob = str(entry4.get())
                        qual = str(entry5.get())
                        salary = float(entry6.get())
                        mln = int(entry7.get())
                        cid = int(entry8.get())
                        add = str(entry9.get())
                        cno = int(entry10.get())
                        emid = str(entry11.get())
                        doj = str(entry12.get())
                        query = """INSERT INTO doctors VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE
                        Name=%s, Titles=%s, Gender=%s, Date_of_Birth=%s, Qualifications=%s, Salary=%s, Center_Id=%s, Address=%s,
                        Contact_NO=%s, Email_ID=%s, Date_of_Joining=%s """
                        val = (name, title, gen, dob, qual, salary, mln, cid, add, cno, emid, doj,
                               name, title, gen, dob, qual, salary, cid, add, cno, emid, doj)
                        mydbcur.execute(query, val)
                        mydb.commit()
                        win.destroy()

                    win.mainloop()

                def button_10():
                    '''Search Doctors from database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Search Patients')
                    win.config(bg='deep sky blue')
                    win.geometry('950x700+300+50')

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit', font=('Jetbrains Mono', 20),
                                       command=lambda: patsearch())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    entryx = tk.Entry(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 30))
                    entryx.place(relwidth=0.5, relheight=0.2, relx=0.25, rely=0.6)
                    labelx = tk.Label(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 30),
                                      text='Registration\nNumber')
                    labelx.place(relwidth=0.5, relheight=0.2, relx=0.25, rely=0.2)

                    def patsearch():
                        if len(entryx.get()) != 0:
                            regno = int(entryx.get())
                            mydbcur.execute('SELECT * FROM Patients where Reg_No=%s' % regno)
                            data = ''
                            for a in mydbcur:
                                data += ' Registration Number : %s\n Registration Date : %s\n Name : %s\n Gender : %s\n' \
                                        ' Date of Birth : %s\n Address : %s\n Contact No. : %s\n Hospital : %s\n Test Date : %s\n' \
                                        ' Test Type : %s\n Handling Doctor : %s\n Fees : %s\n\n\n ' % (int(a[0]), a[1],
                                                                                                       a[2].lower().capitalize(), a[3].upper(), a[4], a[5], int(a[6]), a[7].lower().capitalize(),
                                                                                                       a[8], a[9], a[10].lower().capitalize(), float(a[11]))
                            submit.destroy()
                            labelx.destroy()
                            entryx.destroy()

                            output = st.ScrolledText(win, fg='navy', bg='light sky blue', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)
                        else:
                            submit.destroy()
                            labelx.destroy()
                            entryx.destroy()
                            output = st.ScrolledText(win, fg='navy', bg='light sky blue', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', 'Enter a valid Registration Number')

                def button_11():
                    '''Add titles for doctors to database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Add Titles For Doctors')
                    win.config(bg='sea green')
                    win.geometry('950x700+300+50')

                    label1 = tk.Label(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 25),
                                      text='Medical\nLicense No')
                    label2 = tk.Label(win, bg='lawn green', fg='teal', font=('Jetbrains Mono', 25),
                                      text='Titles to be added')

                    label1.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.2)
                    label2.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.6)

                    entry1 = tk.Entry(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 25))
                    entry2 = tk.Entry(win, bg='green yellow', fg='teal', font=('Jetbrains Mono', 25))

                    entry1.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.2)
                    entry2.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.6)

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit',
                                       font=('Jetbrains Mono', 20), command=lambda: titles())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    def titles():
                        mln = int(entry1.get())
                        title = str(entry2.get())
                        mydbcur.execute('SELECT Titles FROM Doctors WHERE Medical_License_No = %s' % mln)
                        for a in mydbcur:
                            title += ', ' + a[0]
                        mydbcur.execute("UPDATE Patients SET Test_Type = '%s' " % title)
                        mydb.commit()
                        win.destroy()

                def button_12():
                    '''Search Patients from database through tkinter GUI'''
                    win = tk.Tk()
                    win.title('Search Patients')
                    win.config(bg='deep sky blue')
                    win.geometry('950x700+300+50')

                    label1 = tk.Label(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 25), text='Patient\'s\nName')
                    label2 = tk.Label(win, bg='light sky blue', fg='navy', font=('Jetbrains Mono', 25), text='Phone \nNumber')

                    label1.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.2)
                    label2.place(relwidth=0.35, relheight=0.2, relx=0.1, rely=0.6)

                    entry1 = tk.Entry(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 25))
                    entry2 = tk.Entry(win, bg='pale turquoise', fg='navy', font=('Jetbrains Mono', 25))

                    entry1.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.2)
                    entry2.place(relwidth=0.35, relheight=0.2, relx=0.55, rely=0.6)

                    submit = tk.Button(win, fg='black', bg='#DCDCDC', text='Submit',
                                       font=('Jetbrains Mono', 20), command=lambda: patsearch())
                    submit.place(relwidth=0.2, relx=0.4, relheight=0.1, rely=0.8625)

                    def patsearch():
                        if len(entry1.get()) != 0 and len(entry2.get()) != 0:
                            name = str(entry1.get())
                            cno = int(entry2.get())
                            mydbcur.execute("SELECT * FROM Patients WHERE Name = '%s' AND Contact_No = %s" % (name, cno))
                            data = ''
                            for a in mydbcur:
                                data += ' Registration Number : %s\n Registration Date : %s\n Name : %s\n Gender : %s\n' \
                                        ' Date of Birth : %s\n Address : %s\n Contact No. : %s\n Hospital : %s\n Test Date : %s\n' \
                                        ' Test Type : %s\n Handling Doctor : %s\n Fees : %s\n\n\n ' % (
                                            int(a[0]), a[1], a[2].lower().capitalize(),
                                            a[3].upper(), a[4], a[5], int(a[6]),
                                            a[7].lower().capitalize(), a[8], a[9],
                                            a[10].lower().capitalize(), float(a[11]))
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='navy', bg='light sky blue', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        elif len(entry1.get()) != 0:
                            name = str(entry1.get())
                            mydbcur.execute('SELECT * FROM Patients WHERE Name = "%s"' % name)
                            data = ''
                            for a in mydbcur:
                                data += ' Registration Number : %s\n Registration Date : %s\n Name : %s\n Gender : %s\n' \
                                        ' Date of Birth : %s\n Address : %s\n Contact No. : %s\n Hospital : %s\n Test Date : %s\n' \
                                        ' Test Type : %s\n Handling Doctor : %s\n Fees : %s\n\n\n ' % (
                                            int(a[0]), a[1], a[2].lower().capitalize(),
                                            a[3].upper(), a[4], a[5], int(a[6]),
                                            a[7].lower().capitalize(), a[8], a[9],
                                            a[10].lower().capitalize(), float(a[11]))
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='navy', bg='light sky blue', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        elif len(entry2.get()) != 0:
                            cno = int(entry2.get())
                            mydbcur.execute('SELECT * FROM Patients WHERE Contact_No = %s' % cno)
                            data = ''
                            for a in mydbcur:
                                data += ' Registration Number : %s\n Registration Date : %s\n Name : %s\n Gender : %s\n' \
                                        ' Date of Birth : %s\n Address : %s\n Contact No. : %s\n Hospital : %s\n Test Date : %s\n' \
                                        ' Test Type : %s\n Handling Doctor : %s\n Fees : %s\n\n\n ' % (
                                            int(a[0]), a[1], a[2].lower().capitalize(),
                                            a[3].upper(), a[4], a[5], int(a[6]),
                                            a[7].lower().capitalize(), a[8], a[9],
                                            a[10].lower().capitalize(), float(a[11]))
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='navy', bg='light sky blue', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', data)

                        else:
                            submit.destroy()
                            entry1.destroy()
                            entry2.destroy()
                            label1.destroy()
                            label2.destroy()

                            output = st.ScrolledText(win, fg='navy', bg='pale turquoise', font=('Consolas', 20))
                            output.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)
                            output.insert('end', 'Enter at least one valid data!')

                    win.mainloop()

                if x == 'admin' or x == '1':
                    window.destroy()

                    "Please read the comments before use!!!!!!!"
                    def admin_login(password, y):
                        ''' This program module is exclusively to deal with administrator login and admin database management, using MySQL 8.0

                        Administrator password is rockstaradmin

                        The user is requested to change the Administrator login password under the admin_login() function at line: 876'''
                        if password == 'rockstaradmin':
                            admin.destroy()
                            dbwin = tk.Tk()
                            dbwin.title('Admin Database Window')
                            dbwin.configure(background='dodger blue')
                            dbwin.geometry('1600x800+0+0')

                            label1 = tk.Label(dbwin, bg='orange red', fg='white', text='COMMAND-DOCTORS', font=('Consolas', 20, 'bold'))
                            label1.place(relwidth=0.4475, relx=0.035, relheight=0.1, rely=0.0375)
                            label2 = tk.Label(dbwin, bg='orange red', fg='white', text='COMMAND-PATIENTS', font=('Consolas', 20, 'bold'))
                            label2.place(relwidth=0.4475, relx=0.5175, relheight=0.1, rely=0.0375)

                            button1 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='View Doctors', font=('Consolas', 20, 'bold'), command=lambda: button_1())
                            button1.place(relwidth=0.4475, relx=0.035, relheight=0.1, rely=0.175)
                            button2 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='View Patients', font=('Consolas', 20, 'bold'), command=lambda: button_2())
                            button2.place(relwidth=0.4475, relx=0.5175, relheight=0.1, rely=0.175)
                            button3 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='Delete doctors data', font=('Consolas', 20, 'bold'), command=lambda: button_3())
                            button3.place(relwidth=0.4475, relx=0.035, relheight=0.1, rely=0.3125)
                            button4 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='Delete patients data', font=('Consolas', 20, 'bold'), command=lambda: button_4())
                            button4.place(relwidth=0.4475, relx=0.5175, relheight=0.1, rely=0.3125)
                            button5 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='Search on Medical License No./ Center Id', font=('Consolas', 20, 'bold'), command=lambda: button_5())
                            button5.place(relwidth=0.4475, relx=0.035, relheight=0.1, rely=0.45)
                            button6 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='Add more tests for the same patient.', font=('Consolas', 20, 'bold'), command=lambda: button_6())
                            button6.place(relwidth=0.4475, relx=0.5175, relheight=0.1, rely=0.45)
                            button7 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='Search on Name/Contact number', font=('Consolas', 20, 'bold'), command=lambda: button_7())
                            button7.place(relwidth=0.4475, relx=0.035, relheight=0.1, rely=0.5875)
                            button8 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='Modify/Add patient details.', font=('Consolas', 20, 'bold'), command=lambda: button_8())
                            button8.place(relwidth=0.4475, relx=0.5175, relheight=0.1, rely=0.5875)
                            button9 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='Modify/Add doctor details', font=('Consolas', 20, 'bold'), command=lambda: button_9())
                            button9.place(relwidth=0.4475, relx=0.035, relheight=0.1, rely=0.725)
                            button10 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='Search on Registration number.', font=('Consolas', 20, 'bold'), command=lambda: button_10())
                            button10.place(relwidth=0.4475, relx=0.5175, relheight=0.1, rely=0.725)
                            button11 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='Add a new title(Duty Type)', font=('Consolas', 20, 'bold'), command=lambda: button_11())
                            button11.place(relwidth=0.4475, relx=0.035, relheight=0.1, rely=0.8625)
                            button12 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='Search on patient name/phone number.', font=('Consolas', 20, 'bold'), command=lambda: button_12())
                            button12.place(relwidth=0.4475, relx=0.5175, relheight=0.1, rely=0.8625)

                            dbwin.mainloop()
                        else:
                            y['text'] = 'Wrong \npassword'

                    admin = tk.Tk()
                    admin.title('Administrator Credentials')
                    admin.geometry('500x500+500+200')
                    admin.configure(background='orange')

                    frm = tk.Frame(admin, bg='firebrick')
                    frm.place(relheight=0.15, relwidth=0.9, relx=0.05, rely=0.05)
                    lower_frame = tk.Frame(admin, bg='firebrick')
                    lower_frame.place(relheight=0.65, relwidth=0.9, relx=0.05, rely=0.3)

                    field = tk.Entry(frm, show='#', font=('Castellar', 20, 'bold'))
                    field.place(relwidth=0.6, relheight=0.9, relx=0.01, rely=0.05)

                    note = tk.Label(lower_frame, text='Enter Admin\n password\n in the\n text field', font=('Consolas', 40), fg='wheat', bg='navy')
                    note.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

                    click_me = tk.Button(frm, bg='Gainsboro', fg='Black', font=('Jetbrains Mono', 20), command=lambda: admin_login(field.get(), note), text='Submit')
                    click_me.place(relwidth=0.29, relheight=0.9, relx=0.7, rely=0.05)

                    admin.mainloop()

                elif x == 'doctor' or x == '2':
                    window.destroy()
                    "Please read the comments before use!!!!!!!"

                    def doc_login(password, y):
                        '''This program file is exclusively to deal with doctor login and patient's data management, using MySQL 8.0

                            Doctor password is rockstardoctor

                            The user is requested to change the Doctor login password under the doc_login() function at line: 948'''
                        if password == 'rockstardoctor':
                            doc.destroy()
                            dbwin = tk.Tk()
                            dbwin.title('Doctor Database Window')
                            dbwin.configure(background='dodger blue')
                            dbwin.geometry('1600x800+0+0')

                            label = tk.Label(dbwin, bg='orange red', fg='white', text='COMMAND-PATIENTS', font=('Consolas', 20, 'bold'))
                            label.place(relwidth=0.5, relx=0.25, relheight=0.1, rely=0.0375)
                            button1 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='View Patients', font=('Consolas', 20, 'bold'), command=lambda: button_2())
                            button1.place(relwidth=0.5, relx=0.25, relheight=0.1, rely=0.175)
                            button2 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='Delete Patients data', font=('Consolas', 20, 'bold'), command=lambda: button_4())
                            button2.place(relwidth=0.5, relx=0.25, relheight=0.1, rely=0.3125)
                            button3 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='Add more tests for the same patient.', font=('Consolas', 20, 'bold'), command=lambda: button_6())
                            button3.place(relwidth=0.5, relx=0.25, relheight=0.1, rely=0.45)
                            button4 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='Modify/Add patient details.', font=('Consolas', 20, 'bold'), command=lambda: button_8())
                            button4.place(relwidth=0.5, relx=0.25, relheight=0.1, rely=0.5875)
                            button5 = tk.Button(dbwin, bg='#87CEFA', fg='#0041C2', text='Search on Registration number.', font=('Consolas', 20, 'bold'), command=lambda: button_10())
                            button5.place(relwidth=0.5, relx=0.25, relheight=0.1, rely=0.725)
                            button6 = tk.Button(dbwin, bg='#E0FFFF', fg='#2F4F4F', text='Search on patient name/phone number.', font=('Consolas', 20, 'bold'), command=lambda: button_12())
                            button6.place(relwidth=0.5, relx=0.25, relheight=0.1, rely=0.8625)

                            dbwin.mainloop()
                        else:
                            y['text'] = 'Wrong \npassword'

                    doc = tk.Tk()
                    doc.title('Doctor Credentials')
                    doc.geometry('500x500+500+200')
                    doc.configure(background='orange')

                    frm = tk.Frame(doc, bg='firebrick')
                    frm.place(relheight=0.15, relwidth=0.9, relx=0.05, rely=0.05)
                    lower_frame = tk.Frame(doc, bg='firebrick')
                    lower_frame.place(relheight=0.65, relwidth=0.9, relx=0.05, rely=0.3)

                    field = tk.Entry(frm, show='#', font=('Castellar', 20, 'bold'))
                    field.place(relwidth=0.6, relheight=0.9, relx=0.01, rely=0.05)

                    note = tk.Label(lower_frame, text='Enter Doctor\n password\n in the\n text field', font=('Consolas', 40), fg='wheat', bg='navy')
                    note.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

                    click_me = tk.Button(frm, bg='Gainsboro', fg='Black', font=('Jetbrains Mono', 20), command=lambda: doc_login(field.get(), note), text='Submit')
                    click_me.place(relwidth=0.29, relheight=0.9, relx=0.7, rely=0.05)

                    doc.mainloop()

                else:
                    label['text'] = ' 1 : Admin \n 2 : Doctor \n \n Double click to submit.'
                    entry.insert(0, 'Invalid User Level')

            except ValueError:
                if x not in ['admin', 'doctor', 1, 2]:
                    label['text'] = 'Error'
                    entry.insert(0, 'Invalid User Level')

        window = tk.Tk()
        window.title('Diagnostic Centre')
        window.configure(background='Firebrick')
        window.geometry('600x600+450+150')

        frame = tk.Frame(window, bd='5', bg='steel blue')
        frame.place(relx=0.1, relwidth=0.8, rely=0.1, relheight=0.1)

        entry = tk.Entry(frame, bg='antique white', fg='saddle brown', font=('Jetbrains Mono', 15), text='Enter User Level')
        entry.insert(0, 'Enter user level')
        entry.place(relheight=1, relwidth=0.6, relx=0)

        button = tk.Button(frame, bg='Gainsboro', text='Submit', font=('Jetbrains Mono', 15), fg='#B8860B', command=lambda: login(entry.get()))
        button.place(relheight=1, relwidth=0.3, relx=0.7)

        lwrframe = tk.Frame(window, bd='10', bg='steel blue')
        lwrframe.place(relx=0.1, relwidth=0.8, rely=0.3, relheight=0.6)

        label = tk.Label(lwrframe, bd='10', font=('Consolas', 20), justify='left', bg='blanched almond', fg='#B8860B')
        label['text'] = ' 1 : Admin \n 2 : Doctor \n \n Clear existing\n data before entry.'
        label.place(relwidth=1, relheight=1)

        window.mainloop()
    dbwindow.mainloop()
