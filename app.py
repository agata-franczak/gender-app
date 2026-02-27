from flask import Flask, request, render_template, send_file
import pandas as pd
import uuid
import os

app = Flask(__name__)

# Your Google Sheet CSV export link
GENDER_SHEET_URL = "https://docs.google.com/spreadsheets/d/1_xPnU9j8AOjs9sTLqSNfdvlqiHlE_FdW2rdgmqHGfp8/export?format=csv"

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    df_uploaded = pd.read_csv(file)

    # Load gender list from Google Sheet
    df_gender = pd.read_csv(GENDER_SHEET_URL, timeout=10)

    # --- NEW: Detect the first name column ---
    if "first_name" in df_uploaded.columns:
        first_name_col = "first_name"
    elif "First Name" in df_uploaded.columns:
        first_name_col = "First Name"
    else:
        return "CSV must have a column named 'first_name' or 'First Name'", 400
    # ---------------------------------------

    # Normalize to lowercase for merging
    df_uploaded[first_name_col] = df_uploaded[first_name_col].str.lower()
    df_gender["first_name"] = df_gender["first_name"].str.lower()

    # Merge on the detected column
    result = df_uploaded.merge(
        df_gender,
        left_on=first_name_col,
        right_on="first_name",
        how="left"
    )

    # Generate a unique output filename
    unique_name = f"output_{uuid.uuid4().hex}.csv"
    result.to_csv(unique_name, index=False)

    return send_file(unique_name, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
