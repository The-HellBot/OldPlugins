from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def start():
    return "HellBot Started Successfully"

os.system("python3 -m TelethonHell/__main__.py")
app.run(port=5000)
