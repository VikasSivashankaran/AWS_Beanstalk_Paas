from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import csv
import io

app = Flask(__name__, static_url_path='/static')

# S3 Configuration (bucket name and region)
S3_BUCKET = 'laptopbucket-pythonn'
S3_REGION = 'ap-south-1'

# Initialize S3 Client (with region)
s3 = boto3.client('s3', region_name=S3_REGION)

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/add_manufacturer', methods=['POST'])
def add_manufacturer():
    if request.method == 'POST':
        try:
            # Get the form data and print it to the logs
            name = request.form['name']
            email = request.form['email']
            phno = request.form['phno']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
            pname = request.form['pname']
            cat = request.form['cat']

            print(f"Form data received: {name}, {email}, {phno}, {country}, {state}, {city}, {pname}, {cat}")
            
            # Prepare data to write to CSV
            csv_data = [name, email, phno, country, state, city, pname, cat]
            
            # Write CSV data to an in-memory file object
            csv_file = io.StringIO()
            writer = csv.writer(csv_file)
            writer.writerow(['Name', 'Email', 'Phone Number', 'Country', 'State', 'City', 'Product Name', 'Category'])
            writer.writerow(csv_data)
            csv_file.seek(0)  # Move to the start of the file

            # Print before S3 upload
            print("Uploading to S3...")

            # Upload the file to S3
            response = s3.put_object(Bucket=S3_BUCKET, Key='manufacturers.csv', Body=csv_file.getvalue())
            print(f"S3 response: {response}")

            # If the upload is successful, redirect to the form
            print("Upload successful!")
            return redirect(url_for('manufacturer_form'))

        except Exception as e:
            print(f"Error occurred: {e}")
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
