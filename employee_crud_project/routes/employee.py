from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.security import generate_password_hash
import os
import qrcode

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    search_query = request.args.get('search')
    cur = current_app.mysql.connection.cursor()
    if search_query:
        like = f"%{search_query}%"
        cur.execute("SELECT * FROM employee WHERE name LIKE %s OR email LIKE %s OR city LIKE %s", (like, like, like))
    else:
        cur.execute("SELECT * FROM employee")
    employees = cur.fetchall()
    cur.close()
    return render_template('dashboard.html', employees=employees, search_query=search_query)

@employee_bp.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        city = request.form['city']
        photo = request.files['photo']
        photo_filename = photo.filename
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename)

        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        photo.save(upload_path)

        cur = current_app.mysql.connection.cursor()
        cur.execute("INSERT INTO employee (name, username, email, password, city, photo) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, username, email, password, city, photo_filename))
        current_app.mysql.connection.commit()
        employee_id = cur.lastrowid

        # Generate QR Code
        qr_data = str(employee_id)
        qr = qrcode.make(qr_data)

        if not os.path.exists(current_app.config['QR_FOLDER']):
            os.makedirs(current_app.config['QR_FOLDER'])

        safe_name = name.strip().replace(' ', '_').lower()
        qr_filename = f"{safe_name}_{employee_id}.png"
        qr_path = os.path.join(current_app.config['QR_FOLDER'], qr_filename)
        qr.save(qr_path)

        cur.close()
        return redirect('/dashboard')
    return render_template('add_employee.html')

@employee_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    if 'user' not in session:
        return redirect('/')
    cur = current_app.mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        cur.execute("UPDATE employee SET name = %s, email = %s, city = %s WHERE id = %s", (name, email, city, id))
        current_app.mysql.connection.commit()
        cur.close()
        return redirect('/dashboard')
    cur.execute("SELECT * FROM employee WHERE id = %s", (id,))
    employee = cur.fetchone()
    cur.close()
    return render_template('update_employee.html', employee=employee)

@employee_bp.route('/delete/<int:id>')
def delete_employee(id):
    if 'user' not in session:
        return redirect('/')
    cur = current_app.mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE id = %s", (id,))
    current_app.mysql.connection.commit()
    cur.close()
    return redirect('/dashboard')
