from marshmallow import Schema, fields, validate, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Syllabus, ClassSchedule


# -------------------------
# ClassSchedule Schemas
# -------------------------

class ClassScheduleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ClassSchedule
        load_instance = True
        include_fk = True


class ClassScheduleCreateSchema(Schema):
    order = fields.Integer(required=True, validate=validate.Range(min=1))
    class_hours = fields.Integer(required=True, validate=validate.Range(min=1))
    content = fields.String(required=True)


# -------------------------
# Syllabus Schemas
# -------------------------

class SyllabusSchema(SQLAlchemyAutoSchema):
    """読み取り専用（詳細表示）"""
    class_schedule = fields.Nested(ClassScheduleSchema, many=True)

    class Meta:
        model = Syllabus
        load_instance = True


class SyllabusCreateSchema(Schema):
    """作成・全更新用"""
    subject_name = fields.String(required=True)
    academic_subject_name = fields.String()

    instructor = fields.String()
    instructor_type = fields.String()

    teaching_method = fields.String()
    class_hours = fields.Integer()

    recommended_year = fields.String()
    course_classification = fields.String()

    academic_year = fields.Integer(required=True)
    semester = fields.String()

    eligible_departments = fields.List(fields.String(), missing=list)

    course_overview = fields.String()
    learning_objectives = fields.String()

    grading_prerequisites = fields.String()
    grading_criteria = fields.String()

    self_study_required = fields.String()
    textbook = fields.String()
    certification = fields.String()
    textbook_cost = fields.String()
    certification_cost = fields.String()
    notes = fields.String()
    remarks = fields.String()

    class_schedule = fields.List(
        fields.Nested(ClassScheduleCreateSchema),
        required=False
    )

    @validates("academic_year")
    def validate_academic_year(self, value):
        if value < 2000 or value > 2100:
            raise ValidationError("開講年度は2000〜2100の範囲で指定してください")


class SyllabusPartialUpdateSchema(Schema):
    """部分更新（PATCH）用：すべて任意"""
    subject_name = fields.String()
    academic_subject_name = fields.String()

    instructor = fields.String()
    instructor_type = fields.String()

    teaching_method = fields.String()
    class_hours = fields.Integer()

    recommended_year = fields.String()
    course_classification = fields.String()

    academic_year = fields.Integer()
    semester = fields.String()

    eligible_departments = fields.List(fields.String())

    course_overview = fields.String()
    learning_objectives = fields.String()

    grading_prerequisites = fields.String()
    grading_criteria = fields.String()

    self_study_required = fields.String()
    textbook = fields.String()
    certification = fields.String()
    textbook_cost = fields.String()
    certification_cost = fields.String()
    notes = fields.String()
    remarks = fields.String()