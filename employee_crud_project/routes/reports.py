# routes/reports.py

from flask import Blueprint, send_file, current_app
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from io import BytesIO

# Blueprint registration with correct name
reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/export/employees/xlsx')
def export_employees_xlsx():
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT id, name, username, email, city FROM employee")
    employees = cur.fetchall()
    cur.close()

    # Create XLSX file
    wb = Workbook()
    ws = wb.active
    ws.append(['ID', 'Name', 'Username', 'Email', 'City'])

    for emp in employees:
        ws.append(emp)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='employees.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@reports_bp.route('/export/attendance/pdf')
def export_attendance_pdf():
    cur = current_app.mysql.connection.cursor()
    cur.execute("""
        SELECT a.id, e.name, a.date, a.sign_in, a.sign_out 
        FROM attendance a 
        JOIN employee e ON a.employee_id = e.id
        ORDER BY a.date DESC
    """)
    records = cur.fetchall()
    cur.close()

    # Create PDF
    output = BytesIO()
    p = canvas.Canvas(output)
    p.drawString(220, 800, "📅 Attendance Report")
    y = 770

    for record in records:
        text = f"ID: {record[0]} | Name: {record[1]} | Date: {record[2]} | In: {record[3]} | Out: {record[4]}"
        p.drawString(50, y, text)
        y -= 20
        if y < 40:
            p.showPage()
            y = 800

    p.save()
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='attendance_report.pdf',
        mimetype='application/pdf'
    )
