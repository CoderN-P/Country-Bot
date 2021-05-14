from flask import Flask, redirect, render_template
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return redirect('https://cbotdiscord.npcool.repl.co/')
    

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()