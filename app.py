from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import csv
import io
import logging

app = Flask(__name__, static_url_path='/static')

# S3 Configuration (bucket name and region)
S3_BUCKET = 'laptopbucket-pythonn'
S3_REGION = 'ap-south-1'

# Initialize S3 Client (with region)
s3 = boto3.client('s3', region_name=S3_REGION)

# Setup basic logging for the application
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/add_manufacturer', methods=['POST'])
def add_manufacturer():
    if request.method == 'POST':
        try:
            # Log to confirm the request came through
            logging.debug("Received POST request to /add_manufacturer")
            
            # Get the form data and log it
            name = request.form['name']
            email = request.form['email']
            phno = request.form['phno']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
            pname = request.form['pname']
            cat = request.form['cat']

            logging.debug(f"Form data: {name}, {email}, {phno}, {country}, {state}, {city}, {pname}, {cat}")
            
            # Prepare data to write to CSV
            csv_data = [name, email, phno, country, state, city, pname, cat]
            
            # Write CSV data to an in-memory file object
            csv_file = io.StringIO()
            writer = csv.writer(csv_file)
            writer.writerow(['Name', 'Email', 'Phone Number', 'Country', 'State', 'City', 'Product Name', 'Category'])
            writer.writerow(csv_data)
            csv_file.seek(0)  # Move to the start of the file

            # Print before S3 upload
            logging.debug("Attempting to upload the CSV to S3")

            # Upload the file to S3
            response = s3.put_object(Bucket=S3_BUCKET, Key='manufacturers.csv', Body=csv_file.getvalue())
            logging.debug(f"S3 response: {response}")

            # Check response for errors
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logging.debug("File uploaded successfully to S3")
                return redirect(url_for('manufacturer_form'))
            else:
                logging.error(f"Failed to upload file: {response}")
                flash(f"Failed to upload file to S3")
                return str(response), 500

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            flash(f"An error occurred: {e}")
            return str(e), 500

    return render_template('manufacturer_form.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/manufacturer_form.html')
def manufacturer_form():
    return render_template('manufacturer_form.html')

if __name__ == '__main__':
    app.secret_key = '32cb68eb67047f9b8ff872f4424a5b23'  # Required for flash messages
    app.run(host='0.0.0.0', port=8001, debug=True)
