from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def start():
    return "HellBot Started Successfully"

os.system("bash hell")
app.run(port=5000)
