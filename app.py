from flask import Flask, render_template, request
from scanner import scan_url
import json
import os

app = Flask(__name__)


# ==========================================
# Load Model Performance Metrics
# ==========================================

def load_model_metrics():

    metrics_file = "model/model_metrics.json"

    if os.path.exists(metrics_file):

        with open(metrics_file, "r") as file:

            return json.load(file)

    return {
        "accuracy": 0,
        "precision": 0,
        "recall": 0,
        "f1_score": 0
    }


# ==========================================
# Home Route
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    # Load model metrics
    metrics = load_model_metrics()

    # ======================================
    # URL Scanning
    # ======================================

    if request.method == "POST":

        url = request.form.get(
            "url",
            ""
        ).strip()

        if url:

            result = scan_url(url)

    # ======================================
    # Render Website
    # ======================================

    return render_template(
        "index.html",
        result=result,
        metrics=metrics
    )


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )