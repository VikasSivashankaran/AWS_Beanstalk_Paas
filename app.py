from flask import Flask, render_template, request, redirect, url_for
import boto3
import csv
import io

app = Flask(__name__, static_url_path='/static')

# S3 Configuration (bucket name only, no credentials)
S3_BUCKET = 'laptopbucket-pythonn'

# Initialize S3 Client (IAM role will handle the authentication)
s3 = boto3.client('s3')

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/add_manufacturer', methods=['POST'])
def add_manufacturer():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        pname = request.form['pname']
        cat = request.form['cat']

        # Prepare data to write to CSV
        csv_data = [name, email, phno, country, state, city, pname, cat]

        # Write CSV data to an in-memory file object
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(['Name', 'Email', 'Phone Number', 'Country', 'State', 'City', 'Product Name', 'Category'])
        writer.writerow(csv_data)
        csv_file.seek(0)  # Move to the start of the file

        # Upload the file to S3
        s3.put_object(Bucket=S3_BUCKET, Key='manufacturers.csv', Body=csv_file.getvalue())

        return redirect(url_for('manufacturer_form'))

    return render_template('manufacturer_form.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/manufacturer_form.html')
def manufacturer_form():
    return render_template('manufacturer_form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001, debug=True)
