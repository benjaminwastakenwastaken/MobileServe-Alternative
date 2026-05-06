from app import app, db
from app.models import Student, Request
from datetime import datetime

with app.app_context():
    s = Student.query.first()
    print('Student:', s)

    r = Request(
        student_id=s.id,
        hours=3,
        details='Test service',
        direct=True,
        organization='Test Org',
        service_date=datetime.now()
    )
    db.session.add(r)
    db.session.commit()
    print('Added request:', r)
