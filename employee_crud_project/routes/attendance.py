from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime, date

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance')
def attendance_page():
    return render_template('attendance.html')

@attendance_bp.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    emp_id = data['employee_id']
    today = date.today()

    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT id FROM employee WHERE id = %s", (emp_id,))
    if not cur.fetchone():
        return "Employee not found"

    cur.execute("SELECT * FROM attendance WHERE employee_id = %s AND date = %s", (emp_id, today))
    record = cur.fetchone()
    now = datetime.now().time()

    if not record:
        cur.execute("INSERT INTO attendance (employee_id, date, sign_in) VALUES (%s, %s, %s)",
                    (emp_id, today, now))
        current_app.mysql.connection.commit()
        msg = "Sign In marked at " + now.strftime('%H:%M')
    elif record and not record[4]:
        cur.execute("UPDATE attendance SET sign_out = %s WHERE id = %s", (now, record[0]))
        current_app.mysql.connection.commit()
        msg = "Sign Out marked at " + now.strftime('%H:%M')
    else:
        msg = "Already signed in and out today"

    cur.close()
    return msg
