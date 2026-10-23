from flask import Flask, request, render_template, session, make_response
import os
import csv
import io
from codes import run_conversion_single

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    # Use getlist to capture multiple files from the 'input_file' field
    files = request.files.getlist('input_file')
    if not files or files[0].filename == '':
        return "No selected files", 400

    os.makedirs("uploads", exist_ok=True)
    all_extracted_data = []

    for file in files:
        temp_path = os.path.join("uploads", file.filename)
        file.save(temp_path)
        try:
            data = run_conversion_single(temp_path)
            all_extracted_data.append(data)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Store the list of results in the session
    session['all_extracted_data'] = all_extracted_data
    return render_template("results.html", results=all_extracted_data)

@app.route('/download')
def download_file():
    all_data = session.get('all_extracted_data', [])
    if not all_data:
        return "No data available to download", 400
    
    si = io.StringIO()
    cw = csv.writer(si)
   
    # Write headers using the keys from the first dictionary
    headers = [key.replace('_', ' ').title() for key in all_data[0].keys()]
    cw.writerow(headers)

    # Write each file's data as a new row
    for row_data in all_data:
        cw.writerow(list(row_data.values()))
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=extracted_data.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == "__main__":
    app.run(debug=True)