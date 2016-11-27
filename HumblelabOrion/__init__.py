from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from getallvms import vconnect
from wtforms import StringField, IntegerField
from socketCheck import check_server
from flask_assets import Bundle, Environment
import json


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

env = Environment(app)
js = Bundle('js/jquery-3.1.1.js', 'js/bootstrap.min.js', 'js/typeahead.bundle.js')
env.register('js_all', js)
css = Bundle('css/bootstrap.css', 'css/typeahead.css')
env.register('css_all', css)


class Services(db.Model):
   id = db.Column('service_id', db.Integer, primary_key = True)
   serviceName = db.Column(db.String(100))
   serviceAddress = db.Column(db.String(50))
   servicePort = db.Column(db.Integer)
   serviceStatus = db.Column(db.Boolean)


class RegisterServiceForm(FlaskForm):
    serviceName = StringField('serviceName')
    serviceAddress = StringField('serviceAddress')
    servicePort = IntegerField('servicePort')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        # flash(attempted_username)
        # flash(attempted_password)
        if attempted_username == "admin" and attempted_password == "password":
            flash("Successful Login")
            session['logged_in'] = True
            session['username'] = request.form['username']
            print(session['logged_in'])
            return redirect(url_for('index'))
        else:
            flash("Failure")
            session['logged_in'] = False
    return render_template('index.html')


@app.route('/vms/')
def vms():
    return render_template('vms.html')


@app.route('/update/')
def update():
    si = vconnect()
    the_data = json.loads(si)
    return render_template('vmtable.html', vms=the_data)


@app.route('/vmnames/')
def vmnames():
    si = vconnect()
    the_data = json.loads(si)
    vlist = []
    for i in range(len(the_data)):
        vlist.append(the_data[i]['name'])
    return jsonify(vlist)


@app.route('/vmsearch/')
def vmsearch():
    return render_template('vmsearch.html')


@app.route('/services/')
def service():
    print(session['logged_in'])
    return render_template('services.html')


@app.route('/servicescheck/')
def servicecheck():
    svcs=Services.query.all()
    for sv in svcs:
        updatename = Services.query.filter_by(serviceAddress=sv.serviceAddress).first()
        cs = check_server(sv.serviceAddress, sv.servicePort)
        updatename.serviceStatus = cs
        db.session.commit()
    return render_template('servicetable.html', svcs=Services.query.all())


@app.route('/serviceadd/', methods=['GET', 'POST'])
def register_service():
    try:
        form = RegisterServiceForm(request.form)
        if request.method == "POST":
            requestService = form.serviceName.data
            requestAddress = form.serviceAddress.data
            requestPort = form.servicePort.data
            serv = Services(serviceName=requestService,serviceAddress=requestAddress, servicePort=requestPort)
            db.session.add(serv)
            db.session.commit()
            return redirect(url_for('service'))
    except Exception as e:
        return str(e)
    return render_template('addservice.html')


if __name__ == '__main__':
    db.create_all()
#   app.debug = True
    app.run()
