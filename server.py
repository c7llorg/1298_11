#!/usr/bin/env python3
from flask import Flask, request, render_template, url_for, redirect
import service
from config import SERVER_CONFIG, DIRS

app = Flask(__name__, **DIRS)

def main():
    app.run(**SERVER_CONFIG)

@app.route('/')
def index():
    return render_template('layout.html', page='index.html')

@app.route('/warehouse')
def warehouse():
    return render_template('layout.html', page='warehouse.html', positions=service.get_positions())

@app.route('/checkout', methods=["GET"])
def checkout():
    service.checkout(int(dict(request.args).get('n')))
    return redirect(url_for('warehouse'))

@app.route('/add')
def add():
    return render_template('layout.html', page='upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    return render_template('layout.html', page='upload_result.html', result=service.upload(request.files['file']))

@app.route('/remote')
def remote():
    return render_template('layout.html', page='remote.html', positions=service.get_remote())

@app.route('/checkout_list')
def checkout_list():
    return render_template('layout.html', page='checkout_list.html', positions=service.get_checkout_list())

if __name__ == '__main__':
    main()


