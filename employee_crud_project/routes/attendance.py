from flask import Blueprint, render_template, request, current_app
from datetime import datetime, date
import base64
import os

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance')
def attendance_page():
    return render_template('attendance.html')

@attendance_bp.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    emp_id = data.get('employee_id')
    today = date.today()

    if not emp_id:
        return "Employee ID missing", 400

    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT id FROM employee WHERE id = %s", (emp_id,))
    if not cur.fetchone():
        cur.close()
        return "Employee not found", 404

    cur.execute("SELECT * FROM attendance WHERE employee_id = %s AND date = %s", (emp_id, today))
    record = cur.fetchone()
    now = datetime.now().time()

    if not record:
        cur.execute(
            "INSERT INTO attendance (employee_id, date, sign_in) VALUES (%s, %s, %s)",
            (emp_id, today, now)
        )
        msg = "Sign In marked at " + now.strftime('%H:%M')
    elif record and not record[4]:
        cur.execute(
            "UPDATE attendance SET sign_out = %s WHERE id = %s",
            (now, record[0])
        )
        msg = "Sign Out marked at " + now.strftime('%H:%M')
    else:
        msg = "Already signed in and out today"

    current_app.mysql.connection.commit()
    cur.close()
    return msg

@attendance_bp.route('/mark_attendance_photo', methods=['POST'])
def mark_attendance_photo():
    emp_id = request.form.get('employee_id')
    photo_data = request.form.get('photo')

    if not emp_id or not photo_data:
        return "Missing employee ID or photo data", 400

    try:
        header, encoded = photo_data.split(",", 1)
        binary_data = base64.b64decode(encoded)
    except Exception as e:
        return f"Invalid image data: {str(e)}", 400

    today = date.today()
    now = datetime.now().time()

    folder = os.path.join('static', 'attendance_photos')
    os.makedirs(folder, exist_ok=True)

    filename = f"{emp_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, "wb") as f:
            f.write(binary_data)
    except Exception as e:
        return f"Failed to save photo: {str(e)}", 500

    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT * FROM attendance WHERE employee_id = %s AND date = %s", (emp_id, today))
    record = cur.fetchone()

    if not record:
        cur.execute(
            "INSERT INTO attendance (employee_id, date, sign_in, photo) VALUES (%s, %s, %s, %s)",
            (emp_id, today, now, filename)
        )
        msg = "Sign In (with photo) marked at " + now.strftime('%H:%M')
    elif not record[4]:
        cur.execute(
            "UPDATE attendance SET sign_out = %s WHERE id = %s",
            (now, record[0])
        )
        msg = "Sign Out (photo saved) marked at " + now.strftime('%H:%M')
    else:
        msg = "Already signed in and out today"

    current_app.mysql.connection.commit()
    cur.close()
    return msg
