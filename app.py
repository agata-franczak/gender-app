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
def upload_file():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    df = pd.read_csv(file)

    # --- New part: detect first name column ---
    if "first_name" in df.columns:
        first_name_col = "first_name"
    elif "First Name" in df.columns:
        first_name_col = "First Name"
    else:
        return "CSV must have a column named 'first_name' or 'First Name'", 400
    # --- end of new part ---

    # Existing gender matching code
    result = df.merge(
        gender_df,
        left_on=first_name_col,
        right_on="name",  # assuming your gender list has column 'name'
        how="left"
    )

    # Return updated CSV
    output = BytesIO()
    result.to_csv(output, index=False)
    output.seek(0)
    return send_file(
        output,
        mimetype="text/csv",
        download_name="gender_matched.csv",
        as_attachment=True
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # for Render
    app.run(host="0.0.0.0", port=port, debug=True)
