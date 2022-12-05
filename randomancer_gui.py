from flask import Flask, render_template, request
from randomancer import init_tables, parse_roll
import webview

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    result = ""
    choice = ""
    if request.args.get("table_choice") is not None:
        choice = request.args.get("table_choice")
        result = parse_roll(choice)
    tables = init_tables()
    return render_template(
        'main.html',
        list=tables.keys(),
        results=result,
        previous=choice
        )

webview.create_window('Randomancer', app)
webview.start()


