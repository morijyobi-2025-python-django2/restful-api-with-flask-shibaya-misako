from datetime import datetime
from extensions import db


class ClassSchedule(db.Model):
    __tablename__ = "class_schedules"

    id = db.Column(db.Integer, primary_key=True)
    syllabus_id = db.Column(db.Integer, db.ForeignKey("syllabi.id"), nullable=False)

    order = db.Column(db.Integer, nullable=False)
    class_hours = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    syllabus = db.relationship("Syllabus", back_populates="class_schedule")


class Syllabus(db.Model):
    __tablename__ = "syllabi"

    id = db.Column(db.Integer, primary_key=True)

    # 基本情報
    subject_name = db.Column(db.String(255), nullable=False)
    academic_subject_name = db.Column(db.String(255))

    # 教員情報
    instructor = db.Column(db.String(100))
    instructor_type = db.Column(db.String(20))

    # 授業形態
    teaching_method = db.Column(db.String(20))
    class_hours = db.Column(db.Integer)

    # 履修情報
    recommended_year = db.Column(db.String(50))
    course_classification = db.Column(db.String(20))

    # 開講情報
    academic_year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10))

    # JSONField
    eligible_departments = db.Column(db.JSON, default=list)

    # 授業内容
    course_overview = db.Column(db.Text)
    learning_objectives = db.Column(db.Text)

    # 評価基準
    grading_prerequisites = db.Column(db.Text)
    grading_criteria = db.Column(db.Text)

    # その他
    self_study_required = db.Column(db.Text)
    textbook = db.Column(db.Text)
    certification = db.Column(db.Text)
    textbook_cost = db.Column(db.String(100))
    certification_cost = db.Column(db.String(100))
    notes = db.Column(db.Text)
    remarks = db.Column(db.Text)

    # 管理用フィールド
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーション（1:N）
    class_schedule = db.relationship(
        "ClassSchedule",
        back_populates="syllabus",
        cascade="all, delete-orphan"
    )