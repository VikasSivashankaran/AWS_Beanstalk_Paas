from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import csv
import io
import logging

app = Flask(__name__, static_url_path='/static')

# Configuration for the S3 bucket and region
S3_BUCKET = 'laptopbucket-pythonn'
S3_REGION = 'ap-south-1'

# Creating an S3 client
s3 = boto3.client('s3', region_name=S3_REGION)

# Setting up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/add_manufacturer', methods=['POST'])
def add_manufacturer():
    if request.method == 'POST':
        try:
            logging.debug("Received POST request to /add_manufacturer")
            
            # Fetching form data
            name = request.form['name']
            email = request.form['email']
            phno = request.form['phno']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
            pname = request.form['pname']
            cat = request.form['cat']

            logging.debug(f"Form data: {name}, {email}, {phno}, {country}, {state}, {city}, {pname}, {cat}")
            
            # Prepare new data
            csv_data = [name, email, phno, country, state, city, pname, cat]
            
            # Initialize CSV file content
            csv_file = io.StringIO()
            writer = csv.writer(csv_file)
            
            # Attempt to download the existing file from S3
            try:
                existing_obj = s3.get_object(Bucket=S3_BUCKET, Key='manufacturers_data/manufacturers.csv')
                existing_csv_content = existing_obj['Body'].read().decode('utf-8')
                csv_file.write(existing_csv_content)
                csv_file.seek(0, io.SEEK_END)  # Move to the end to append new row
            except s3.exceptions.NoSuchKey:
                # If the file doesn't exist, we will create a new one
                logging.debug("No existing CSV found, creating a new file.")
                writer.writerow(['Name', 'Email', 'Phone Number', 'Country', 'State', 'City', 'Product Name', 'Category'])

            # Append new data
            writer.writerow(csv_data)
            csv_file.seek(0)  # Reset pointer to the start of the file for upload
            
            logging.debug("Attempting to upload the updated CSV to S3 inside the manufacturers_data folder.")

            # Upload the updated CSV file to the S3 bucket
            response = s3.put_object(
                Bucket=S3_BUCKET, 
                Key='manufacturers_data/manufacturers.csv',  # Add folder name before file name
                Body=csv_file.getvalue()
            )

            logging.debug(f"S3 response: {response}")

            # Check for successful upload
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
    app.run(host='0.0.0.0', port=8001, debug=True)
