from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        student_name = request.form["student_name"]
        student_level = request.form["student_level"]
        current_session = request.form["current_session"]

        course_titles = request.form.getlist("course_title")
        course_units = request.form.getlist("course_unit")
        course_scores = request.form.getlist("course_score")

        total_unit_registered = 0
        accumulative_total_unit_passed = 0
        results = []

        for title, unit, score in zip(course_titles, course_units, course_scores):
            unit = int(unit)
            score = float(score)
            total_unit_registered += unit

            if 0 <= score <= 44:
                grade_point = 0
            elif 45 <= score <= 49:
                grade_point = 1
            elif 50 <= score <= 59:
                grade_point = 2
            elif 60 <= score <= 69:
                grade_point = 3
            elif 70 <= score <= 100:
                grade_point = 4
            else:
                grade_point = 0  # Default for invalid

            total_passed = unit * grade_point
            accumulative_total_unit_passed += total_passed

            results.append({
                "title": title,
                "unit": unit,
                "score": score,
                "grade_point": grade_point,
                "total_passed": total_passed
            })

        cgpa = accumulative_total_unit_passed / total_unit_registered if total_unit_registered else 0

        # Classification
        if cgpa < 1.00:
            remark = "Oppps, You Failed."
        elif 1.00 <= cgpa <= 1.99:
            remark = "Congratulations! You are a Third Class Student."
        elif 2.00 <= cgpa <= 2.99:
            remark = "Congratulations! You are a Second Class Lower Division student."
        elif 3.00 <= cgpa <= 3.49:
            remark = "Congratulations! You are a Second Class Upper Division student."
        elif 3.50 <= cgpa <= 4.00:
            remark = "Congratulations! You are a FIRST-CLASS student."
        else:
            remark = "Invalid CGPA"

        return render_template("result.html",
                               name=student_name,
                               level=student_level,
                               session=current_session,
                               results=results,
                               total_unit=total_unit_registered,
                               total_passed=accumulative_total_unit_passed,
                               cgpa=round(cgpa, 2),
                               remark=remark)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

