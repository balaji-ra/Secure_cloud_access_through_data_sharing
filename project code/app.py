from flask import Flask, render_template, request, session, redirect, url_for, flash,send_file
import pandas as pd
from flask_mail import *
import secrets
import os
import random
from random import getrandbits
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
from werkzeug.utils import secure_filename
import mysql.connector
import os

mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="VerifiableandFair",charset='utf8',port=3306)
mycursor = mydb.cursor()

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/cloudserver")
def cloudserver():
    return render_template('cloudserver.html')

@app.route("/ac")
def ac():
    return render_template('ac.html')

@app.route("/achome")
def achome():
    return render_template('achome.html')

@app.route("/cshome")
def cshome():
    return render_template('cshome.html')

@app.route("/dohome")
def dohome():
    return render_template('dohome.html')

@app.route("/cslog", methods=["POST", "GET"])
def cslog():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        if username == 'cloud@gmail.com' and password == 'cloud':
            return render_template('cshome.html', msg="Login successfull")
        else:
            return render_template('cloudserver.html', msg="Login Failed!!")
    return render_template('cloudserver.html')

@app.route("/aclog", methods=["POST", "GET"])
def aclog():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        if username == 'ac@gmail.com' and password == 'ac':
            return render_template('achome.html', msg="Login successfull")
        else:
            return render_template('ac.html', msg="Login Failed!!")
    return render_template('ac.html')

@app.route("/dataownerlog", methods=["POST", "GET"])
def dataownerlog():
    if request.method == "POST":
        doemail = request.form['doemail']
        password = request.form['password']
        sql = "select * from dataowner where doemail='%s' and password='%s' and status='accepted'" % (doemail, password)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if len(results) > 0:
            session['doemail'] = doemail
            print(session['doemail'])
            return render_template('dataownerhome.html', message="Login successfull")
        else:
            return render_template('dataownerlog.html', message="Login failed")
    return render_template('dataownerlog.html')

@app.route("/dataowner", methods=["POST", "GET"])
def dataowner():
    if request.method == "POST":
        doname = request.form['doname']
        doemail = request.form['doemail']
        password = request.form['password']
        password1 = request.form['Con_Password']
        contact = request.form['mobile']
        address = request.form['address']
        myfile = request.files['myfile']
        sql="select * from dataowner"
        result=pd.read_sql_query(sql,mydb)
        doemail1=result['doemail'].values
        print(doemail1)
        filename = myfile.filename
        if doemail in doemail1:
            return render_template('dataowner.html', message="email existed")
        if password == password1:
            sql="select * from dataowner where doemail='%s' and password='%s'"%(doemail,password)
            mycursor.execute(sql)
            data=mycursor.fetchall()
            print(data)
            if data==[]:
                path=os.path.join("static/profiles/", filename)
                myfile.save(path)
                profilepath = "static/profiles/"+filename
            print(doname, doemail, password, address)
            sql = "insert into dataowner(doname,doemail,password,contact,address,profile)values(%s,%s,%s,%s,%s,%s)"
            val = (doname, doemail, password, contact, address,profilepath)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('dataownerlog.html',message="registered successfully")
        else:
                return render_template('dataowner.html',message="registered ")
        flash('password not matched')
        return render_template('dataowner.html')
    return render_template('dataowner.html',message="somthing wrong")

@app.route('/viewowner')
def viewowner():
    sql="select * from dataowner where status='pending'"
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('viewowner.html',data1=data1)

@app.route("/accept/<id>")
def accept(id=0):
    print(id)
    sql = "select * from dataowner where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    email = dc[0][2]
    password = dc[0][3]
    print(email, password)
    status='Accepted'
    otp="Your request is accepted :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is accepted by Admin and email is:'+ email + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A Verifiable and Fair Attribute-Based Proxy Re-Encryption Scheme for Data Sharing in Clouds'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql = "update dataowner set status='accepted' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('Login approvel is accepted by the admin', 'success')
    return redirect(url_for('viewowner'))

@app.route("/reject/<id>")
def reject(id=0):
    print(id)
    sql = "select * from dataowner where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    email = dc[0][2]
    password = dc[0][3]
    print(email, password)
    
    otp="Your request is Rejected:"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is Rejected by Admin and email is:'+ email + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A Verifiable and Fair Attribute-Based Proxy Re-Encryption Scheme for Data Sharing in Clouds'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql = "update dataowner set status='rejected' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('viewlender'))

@app.route('/vieactivewowner')
def vieactivewowner():
    sql="select * from dataowner where status='accepted'"
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('vieactivewowner.html',data1=data1)

@app.route("/UploadFiles",methods=['POST','GET'])
def UploadFiles():
    if request.method=='POST':
        FileName=request.form["FileName"]
        Keywords=request.form["Keywords"]
        Police = request.form['Police']
        Files=request.files["Files"]
        n = secure_filename(Files.filename)
        path = os.path.join("uploads/", n)
        Files.save(path)
        dd = r"uploads/" + n
        f = open(dd, "r")
        data = f.read()
        print(data)
        sql = "select * from filesupload where FileName='%s'"%(FileName)
        result = pd.read_sql_query(sql, mydb)
        fname1 = result['FileName'].values
        if FileName in fname1:
            flash("File with this name already exists","danger")
            return render_template('DataOwnersUploadFiles.html')
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()
        print(current_date)
        print(t)
        
        sql="insert into filesupload (doemail,FileName,Keywords,Files,AccessPilicy,Date,Time) values (%s,%s,%s,AES_ENCRYPT(%s,'rupesh'),%s,%s,%s)"
        values=(session['doemail'],FileName,Keywords,data,Police,current_date,t)
        mycursor.execute(sql,values)
        mydb.commit()
        return render_template("UploadFiles.html",msg="success",files=Files)
    return render_template("UploadFiles.html")


@app.route('/viewmyfile')
def viewmyfile():
    sql="select * from filesupload where doemail='%s' "%(session['doemail'])
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('viewmyfile.html',data1=data1)

@app.route("/recipientslog", methods=["POST", "GET"])
def recipientslog():
    if request.method == "POST":
        reemail = request.form['reemail']
        password = request.form['password']
        sql = "select * from recipients where reemail='%s' and password='%s' and status='accepted'" % (reemail, password)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if len(results) > 0:
            session['reemail'] = reemail
            print(session['reemail'])
            return render_template('recipientshome.html', message="Login successfull")
        else:
            return render_template('recipientslog.html', message="Login failed")
    return render_template('recipientslog.html')

@app.route("/recipients", methods=["POST", "GET"])
def recipients():
    if request.method == "POST":
        rename = request.form['rename']
        print(request.form)
        reemail = request.form['reemail']
        password = request.form['password']
        password1 = request.form['Con_Password']
        contact = request.form['mobile']
        address = request.form['address']
        myfile = request.files['myfile']
        sql="select * from recipients"
        result=pd.read_sql_query(sql,mydb)
        reemail1=result['reemail'].values
        print(reemail1)
        filename = myfile.filename
        if reemail in reemail1:
            return render_template('recipients.html', message="email existed")
        if password == password1:
            sql="select * from recipients where reemail='%s' and password='%s'"%(reemail,password)
            mycursor.execute(sql)
            data=mycursor.fetchall()
            print(data)
            if data==[]:
                path=os.path.join("static/profiles/", filename)
                myfile.save(path)
                profilepath = "static/profiles/"+filename
            print(rename, reemail, password, address)
            sql = "INSERT INTO recipients (`rename`, `reemail`, `password`, `contact`, `address`, `profile`) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (rename, reemail, password, contact, address, profilepath)
            mycursor.execute(sql, val)
            mydb.commit()

            
            return render_template('recipientslog.html',message="registered successfully")
        else:
                return render_template('recipients.html',message="registered ")
        flash('password not matched')
        return render_template('dataowner.html')
    return render_template('recipients.html',message="somthing wrong")

@app.route('/viewrecipients')
def viewrecipients():
    sql="select * from recipients where status='pending'"
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('viewrecipients.html',data1=data1)

@app.route("/reciaccept/<ID>")
def reciaccept(ID=0):
    print(ID)
    sql = "select * from recipients where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    reemail = dc[0][2]
    password = dc[0][3]
    print(reemail, password)
    status='Accepted'
    otp="Your request is accepted :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is accepted by Admin and email is:'+ reemail + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = reemail
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A Verifiable and Fair Attribute-Based Proxy Re-Encryption Scheme for Data Sharing in Clouds'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql = "update recipients set status='accepted' where ID='%s'" % (ID)
    mycursor.execute(sql)
    mydb.commit()
    flash('Login approvel is accepted by the admin', 'success')
    return redirect(url_for('viewowner'))

@app.route("/recireject/<ID>")
def recireject(ID=0):
    print(ID)
    sql = "select * from recipients where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    reemail = dc[0][2]
    password = dc[0][3]
    print(reemail, password)
    
    otp="Your request is Rejected:"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is Rejected by Admin and email is:'+ reemail + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = reemail
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A Verifiable and Fair Attribute-Based Proxy Re-Encryption Scheme for Data Sharing in Clouds'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql = "update recipients set status='rejected' where ID='%s'" % (ID)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('viewlender'))

@app.route('/vieactiverecipients')
def vieactiverecipients():
    sql="select * from recipients where status='accepted'"
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('vieactiverecipients.html',data1=data1)

@app.route('/viewcloudfile')
def viewcloudfile():
    sql="select * from filesupload"
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('viewcloudfile.html',data1=data1)

@app.route('/sharefile', methods=["POSt", "GET"])
def sharefile():
    sql="select * from filesupload"
    x=pd.read_sql_query(sql,mydb)
    print(x)
    print("**********")
    FileName = x.values[0][2]
    keywords = x.values[0][3]
    Files = x.values[0][4]
    AccessPilicy =x.values[0][5]
    Date =x.values[0][6]
    Time = x.values[0][7]
    print(FileName,keywords,Files,AccessPilicy,Date,Time)
    print("pppppp")
    mydb.commit()

    sql="select * from recipients"
    y=pd.read_sql_query(sql,mydb)
    id = y.values[0][0]
    print(id)
    print(y)
    print(">>>>>>>>>>>>>>>>")
    mydb.commit()
    otp = random.randint(000000, 999999)
    print(otp)

    if request.method == "POST":
        doemail = session['doemail']
        FileName = request.form['FileName']
        reemail = request.form['reemail']
        sql = "insert into sharefile(doemail,RecipintId,FileName,AccessPilicy,reemail,Files,otp,Date,Time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (session['doemail'],id,FileName,AccessPilicy, reemail,Files,otp,Date,Time)
        s=mycursor.execute(sql, val)
        print(s)
        mydb.commit()

    sql = "select FileName from filesupload"
    mycursor.execute(sql)
    fdata = mycursor.fetchall()

    fdata = [j for i in fdata for j in i]
    print(fdata)

    sql = "select reemail from recipients"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    data = [j for i in data for j in i]
    print(data)

    return render_template('sharefile.html',fdata=fdata,data=data)

@app.route('/accessrequest')
def accessrequest():
    sql="select * from sharefile where Status='pending'"
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data1)
    print("***********")
    return render_template('accessrequest.html',data1=data1)

@app.route("/acceptfile/<id>")
def acceptfile(id=0):
    print(id)
    sql = "select * from sharefile where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    
    print("**********")
    reemail = dc[0][4]
    otp = dc[0][6]
    print(reemail, otp)
    status='Accepted'
    otp="Your request is accepted :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is accepted by Admin and email is:'+ reemail + ' and The Your secrate key is: '+ otp +'' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    # receiver_address = reemail
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = 'A Verifiable and Fair Attribute-Based Proxy Re-Encryption Scheme for Data Sharing in Clouds'
    # message.attach(MIMEText(mail_content, 'plain'))
    # session = smtplib.SMTP('smtp.gmail.com', 587)
    # session.starttls()
    # session.login(sender_address, sender_pass)
    # text = message.as_string()
    # session.sendmail(sender_address, receiver_address, text)
    # session.quit()
    sql = "update sharefile set Status='accepted' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('Login approvel is accepted by the admin', 'success')
    return redirect(url_for('accessrequest'))

@app.route("/rejectfile/<id>")
def rejectfile(id=0):
    print(id)
    sql = "update sharefile set Status='rejected' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('accessrequest'))

@app.route('/ViewshredFile')
def ViewshredFile():
    sql="select * from sharefile where reemail='%s' "%(session['reemail'])
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('ViewshredFile.html',data1=data1)

@app.route('/ViewFile',methods=['POST','GET'])
def ViewFile(id=0):
    print(id)
    sql = "select FileName from sharefile"
    mycursor.execute(sql)
    fdata = mycursor.fetchall()
    fdata = [j for i in fdata for j in i]
    print(fdata)
    return render_template('ViewFile.html',fdata=fdata)

@app.route('/Filedec', methods=['POST', 'GET'])
def Filedec():
    if request.method == 'POST':
        file_key = request.form["otp"]
        print(file_key)
        try:
            sql = f"SELECT AES_DECRYPT(Files, '{file_key}') FROM filesupload WHERE id = {id}"
            data = pd.read_sql_query(sql, mydb)
            decrypted_content = data.values[0][0].decode('utf8')
            return render_template("ViewdecFile.html", row_val=[[decrypted_content]])
        except Exception as e:
            print(e)
            return render_template("ViewdecFile.html", msg="notfound")

    return render_template("ViewdecFile.html", id=id)

@app.route('/sharefilereci', methods=["POST", "GET"])
def sharefilereci():
    sql="select * from sharefile"
    x=pd.read_sql_query(sql,mydb)
    print(x)
    doemail = x.values[0][1]
    RecipintId = x.values[0][2]
    FileName = x.values[0][3]
    reemail =x.values[0][4]
    Files =x.values[0][5]
    otp =x.values[0][6]
    Date =x.values[0][7]
    Time = x.values[0][8]
    print(doemail,RecipintId,FileName,reemail,Files,otp,Date,Time)
    mydb.commit()

    sql="select * from recipients"
    y=pd.read_sql_query(sql,mydb)
    id = y.values[0][0]
    reemail = y.values[0][2]
    print(id,reemail)
    print(y)
    mydb.commit()
    otp = random.randint(000000, 999999)
    print(otp)

    if request.method == "POST":
        reemail = session['reemail']
        FileName = request.form['FileName']
        sharedrecipient = request.form['reemail']  # Assuming you have a form field named 'reemail'
        sql = "INSERT INTO recipientsharefile (doemail, FileName, reemail,sharedrecipient, Files, otp, Date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (session['doemail'], FileName,session['reemail'], sharedrecipient, Files, otp,Date)
        print(val)
        mycursor.execute(sql, val)
        mydb.commit()



    sql = "select FileName from sharefile"
    mycursor.execute(sql)
    fdata = mycursor.fetchall()

    fdata = [j for i in fdata for j in i]
    print(fdata)

    sql = "select reemail from recipients"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    data = [j for i in data for j in i]
    print(data)
    return render_template('sharefilereci.html',fdata=fdata,data=data)

@app.route('/Viewsharedrecipient')
def Viewsharedrecipient():
    sql="select * from sharefile where reemail='%s'"%(session['reemail'])
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('Viewsharedrecipient.html',data1=data1)

@app.route('/ViewreFile/<id>')
def ViewreFile(id=0):
    print(id)
    sql = "select FileName from sharefile"
    mycursor.execute(sql)
    fdata = mycursor.fetchall()
    fdata = [j for i in fdata for j in i]
    return render_template('ViewreFile.html',fdata=fdata,id=id)

@app.route('/Filedecripted', methods=['POST', 'GET'])
def Filedecripted():
    if request.method == 'POST':
        id = request.form['id']
        file_key = request.form["otp"]
        FileName = request.form["FileName"]
        
        try:
            sql = f"SELECT AES_DECRYPT(Files, '{file_key}') FROM filesupload WHERE FileName = {FileName}"
            data = pd.read_sql_query(sql, mydb)
            decrypted_content = data.values[0][0].decode('utf8')
            return render_template("ViewdecriptedFile.html", row_val=[[decrypted_content]])
        except Exception as e:
            print(e)
            return render_template("ViewdecriptedFile.html", msg="notfound")
    return render_template("ViewdecriptedFile.html", id=id)

@app.route('/Viewownerfiles')
def Viewownerfiles():
    sql="select * from recipientsharefile "
    data1=pd.read_sql_query(sql,mydb)
    mydb.commit()
    return render_template('Viewownerfiles.html',data1=data1)

@app.route('/attacker',methods=['POST','GET'])
def attacker():
    if request.method=='POST':
        name=request.form['email']
        password=request.form['passcode']
        if name=="attacker" and password=="attacker":
            msg="Attacker Login Success"
            return render_template('attackerhome.html',msg=msg)
        else:
            msg="Invalid Credentials"
            return render_template('attacker.html',msg=msg)
    return render_template('attacker.html')

#searching files
@app.route("/attackersearchfile",methods=['POST','GET'])
def attackersearchfile():
    if request.method=='POST':
        Name=request.form['Keywords']
        try:
            sql = "select * from filesupload where Keywords='%s' " % (Name)
            print(sql)
            mycursor.execute(sql)
            X = mycursor.fetchall()
            print(X)
            mydb.commit()
            print(X[0][0])#important
            data1=pd.read_sql_query(sql,mydb)
            data1["action"]=""
            print("************")
            print(data1)
            
            # result=results.drop(["user","dualaccess","dualaccessownerid","status"],axis=1)
            return render_template("attackersearchfileDisplay.html", data1=data1)
        except:
            return render_template("attackersearchfile.html",msg="not found")
    return render_template("attackersearchfile.html")
            

@app.route('/attack/<s1>/<s2>')
def attack(s1, s2):
    print(s1,"dwe",s2)
    c="forworded to filesupload"
    print(c)
    Attack="Attacked"
    sql="update filesupload set Attack='%s' where id='%s' "%(Attack,s1)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('attackersearchfile'))

@app.route("/Viewattckedfiles")
def Viewattckedfiles():
    sql = "SELECT * FROM filesupload where Attack ='Attacked'"
    data1 = pd.read_sql_query(sql, mydb)
    mydb.commit()
    return render_template("Viewattckedfiles.html", data1=data1)

@app.route('/protect/<s1>/<s2>')
def protect(s1=0,s2=""):
    print(s1,"dwe",s2)
    c="forworded to filesupload"
    print(c)
    Attack="Protected"
    sql="update filesupload set Attack='%s' where id='%s' "%(Attack,s1)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('Viewattckedfiles'))

if __name__=="__main__":
    app.run(debug=True)