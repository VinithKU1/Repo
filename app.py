from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Demo exchange rates (fallback)
exchange_rates = {
    "USD": {"INR": 83.0, "EUR": 0.93},
    "INR": {"USD": 0.012, "EUR": 0.011},
    "EUR": {"USD": 1.08, "INR": 89.0}
}

@app.route('/')
def home():
    return render_template("index.html")  # or use jsonify() if you don’t have a frontend

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    amount = data.get("amount")
    from_currency = data.get("from_currency", "").upper()
    to_currency = data.get("to_currency", "").upper()

    if not amount or not from_currency or not to_currency:
        return jsonify({"error": "Invalid input"}), 400

    try:
        # Live rate from exchangerate.host
        res = requests.get("https://api.exchangerate.host/convert",
                           params={"from": from_currency, "to": to_currency})
        rate = res.json()["info"]["rate"]
        converted_amount = amount * rate
    except Exception as e:
        return jsonify({"error": "Failed to fetch exchange rate"}), 500

    return jsonify({
        "from": from_currency,
        "to": to_currency,
        "rate": rate,
        "original_amount": amount,
        "converted_amount": round(converted_amount, 2)
    })

# ✅ Correct single app.run block
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
