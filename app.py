#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from pymodbus.client.sync import ModbusTcpClient

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    ip = TextField('IP:', validators=[validators.required()])
    port = TextField('Port:', validators=[validators.required(), validators.Length(min=1, max=65536)])
    adres = TextField('Baslangic Adresi:', validators=[validators.required(), validators.Length(min=0, max=65536)])
    deger = TextField('IP:', validators=[validators.required()])
    unitId = TextField('unitId:', validators=[validators.required()])

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/read-holding-registers", methods=['GET', 'POST'])
def read_holding_regs():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        ip=request.form['ip']
        port=request.form['port']
        adres=request.form['adres']
        deger=request.form['deger']
        unitId=request.form['unitId']
        print ip, " ", port, " ", adres

        host = ip
        port = int(port)
        client = ModbusTcpClient(host, port)
        client.connect()

        rr = client.read_holding_registers(int(adres),int(deger),unit= int(unitId))
        assert(rr.function_code < 0x80)     # test that we are not an error
        print (rr)
        print (rr.registers)



        if form.validate():
            # Save the comment here.
            flash(rr.registers)
            #flash('Thanks for registration ' + ip)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('read-hold-regs.html', form=form)

@app.route("/write-holding-register", methods=['GET', 'POST'])
def write_regs():
        form = ReusableForm(request.form)

        print form.errors
        if request.method == 'POST':
            ip=request.form['ip']
            port=request.form['port']
            address=request.form['address']
            value=request.form['value']
            unitId=request.form['unitId']
            print ip, " ", port, " ", address

            host = ip
            port = int(port)
            client = ModbusTcpClient(host, port)
            client.connect()

            rr = client.write_register(int(address),int(value),unit= int(unitId))
            assert(rr.function_code < 0x80)     # test that we are not an error
            #print (rr)
            #print (rr.registers)



            if form.validate():
                # Save the comment here.
                flash("Success")
                #flash('Thanks for registration ' + ip)
            else:
                flash('Error: All the form fields are required. ')

        return render_template('write-register.html', form=form)

@app.route("/read-coils", methods=['GET', 'POST'])
def coils():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        ip=request.form['ip']
        port=request.form['port']
        adres=request.form['adres']
        deger=request.form['deger']
        unitId=request.form['unitId']
        print ip, " ", port, " ", adres

        host = ip
        port = int(port)
        client = ModbusTcpClient(host, port)
        client.connect()

        rr = client.read_coils(int(adres),int(deger),unit= int(unitId))
        assert(rr.function_code < 0x80)     # test that we are not an error
        print (rr)
        print (rr.bits)



        if form.validate():
            # Save the comment here.

                flash(str(rr.bits))
            #flash((rr.bits))
            #flash('Thanks for registration ' + ip)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('read-coils.html', form=form)

@app.route("/write-coils", methods=['GET', 'POST'])
def write_coils():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        ip=request.form['ip']
        port=request.form['port']
        address=request.form['address']
        value=request.form['value']
        unitId=request.form['unitId']
        print ip, " ", port, " ", address

        host = ip
        port = int(port)
        client = ModbusTcpClient(host, port)
        client.connect()

        rr = client.write_coils(int(address),int(value),unit= int(unitId))
        #assert(rr.function_code < 0x80)     # test that we are not an error




        if form.validate():
            # Save the comment here.
            flash("Success")
        else:
            flash('Error: All the form fields are required. ')

    return render_template('write-coils.html', form=form)



if __name__ == "__main__":
    app.run()
