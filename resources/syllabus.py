from flask.views import MethodView
from flask_smorest import Blueprint, abort
from extensions import db
from models import Syllabus, ClassSchedule
from schemas import (
    SyllabusSchema,
    SyllabusCreateSchema,
    SyllabusPartialUpdateSchema,
)

blp = Blueprint("syllabi", __name__, url_prefix="/api/syllabi")


# -------------------------
# 一覧取得 / 作成
# -------------------------
@blp.route("/")
class SyllabusList(MethodView):

    @blp.response(200, SyllabusSchema(many=True))
    def get(self):
        """シラバス一覧取得"""
        return Syllabus.query.all()

    @blp.arguments(SyllabusCreateSchema)
    @blp.response(201, SyllabusSchema)
    def post(self, data):
        """シラバス作成"""
        class_schedule_data = data.pop("class_schedule", [])
        SyllabusDetail.validate_class_schedule_order(class_schedule_data)

        syllabus = Syllabus(**data)
        db.session.add(syllabus)
        db.session.commit()

        for schedule in class_schedule_data:
            cs = ClassSchedule(syllabus_id=syllabus.id, **schedule)
            db.session.add(cs)

        db.session.commit()
        return syllabus


# -------------------------
# 詳細取得 / 更新 / 削除
# -------------------------
@blp.route("/<int:syllabus_id>")
class SyllabusDetail(MethodView):

    @blp.response(200, SyllabusSchema)
    def get(self, syllabus_id):
        """シラバス詳細取得"""
        syllabus = Syllabus.query.get_or_404(syllabus_id)
        return syllabus

    @blp.arguments(SyllabusCreateSchema)
    @blp.response(200, SyllabusSchema)
    def put(self, data, syllabus_id):
        """シラバス全更新"""
        syllabus = Syllabus.query.get_or_404(syllabus_id)

        class_schedule_data = data.pop("class_schedule", None)

        # 本体更新
        for key, value in data.items():
            setattr(syllabus, key, value)

        # class_schedule が指定されている場合は全削除 → 再作成
        if class_schedule_data is not None:
            SyllabusDetail.validate_class_schedule_order(class_schedule_data)
            ClassSchedule.query.filter_by(syllabus_id=syllabus.id).delete()
            for schedule in class_schedule_data:
                cs = ClassSchedule(syllabus_id=syllabus.id, **schedule)
                db.session.add(cs)

        db.session.commit()
        return syllabus

    @blp.arguments(SyllabusPartialUpdateSchema)
    @blp.response(200, SyllabusSchema)
    def patch(self, data, syllabus_id):
        """シラバス部分更新"""
        syllabus = Syllabus.query.get_or_404(syllabus_id)

        for key, value in data.items():
            setattr(syllabus, key, value)

        db.session.commit()
        return syllabus

    @blp.response(204)
    def delete(self, syllabus_id):
        """シラバス削除"""
        syllabus = Syllabus.query.get_or_404(syllabus_id)
        db.session.delete(syllabus)
        db.session.commit()
        return ""
    
    # -------------------------
    # class_schedule の order 重複チェック（PUT / POST 共通）
    # -------------------------
    @staticmethod
    def validate_class_schedule_order(class_schedule_data):
        orders = [item["order"] for item in class_schedule_data]
        if len(orders) != len(set(orders)):
            abort(400, message="class_schedule の order が重複しています。")
