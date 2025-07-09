from flask import Blueprint, send_file, current_app
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/export/employees/xlsx')
def export_employees_xlsx():
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT id, name, username, email, city FROM employee")
    employees = cur.fetchall()
    cur.close()

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

    output = BytesIO()
    p = canvas.Canvas(output, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 40, "📅 Attendance Report")
    y = height - 70

    p.setFont("Helvetica", 10)
    for record in records:
        line = f"ID: {record[0]} | Name: {record[1]} | Date: {record[2]} | Sign In: {record[3]} | Sign Out: {record[4]}"
        p.drawString(40, y, line)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='attendance_report.pdf',
        mimetype='application/pdf'
    )


@reports_bp.route('/export/employee_cards/pdf')
def export_employee_cards_pdf():
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT id, name, username, photo FROM employee")
    employees = cur.fetchall()
    cur.close()

    output = BytesIO()
    p = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    x = 40
    y = height - 100

    for emp in employees:
        emp_id, name, username, photo_filename = emp
        qr_filename = f"{emp_id}.png"
        qr_path = os.path.join("static", "qr_codes", qr_filename)
        photo_path = os.path.join("static", "uploads", photo_filename)

        # Card Border
        p.setStrokeColorRGB(0.2, 0.2, 0.2)
        p.rect(x - 10, y - 85, 500, 100, stroke=1, fill=0)

        p.setFont("Helvetica-Bold", 12)
        p.drawString(x, y, f"Name: {name}")
        p.drawString(x, y - 20, f"Username: {username}")

        if os.path.exists(photo_path):
            try:
                p.drawImage(photo_path, x + 300, y - 10, width=60, height=60, preserveAspectRatio=True)
            except:
                pass

        if os.path.exists(qr_path):
            try:
                p.drawImage(qr_path, x + 380, y - 10, width=60, height=60, preserveAspectRatio=True)
            except:
                pass

        y -= 130
        if y < 100:
            p.showPage()
            y = height - 100

    p.save()
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='employee_cards.pdf',
        mimetype='application/pdf'
    )


@reports_bp.route('/employee_card/<int:emp_id>')
def single_employee_card(emp_id):
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT id, name, username, photo FROM employee WHERE id = %s", (emp_id,))
    emp = cur.fetchone()
    cur.close()

    if not emp:
        return "Employee not found", 404

    output = BytesIO()
    c = canvas.Canvas(output, pagesize=A4)

    card_width = 260
    card_height = 130
    x = 150
    y = 500

    emp_id, name, username, photo_filename = emp
    qr_filename = f"{emp_id}.png"
    qr_path = os.path.join("static", "qr_codes", qr_filename)
    photo_path = os.path.join("static", "uploads", photo_filename)

    c.setStrokeColorRGB(0.3, 0.3, 0.3)
    c.rect(x, y, card_width, card_height, stroke=1, fill=0)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 15, y + card_height - 25, f"Name: {name}")
    c.setFont("Helvetica", 10)
    c.drawString(x + 15, y + card_height - 45, f"Username: {username}")

    if os.path.exists(photo_path):
        try:
            c.drawImage(photo_path, x + 15, y + 20, width=60, height=60, preserveAspectRatio=True)
        except:
            pass

    if os.path.exists(qr_path):
        try:
            c.drawImage(qr_path, x + card_width - 75, y + 20, width=60, height=60, preserveAspectRatio=True)
        except:
            pass

    c.save()
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=f'employee_card_{emp_id}.pdf',
        mimetype='application/pdf'
    )
