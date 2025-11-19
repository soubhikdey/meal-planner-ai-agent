from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os
import webbrowser
import threading

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

model = genai.GenerativeModel("models/gemini-pro-latest")



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    goal = request.form["goal"]
    preference = request.form["preference"]
    budget = request.form["budget"]
    days = request.form["days"]

    prompt = f"""
    Create a {days}-day Indian meal plan.
    Goal: {goal}
    Food Preference: {preference}
    Budget level: {budget}

    Provide:
    - Breakfast, Lunch, Dinner for each day
    - Calories for each meal
    - Daily total calories
    - Combined shopping list
    Present it in clean text format.
    """

    response = model.generate_content(prompt)
    result = response.text

    return render_template("index.html", result=result)


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=True)
