import os
from dotenv import load_dotenv
import google.generativeai as genai
from fpdf import FPDF

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_meal_plan(goal, budget, preference, days):
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
    """

    response = model.generate_content(prompt)
    return response.text

def save_to_pdf(text, filename="MealPlan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    print(f"\nPDF saved as {filename}")

def main():
    print("\n===== MEALPLANNER AGENT =====\n")

    goal = input("Enter your fitness goal (weight-loss/weight-gain/general): ")
    preference = input("Preference (veg/non-veg/vegan): ")
    budget = input("Budget level (low/medium/high): ")
    days = input("Number of days to plan (e.g., 3): ")

    print("\nGenerating your meal plan... (takes 5–10 seconds)\n")
    meal_plan = generate_meal_plan(goal, budget, preference, days)

    print("\n=== Your Meal Plan ===\n")
    print(meal_plan)

    save_to_pdf(meal_plan)

if __name__ == "__main__":
    main()
