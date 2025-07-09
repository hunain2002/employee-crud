from flask import Blueprint, request, jsonify, current_app

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data.get('question', '').lower()

    cur = current_app.mysql.connection.cursor()

    if "present today" in question:
        cur.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance WHERE date = CURDATE()")
        result = cur.fetchone()[0]
        answer = f"{result} employees are present today."

    elif "total employees" in question:
        cur.execute("SELECT COUNT(*) FROM employee")
        result = cur.fetchone()[0]
        answer = f"There are {result} total employees."

    elif "male" in question and "female" in question:
        cur.execute("SELECT gender, COUNT(*) FROM employee GROUP BY gender")
        results = cur.fetchall()
        counts = {row[0].lower(): row[1] for row in results}
        male = counts.get("male", 0)
        female = counts.get("female", 0)
        answer = f"There are {male} male and {female} female employees."

    else:
        answer = "Sorry, I didn't understand the question."

    cur.close()
    return jsonify({"response": answer})
