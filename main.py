from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def meat_to_carbon(meat_weight):
    emission_constant = 59.5
    carbon = emission_constant * meat_weight
    return carbon

# Load restaurant data
restaurants = {}
with open('Data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        restaurant = row['Resturant']
        meal = row['Meal']
        weight = float(row['Pounds of Meat'])
        if restaurant not in restaurants:
            restaurants[restaurant] = []
        restaurants[restaurant].append((meal, weight))

@app.route('/')
def index():
    return render_template('index.html', restaurants=restaurants)

@app.route('/calculate', methods=['POST'])
def calculate():
    selected_restaurant = request.form['restaurant']
    selected_meal_index = int(request.form['meal'])
    selected_meal, selected_weight = restaurants[selected_restaurant][selected_meal_index]
    carbon = meat_to_carbon(selected_weight)
    return render_template('result.html', restaurant=selected_restaurant, meal=selected_meal, carbon=carbon)

if __name__ == '__main__':
    app.run(debug=True)