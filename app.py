from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_energy_charge(units):
    """Calculate the energy charge based on unit slabs."""
    energy_charge = 0
    
    if units <= 120:
        energy_charge = units * 6
    elif units <= 240:
        energy_charge = (120 * 6) + (units - 120) * 7.3
    elif units <= 360:
        energy_charge = (120 * 6) + (120 * 7.3) + (units - 240) * 8.2
    elif units <= 480:
        energy_charge = (120 * 6) + (120 * 7.3) + (120 * 8.2) + (units - 360) * 8.4
    else:
        energy_charge = (120 * 6) + (120 * 7.3) + (120 * 8.2) + (120 * 8.4) + (units - 480) * 8.4
    
    return energy_charge


def calculate_bill(units):
    """Calculate the total electricity bill based on given details."""
    # Fixed charges
    fixed_charge = 138.08
    
    # Calculate energy charge
    energy_charge = calculate_energy_charge(units)
    
    # Electricity duty: 5% of (energy charge + fixed charge)
    electricity_duty = 0.05 * (energy_charge + fixed_charge)
    
    # Government subsidy: valid for up to 120 units
    subsidy = 0.75 * units if units <= 120 else 0.75 * 120
    
    # Total bill
    total_bill = (energy_charge + electricity_duty + fixed_charge) - subsidy
    
     # Round the total bill to two decimal places
    total_bill = round(total_bill, 2)
    
    return {
        "Energy Charge": energy_charge,
        "Electricity Duty": electricity_duty,
        "Fixed Charge": fixed_charge,
        "Subsidy": subsidy,
        "Total Bill": total_bill
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        units_consumed = request.form['units']
        if not units_consumed.isdigit() or int(units_consumed) <= 0:
            return "Please enter a valid positive integer for units consumed."
        
        units_consumed = int(units_consumed)
        
        # Calculate the bill
        bill_details = calculate_bill(units_consumed)
        return render_template('result.html', bill_details=bill_details)
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    app.run(debug=True)
