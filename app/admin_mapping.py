from flask_admin.contrib.sqla import ModelView

from app.database import db
from app.user.models import User
from app.report.models import Report
from app.extensions import admin

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Report, db.session))
