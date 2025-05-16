from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Demo exchange rates (can be replaced with live ones)
exchange_rates = {
    "USD": {"INR": 83.0, "EUR": 0.93},
    "INR": {"USD": 0.012, "EUR": 0.011},
    "EUR": {"USD": 1.08, "INR": 89.0}
}

@app.route('/')
def home():
    return render_template("index.html")  # Make sure index.html is inside the 'templates' folder

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
    amount = data.get("amount")
    from_currency = data.get("from_currency", "").upper()
    to_currency = data.get("to_currency", "").upper()

    if not amount or not from_currency or not to_currency:
        return jsonify({"error": "Invalid input"}), 400

    try:
        # Try to fetch live exchange rate
        res = requests.get("https://api.exchangerate.host/convert", params={
            "from": from_currency,
            "to": to_currency
        })
        rate = res.json()["info"]["rate"]
        converted_amount = amount * rate
    except Exception:
        return jsonify({"error": "Failed to fetch exchange rate"}), 500

    return jsonify({
        "from": from_currency,
        "to": to_currency,
        "rate": rate,
        "original_amount": amount,
        "converted_amount": round(converted_amount, 2)
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Railway uses PORT env variable
    app.run(host='0.0.0.0', port=port)
