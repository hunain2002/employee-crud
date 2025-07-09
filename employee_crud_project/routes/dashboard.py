from flask import Blueprint, render_template, current_app, request

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/admin_dashboard')
def admin_dashboard():
    try:
        mysql = current_app.mysql
        cur = mysql.connection.cursor()

        cur.execute("SELECT COUNT(*) FROM employee")
        total_employees = cur.fetchone()[0]

        cur.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance WHERE date = CURDATE()")
        present_today = cur.fetchone()[0]

        absent_today = total_employees - present_today

        cur.execute("""
            SELECT date, COUNT(DISTINCT employee_id) as present
            FROM attendance
            WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY date
            ORDER BY date
        """)
        rows = cur.fetchall()

        labels = [row[0].strftime('%Y-%m-%d') for row in rows]
        data = [row[1] for row in rows]

        cur.execute("SELECT * FROM employee")
        employees = cur.fetchall()

        cur.close()

        return render_template("dashboard.html",
            total=total_employees,
            present=present_today,
            absent=absent_today,
            labels=labels,
            data=data,
            employees=employees
        )
    except Exception as e:
        return str(e)
