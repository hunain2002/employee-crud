from flask import Blueprint, render_template, current_app

dashboard_bp = Blueprint('dashboard', __name__)  # Correct blueprint name

@dashboard_bp.route('/admin_dashboard')
def admin_dashboard():
    try:
        mysql = current_app.mysql
        cur = mysql.connection.cursor()

        # Total employees
        cur.execute("SELECT COUNT(*) FROM employee")
        total_employees = cur.fetchone()[0]

        # Employees present today
        cur.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance WHERE date = CURDATE()")
        present_today = cur.fetchone()[0]

        # Calculate absent employees
        absent_today = total_employees - present_today

        # Weekly attendance data
        cur.execute("""
            SELECT date, COUNT(DISTINCT employee_id) as present
            FROM attendance
            WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY date
            ORDER BY date
        """)
        rows = cur.fetchall()

        # Format for chart.js
        labels = [row[0].strftime('%Y-%m-%d') for row in rows]
        data = [row[1] for row in rows]

        cur.close()

        return render_template("admin_dashboard.html",
            total=total_employees,
            present=present_today,
            absent=absent_today,
            labels=labels,
            data=data
        )
    except Exception as e:
        return f"<h3>⚠️ Error in Dashboard Route:</h3><pre>{str(e)}</pre>"
