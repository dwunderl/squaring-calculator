from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

VERSION = "v1.1.1"

def calculate_binomial(base):
    # Calculate components
    nearest_50 = round(base / 50) * 50
    is_below_nearest = base < nearest_50
    difference = abs(base - nearest_50)
    sign = "-" if is_below_nearest else "+"
    
    # Calculate Form 2 and 3 components
    nearest_div_10 = nearest_50 // 10  # Integer division of nearest_50 by 10
    nearest_div_100 = nearest_div_10 / 10.0  # Floating-point division by 10.0
    nearest_div_10_squared = nearest_div_10 * nearest_div_10
    difference_squared = difference * difference
    two_times_nearest_div_100 = int(2 * nearest_div_100)  # Truncate to integer
    
    # Calculate shared components for Stage 4a and 4b
    nearest_50_squared = nearest_50 * nearest_50
    nearest_50_squared_times_100 = nearest_50_squared * 100
    middle_total = 2 * nearest_div_100 * difference * 100
    middle_rup = math.ceil(middle_total / 1000) * 1000  # Round up to next 1000
    middle_delta = middle_rup - middle_total
    
    # Store components for future forms
    components = {
        'base': base,
        'nearest_50': nearest_50,
        'difference': difference,
        'is_below_nearest': is_below_nearest,
        'sign': sign,
        'nearest_div_10': nearest_div_10,
        'nearest_div_100': nearest_div_100,
        'nearest_div_10_squared': nearest_div_10_squared,
        'difference_squared': difference_squared,
        'form2_term1': f"{nearest_div_10}^2 (00)",
        'form2_term2': f"2*{nearest_div_100}*{difference}",
        'form2_term3': f"{difference}^2",
        'form2_expression': f"{nearest_div_10}^2 (00) {sign} 2*{nearest_div_100}*{difference} (00) + {difference}^2",
        'form3_term1': f"{nearest_div_10_squared}",
        'form3_term2': f"{two_times_nearest_div_100}*{difference}",
        'form3_term3': f"{difference_squared}",
        'form3_expression': f"{nearest_div_10_squared} (00) {sign} {two_times_nearest_div_100}*{difference} (00) + {difference_squared}",
        'stage4a_line1': nearest_50_squared_times_100,
        'stage4a_line2': middle_total,
        'stage4a_line3': difference_squared,
        'stage4b_line1': nearest_50_squared_times_100,
        'stage4b_line2': middle_rup,
        'stage4b_line3': middle_delta,
        'stage4b_line4': difference_squared,
        'stage4b_show': is_below_nearest  # Only show if sign is negative
    }
    
    # Build the result including all components
    return {
        'squared_result': base * base,
        'term1': nearest_50,
        'term2': difference,
        'sign': sign,
        'components': components,
        'version': VERSION
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    base = int(data.get('base', 0))
    
    if not (10 <= base <= 999):
        return jsonify({'error': 'Please enter a 2 or 3-digit number (10-999)'}), 400
        
    result = calculate_binomial(base)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)
