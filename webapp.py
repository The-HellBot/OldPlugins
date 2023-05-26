from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def start():
    return "HellBot Started Successfully"

subprocess.call(["bash","-c",cmd])
app.run(port=5000)
