

# Admin - student list page
@app.route('/admin/students')
@admin_required
def admin_students():
    students = Student.query.all()
    return render_template('studentList.html', students=students)
