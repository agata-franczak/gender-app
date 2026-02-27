from flask import Flask, request, render_template, send_file
import pandas as pd
import uuid

app = Flask(__name__)

# PASTE your Google Sheet export link here
GENDER_SHEET_URL = "https://docs.google.com/spreadsheets/d/1_xPnU9j8AOjs9sTLqSNfdvlqiHlE_FdW2rdgmqHGfp8/export?format=csv"

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    df_uploaded = pd.read_csv(file)

    df_gender = pd.read_csv(GENDER_SHEET_URL)

    df_uploaded["first_name"] = df_uploaded["first_name"].str.lower()
    df_gender["first_name"] = df_gender["first_name"].str.lower()

    result = df_uploaded.merge(
        df_gender,
        on="first_name",
        how="left"
    )

    unique_name = f"output_{uuid.uuid4().hex}.csv"
    result.to_csv(unique_name, index=False)

    return send_file(unique_name, as_attachment=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
