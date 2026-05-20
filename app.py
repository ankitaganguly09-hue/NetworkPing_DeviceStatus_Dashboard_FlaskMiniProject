from flask import Flask, redirect, render_template, request
import subprocess
import platform

app = Flask(__name__)

devices = []

def ping_device(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", param, "1", ip]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return result.returncode == 0

@app.route('/')
def home():

    # Update device status
    for device in devices:
        device["status"] = "Online" if ping_device(device["ip"]) else "Offline"

    return render_template("index.html", devices=devices)

@app.route('/add', methods=['POST'])
def add_device():
    name = request.form['name']
    ip = request.form['ip']

    devices.append({"name": name, "ip": ip, "status": "Unknown"})

    return render_template("index.html", devices=devices)

@app.route("/refresh")
def refresh():

    for device in devices:
        device["status"] = "Online" if ping_device(device["ip"]) else "Offline"

    return redirect("/")