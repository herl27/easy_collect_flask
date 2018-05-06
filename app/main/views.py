from app.main import main
from app.main.forms import TeacherForm, NewTeacherForm, TeacherChangeRequestForm
from app import db
from app.models import Teacher
from app.excel import write2excel
from flask import render_template, flash, redirect, url_for, abort, session, g
from datetime import datetime
from markupsafe import Markup

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/add', methods=['GET', 'POST'])
def add():
    form = NewTeacherForm()
    if form.validate_on_submit():
        teacher = Teacher(
                name = form.name.data,
                id_card = form.id_card.data,
                race = form.race.data,
                origin = form.origin.data,
                tel = form.tel.data,
                course = form.course.data,
                is_header_teacher = form.is_header_teacher.data,
                working_date = form.working_date.data,
                create_time = datetime.now(), 
                change_time = datetime.now())
        db.session.add(teacher)
        db.session.commit()
        flash('资料保存完毕','success')
        return redirect(url_for('main.view', id=teacher.id))
    try:
        form.name.data = session.pop('name')
    except KeyError:
        pass
    return render_template('form.html', form=form, form_header='新建')

@main.route('/view/<int:id>')
def view(id):
    current_teacher = Teacher.query.get_or_404(id)
    return render_template('view.html', teacher=current_teacher)

@main.route('/change', methods=['GET', 'POST'])
def change_request():
    form = TeacherChangeRequestForm()   
    if form.validate_on_submit():
        query_data = Teacher.query.filter_by(name=form.name.data) 
        num = query_data.count()
        if num == 1:
            id = query_data.first().id
            return redirect(url_for('main.view', id=id))
        if num > 1:
            table = [('#', '姓名', '出生日期', '任教科目', '操作')]   
            i = 1
            for data in query_data:
                name = data.name
                birthday = data.birthday.strftime('%Y年%m月')
                course = data.course
                action = Markup('<a href="'\
                    + url_for('main.change', id=data.id)\
                    + '">修改</a>')
                table.append((i, name, birthday, course, action))
                i += 1
            g.table = table
            return render_template('table.html', table_title='请选择要修改的数据')
        if num == 0:
            session['name'] = form.name.data
            flash(Markup('没有查询到您的信息，<a href="'
                +url_for('main.add')+'">点击此处</a>新建'), 'warning')
    return render_template('form.html', form=form, form_header='请输入姓名')

@main.route('/change/<int:id>', methods=['GET', 'POST'])
def change(id):
    current_teacher = Teacher.query.get_or_404(id)
    form = TeacherForm()
    if form.validate_on_submit():
        current_teacher.name = form.name.data
        current_teacher.id_card = form.id_card.data
        current_teacher.race = form.race.data
        current_teacher.origin = form.origin.data
        current_teacher.tel = form.tel.data
        current_teacher.course = form.course.data
        current_teacher.is_header_teacher = form.is_header_teacher.data
        current_teacher.working_date = form.working_date.data
        current_teacher.change_time = datetime.now()
        db.session.add(current_teacher)
        db.session.commit()
        flash('您的资料已经更新', 'success')
        return redirect(url_for('main.view',id=id))
    form.name.data = current_teacher.name
    form.id_card.data = current_teacher.id_card
    form.race.data = current_teacher.race
    form.origin.data = current_teacher.origin
    form.tel.data = current_teacher.tel
    form.course.data = current_teacher.course
    form.is_header_teacher.data = current_teacher.is_header_teacher
    form.working_date.data = current_teacher.working_date
    return render_template('form.html', form=form, form_header='修改资料')

@main.route('/del/<int:id>')
def delete(id):
    current_teacher = Teacher.query.get_or_404(id)
    name = current_teacher.name
    db.session.delete(current_teacher)
    db.session.commit()
    flash('{}的填报资料已经删除'.format(name),'danger')
    return redirect(url_for('main.index'))

@main.route('/all')
def all():
    table = [('#', '姓名', '性别', '出生日期', '民族', '身份证号',
        '籍贯','电话号码','任教科目', '班主任', '填写时间', '操作')]   
    i = 1
    for data in Teacher.query.all():
        name = data.name
        sex = data.sex
        birthday = data.birthday.strftime('%Y-%m-%d')
        race = data.race
        id_card = data.id_card
        origin = data.origin
        tel = data.tel
        course = data.course
        is_header_teacher = "是" if data.is_header_teacher else "否"
        change_time = data.change_time.strftime('%m-%d %H:%M')
        action = Markup('<a href="'\
            + url_for('main.change', id=data.id)\
            + '">修改</a>'+' | '+'<a style=\'color:red\' href="'\
            + url_for('main.delete', id=data.id)\
            + '">删除</a>')
        table.append((i, name, sex, birthday, race, id_card,
            origin, tel, course, is_header_teacher, change_time, action))
        i += 1
    g.table = table
    session['table'] = table
    return render_template('table.html', table_title='全部资料')

@main.route('/out')
def out():
    table = session.get('table')
    if table is None:
        return redirect(url_for('main.all'))
    data = (row[:-2] for row in table)
    name = '导出'
    filename = write2excel(name, data)
    return redirect(url_for('static', filename=filename, _external=True))
