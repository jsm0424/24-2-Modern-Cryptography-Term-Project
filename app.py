from flask import Flask, render_template, request, jsonify
import json
import random
from encryption.he import HEManager

app = Flask(__name__)

# Initialize HE Manager and load results
he_manager = HEManager()
results = {"wins": 0, "losses": 0}

# Load results from file
try:
    with open("data/results.json", "r") as f:
        results = json.load(f)
except FileNotFoundError:
    pass

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("index.html")


@app.route("/flip_coin", methods=["POST"])
def flip_coin():
    """Simulate a coin flip and determine if the user wins or loses."""
    global results

    # Get user choice (0 for Head, 1 for Tail)
    user_choice = int(request.form["choice"])

    # Encrypt user choice
    encrypted_user_choice = he_manager.encrypt_choice(user_choice)

    # Simulate coin flip (0 for Head, 1 for Tail)
    coin_flip = random.randint(0, 1)
    encrypted_coin_flip = he_manager.encrypt_choice(coin_flip)

    # Compare encrypted values to determine the result
    encrypted_result = he_manager.compare_choices(encrypted_user_choice, encrypted_coin_flip)
    result = he_manager.decrypt_result(encrypted_result)

    # Update results
    if result == 1:  # User wins
        results["wins"] += 1
        outcome = "win"
    else:  # User loses
        results["losses"] += 1
        outcome = "lose"

    # Save results to file
    with open("data/results.json", "w") as f:
        json.dump(results, f)

    # Truncate serialized encrypted data
    def truncate(data):
        return data.serialize().hex()[:30]  # Only include the first 30 characters

    # Return truncated encrypted data and results
    return jsonify({
        "outcome": outcome,
        "coinFlip": coin_flip,
        "encryptedUserChoice": truncate(encrypted_user_choice),
        "encryptedCoinFlip": truncate(encrypted_coin_flip),
        "encryptedResult": truncate(encrypted_result),
        "wins": results["wins"],
        "losses": results["losses"]
    })

if __name__ == "__main__":
    app.run(debug=True)
