#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText

from flask.app import Flask
from flask.globals import request
from flask.templating import render_template
import mysql.connector

#from flask import  session

#import MySQLdb
app=Flask(__name__)
'''app = Flask(__name__,
            #static_url_path='', 
            static_folder='static',
            template_folder='templates')'''
#con=MySQLdb.connect(host='localhost',user='stk',passwd='stk',port=3306,db='armstrong health club')
con = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='armstrong health club')

cmd=con.cursor(buffered=True)


@app.route('/')
def log():
    return render_template('log1.html')
@app.route('/home')
def home():
    return render_template('Home.html')
@app.route('/user')
def user():
    return render_template('userhome.html')



@app.route('/find')
def find():
    return render_template('find.html')
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/forgoten', methods=['POST','GET'])
def forgotten():
    return render_template('forgottenPsswrd.html')
@app.route('/preg')
def preg():
    return render_template('admin.html')
@app.route('/eqpmnt')
def eqpmnt():
    return render_template('Equipment.html')
@app.route('/ppay',methods=['GET','POST'])
def ppay():
    cmd.execute("select name,year,month,ammount from account A INNER JOIN PLAYER P ON P.Id = A.Player_Id")
    s=cmd.fetchall()
    cmd.execute("select Id,Name from player")
    pname=cmd.fetchall()
    return render_template('ppay.html',val=s,pname = pname)
@app.route('/treg')
def treg():
    return render_template('treg.html')
@app.route('/nutri')
def nutri():
    return render_template('Nutrition.html')
@app.route('/tips')
def tips():
    return render_template('tips.html')
@app.route('/notification')
def noti():
    return render_template('user_viewnoti.html')

@app.route('/playerList' , methods=['POST','GET'])
def playerList():
    cmd.execute("select  Name,Address,DOB,Email,Phone_Number,course from player")
    data=cmd.fetchall()
    return render_template('TrPlayerList.html',data=data)

@app.route('/login', methods=['POST'] )
def login():
    email=request.form['txt1']
    passwrd=request.form['txt2']
    #session['username'] = email
    #session["passwrd"] = passwrd
    global sesemail
    global sespasw
    cmd.execute("select * from login where email='"+email+"' and password='"+passwrd+"'")
    lg=cmd.fetchone()
    if lg is None:
        return '''<script> alert('INVALID USERNAME OR PASSWORD'); window.location='/'</script>'''
    elif lg[3]=='admin':
        return  render_template('admin.html')
    elif lg[3] == 'trainer':
        sesemail = email
        sespasw = passwrd
        cmd.execute("select * from trainer where email='"+email+"' and password='"+passwrd+"' limit 1")
        s=cmd.fetchall()
        return render_template('trainerhome.html',val=s)
    elif lg[3] == 'player':
        sesemail = email
        sespasw = passwrd
        cmd.execute("select * from player where email='"+email+"' and password='"+passwrd+"' limit 1")
        s=cmd.fetchall()
        return render_template('userhome.html',val=s)

    else:
        return '''<script> alert('INVALID USERNAME OR PASSWORD'); window.location='/'</script>'''

@app.route('/userprof')
def userprof():
    cmd.execute("select * from player where email='"+sesemail+"' and password='"+sespasw+"'")
    s=cmd.fetchall()
    return render_template('userhome.html',val=s)

@app.route('/trhome')
def trhome():
    cmd.execute("select * from trainer where email='"+sesemail+"' and password='"+sespasw+"'")
    s=cmd.fetchall()
    return render_template('trainerhome.html',val=s)

@app.route('/vaddnoti',methods=['POST','GET'])
def vaddnoti():
    cmd.execute("select * from notification")
    s = cmd.fetchall()
    return render_template('ad_addnoti.html', val=s)

@app.route('/plviewNotifi',methods=['POST','GET'])
def plviewNotifi():
    cmd.execute("select * from notification")
    s = cmd.fetchall()
    return render_template('plviewNotific.html', val=s)

@app.route('/plyviewtips',methods=['POST','GET'])
def plyviewtips():
    cmd.execute("select * from tips")
    s = cmd.fetchall()
    return render_template('PlyViewtips.html', val=s)

@app.route('/plyviewnutri',methods=['POST','GET'])
def plyviewnutri():
    cmd.execute("select * from nutrition")
    s = cmd.fetchall()
    return render_template('PlyViewNutri.html', val=s)

@app.route('/addnoti',methods=['POST','GET'])
def addnoti():
    noti=request.form['noti']

    cmd.execute("insert into  notification values(null,curdate(),'"+str(noti)+"')")

    cmd.execute("select * from notification")
    s=cmd.fetchall()
    con.commit()
    #return render_template('ad_addnoti.html',val=s)
    return '''<script> alert('Notification Posted Successfully !'); window.location='/viewnoti'</script>'''

@app.route('/viewnoti',methods=['POST','GET'])
def viewnoti():
    cmd.execute("select * from notification")
    s=cmd.fetchall()
    return render_template('ad_addnoti.html',val=s)

@app.route('/listdata',methods=['POST','GET'])
def listdata():
    listtype=request.form['select']
    data = ""
    print(listtype)
    if listtype == "Trainer":
        cmd.execute("select trainer_name,Address,Dob,email,Phone_number,Department from trainer")
        data=cmd.fetchall()
    else:
        cmd.execute("select  Name,Address,DOB,Email,Phone_Number,course from player")
        data=cmd.fetchall()
    print(data)
    return render_template('Find.html',data=data)

@app.route('/playerreg',methods=['POST'])
def playerreg():
    name=request.form['textfield']
    address=request.form['textarea']
    sex=request.form['radio']
    dob=request.form['textfield1']
    email = request.form['textfield2']
    passwd=request.form['textfield3']
    phnum=request.form['textfield4']
    course=request.form.getlist('checkbox')
    print(sex)
    crs=""
    for i in course:
        crs=i+","+crs
    print(crs)
    height = request.form['textfield5']
    weight = request.form['textfield6']
    bloodgrp=request.form['select']
    bloodprsr=request.form['textfield7']
    cholesterole=request.form['textfield8']
    regfee=request.form['textfield9']

    sql="INSERT INTO login(email,password,type)VALUES(%s, %s, %s)"
    val = (email,passwd,'player')
    cmd.execute(sql, val)

    #id=con.insert_id()
    cmd.execute("select MAX(ID)+1 as Id from player;")
    id =cmd.fetchone()
    sql="INSERT INTO player(Id,name,address,sex,dob,email,password,phone_number,course,height,weight,blood_group,blood_pressure,cholesterol_rate,regfee)VALUES(%s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)"
    val = (id[0],name, address,sex,dob,email,passwd,phnum,crs,height,weight,bloodgrp,bloodprsr,cholesterole,regfee)
    cmd.execute(sql, val)
    con.commit()
    mesg = "";
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('mikhil.amk@gmail.com', '112mikhil@')

    except Exception as e:
        mesg = "New Player Created Successfully Please Check Your Internet Connectivity !"
        return "'''<script> alert('"+mesg+"'); window.location='/preg'</script>'''"

    msg = MIMEText("Your password is " + passwd)

    msg['Subject'] = 'ArmStrong Health Club Secret Password...'

    msg['To'] = email

    msg['From'] = 'mikhil.amk@gmail.com'

    try:
        gmail.send_message(msg)

    except Exception as e:
        mesg = "New Player Created Successfully Please Check Your  Internet Connectivity !"
        return "'''<script> alert('"+mesg+"'); window.location='/preg'</script>'''"
    mesg = "New Player Created Successfully Please Refer Your Email For Password !"
    return "'''<script> alert('"+mesg+"'); window.location='/preg'</script>'''"

@app.route('/trainerreg', methods=['POST'] )
def trainerreg():
    name=request.form['textfield0']
    address=request.form['textarea']
    dob=request.form['textfield1']
    email=request.form['textfield2']
    passwd=request.form['textfield3']
    phnnum=request.form['textfield4']
    departmnt=request.form['radio']
    achievmnts=request.form['textfield5']
    specialztn=request.form['textfield6']
    #cmd.execute("insert into login values('" + str(email) + "','" + str(passwd) + "','trainer')")
    sql="INSERT INTO login(email,password,type)VALUES(%s, %s, %s)"
    val = (email,passwd,'trainer')
    cmd.execute(sql, val)

    #id=con.insert_id()
    #cmd.execute("insert into trainer values('"+str(id)+"','"+str(name)+ "','"+ str(address)+"','"+str(departmnt)+"','"+str(dob)+"','"+str(email)+"','"+str(phnnum)+"','"+ str(specialztn)+"','"+str(achievmnts)+"','"+ str(passwd)+"')")
    
    cmd.execute("select MAX(ID)+1 as Id from trainer;")
    id =cmd.fetchone()

    sql="INSERT INTO trainer(Id,trainer_name,address,department,dob,email,phone_number,specialisation,achievement,password)VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)"
    val = (id[0],name, address,departmnt,dob,email,phnnum,specialztn,achievmnts,passwd)
    cmd.execute(sql, val)
    con.commit()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('mikhil.amk@gmail.com', '112mikhil@')

    except Exception as e:
        mesg = "New Trainer Created Successfully Please Check Your Internet Connectivity !"
        return "'''<script> alert('"+mesg+"'); window.location='/treg'</script>'''"

    msg = MIMEText("Your password is " + passwd)

    msg['Subject'] = 'ArmStrong Health Club Secret Password...'

    msg['To'] = email

    msg['From'] = 'mikhil.amk@gmail.com'

    try:
        gmail.send_message(msg)

    except Exception as e:
        mesg = "New Trainer Created Successfully Please Check Your  Internet Connectivity !"
        return "'''<script> alert('"+mesg+"'); window.location='/treg'</script>'''"
    mesg = "New Trainer Created Successfully Please Refer Your Email For Password !"
    return "'''<script> alert('"+mesg+"'); window.location='/treg'</script>'''"


@app.route('/playerpay', methods=['POST'])
def playerpay():
    player_id=request.form['select0']
    amount=request.form['textfield0']
    month=request.form['select1']
    year=request.form['select2']
    cmd.execute("insert into account values(null,'" + str(player_id) + "','" + str(amount) + "','" + str(month) + "','" + str(year) + "')")
    con.commit()
    return '''<script> alert('SUCCESSFULLY INSERTED'); window.location='/ppay'</script>'''


@app.route('/eqp', methods=['POST'])
def eqp():
    eqpmntname=request.form['textfield0']
    eqclass=request.form['select0']
    quantity=request.form['textfield1']
    description=request.form['textarea']
    cmd.execute("insert into equipment values(null,'" + str(eqpmntname) + "','" + str(eqclass) + "','" + str(quantity) + "','" + str(description) + "')")
    con.commit()
    return '''<script> alert('SUCCESSFULLY INSERTED'); window.location='/eqpmnt'</script>'''


@app.route('/nutrition', methods=['POST'])
def nutrition():
        nutriid = request.form['textfield3']
        nutriname = request.form['textfield2']
        date = request.form['textfield4']
        cmd.execute("insert into nutrition values('" + str(nutriid) + "','" + str(nutriname) + "','" + str(date) + "')")
        con.commit()
        return '''<script> alert('Nutrition Added Successfully !'); window.location='/nutri'</script>'''


@app.route('/tip', methods=['POST'])
def tip():
        mudcr = request.form['textarea1']
        mudate= request.form['textfield1']
        zodcr = request.form['textarea2']
        zodate = request.form['textfield2']
        yodcr = request.form['textarea3']
        yodate=request.form['textfield4']
        sql="INSERT INTO tips(Mu_Descrption,Mu_Date,Zo_Description,Zo_Date,Yo_Description,Yo_Date)VALUES(%s,%s, %s, %s,%s, %s)"
        val = (mudcr,mudate, zodcr,zodate,yodcr,yodate)
        cmd.execute(sql, val)
        con.commit()
        return '''<script> alert('New Tips Added Sucessfully !'); window.location='/tips'</script>'''


@app.route('/forgot', methods=['POST','GET'])
def fPsswrd():
    email=request.form['txt1']
    cmd.execute("select  * from login where email='"+email+"' and password<>''")
    print(cmd)
    s=cmd.fetchone()
    print(s)
    # email = request.args.get('email')
    # msg = Message('Booking Confirmed ', sender='project2016mails@gmail.com', recipients=["select email from booking where status='accepted'"])
    # msg.body = 'Confirmed your booking'
    # mail.send(msg)



    if s is None:
        return '''<script> alert('Invalid emailid'); window.location='/'</script>'''
    else:
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('mikhil.amk@gmail.com', '112mikhil@')

        except Exception as e:
            print("Couldn't setup email!!" + str(e))

        msg = MIMEText("Your password is " + s[2])

        msg['Subject'] = 'ArmStrong Health Club Forgot Password...'

        msg['To'] = email

        msg['From'] = 'mikhil.amk@gmail.com'

        try:

            gmail.send_message(msg)

        except Exception as e:

            print("COULDN'T SEND EMAIL", str(e))

        return '''<script> alert('Please Check Your  EmailId for Your Password'); window.location='/'</script>'''


if __name__=="__main__":
    app.run(debug=True)
