#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from pymodbus.client.sync import ModbusTcpClient

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

class ReusableForm(Form):
    ip = TextField('IP:')
    port = TextField('Port:')
    adres = TextField('Start address:')
    value = TextField('IP:')
    unitId = TextField('unitId:')

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
        address=request.form['address']
        value=request.form['value']
        unitId=request.form['unitId']
        print ip, " ", port, " ", address

        host = ip
        port = int(port)
        client = ModbusTcpClient(host, port)
        client.connect()

        rr = client.read_holding_registers(int(address),int(value),unit= int(unitId))
        assert(rr.function_code < 0x80)     # test that we are not an error
        print (rr)
        print (str(rr.registers))

        if form.validate():
            flash(str(rr.registers))
        else:
            flash("Error")

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
                flash("Success!")
                #flash('Thanks for registration ' + ip)
            else:
                flash('Error')

        return render_template('write-register.html', form=form)

@app.route("/read-coils", methods=['GET', 'POST'])
def read_coils():
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

        rr = client.read_coils(int(address),int(value),unit= int(unitId))
        assert(rr.function_code < 0x80)     # test that we are not an error
        print (rr)
        print (rr.bits)

        if form.validate():
            flash(str(rr.bits))
        else:
            flash('Error')

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
        assert(rr.function_code < 0x80)     # test that we are not an error

        if form.validate():
            flash("Success")
        else:
            flash('Error')

    return render_template('write-coils.html', form=form)


if __name__ == "__main__":
    app.run()
