from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Regexp
from wtforms import ValidationError
from app.models import Teacher
from markupsafe import Markup

class TeacherForm(FlaskForm):
    name = StringField('姓名', validators=[Required()])
    id_card = StringField('身份证号', validators=[Required(),
        Regexp('^[1-9][0-9]{16}[0-9X]$', 0, '请输入正确身份证号，X大写')])
    race = StringField('民族', validators=[Required()])
    origin = StringField('籍贯', validators=[Required()])
    tel = StringField('手机号', validators=[Required(),
        Regexp('^1[35678][0-9]{9}$', 0, '请输入正确的手机号')])
    course = StringField('任教学科', validators=[Required()])
    is_header_teacher = SelectField('班主任', coerce=int,
            choices=[(0, "否"), (1, "是")])
    working_date = DateField('工作日期', 
            format='%Y-%m-%d', validators=[Required()])
    submit = SubmitField('保存')

class NewTeacherForm(TeacherForm):
    def validate_id_card(self, field):
        existed = Teacher.query.filter_by(id_card=field.data).first()
        if existed:
            raise ValidationError(
                    Markup('身份证已存在，查看/修改信息<a href="'
                        + url_for('main.view', id=existed.id)
                        + '">单击此处</a>'))

class TeacherChangeRequestForm(FlaskForm):
    name = StringField('姓名', validators=[Required()])
    submit = SubmitField('查看')
