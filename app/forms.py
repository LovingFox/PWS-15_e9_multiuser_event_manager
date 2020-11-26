import arrow
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea, HTMLString, html_params
from app.models import User
from app import app


class DateTimeWidget:
    """
    Виджет для раздельного заполнения даты и времени (html5)
    Для выбора даты будет возникать окошко выбора
    Для времени будут бегунки вверх-вниз (передвигаются стрелками на клавиатуре)
    """
    def __call__(self, field, **kwargs):
        id = kwargs.pop('id', field.id)
        date = time = ''
        if field.data:
            dt = arrow.get(field.data).to(app.config['TIMEZONE'])
            date = dt.format('YYYY-MM-DD')
            time = dt.format('HH:mm')
        date_params = html_params(name=field.name, id=id + '-date', value=date, **kwargs)
        time_params = html_params(name=field.name, id=id + '-time', value=time, **kwargs)
        return HTMLString('<input type="date" {}/><input type="time" {}/>'.format(date_params, time_params))


class MyDateTimeField(DateTimeField):
    """
    Модифицированный DateTimeField, что бы можно было применить виджет DateTimeWidget
    """
    widget = DateTimeWidget()

    def process_formdata(self, valuelist):
        app.logger.debug(valuelist)
        self.data = None
        self.data_raw = ()
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str:
                try:
                    self.data = arrow.get(date_str).replace(tzinfo=app.config['TIMEZONE']).to('UTC')
                    app.logger.debug(self.data)
                except arrow.parser.ParserError as e:
                    app.logger.warn('Invalid datetime value submitted: %s', e)
                    raise ValueError('Not a valid datetime value. Looking for YYYY-MM-DD HH:mm.')


class LoginForm(FlaskForm):
    '''
    Форма для входа в систему
    '''
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    '''
    Форма для регистрации нового пользователя
    '''
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), Length(max=128), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        '''
        Проверка, что имени пользователя нет в системе
        '''
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(f'Username "{username.data}" already exists.')

    def validate_email(self, email):
        '''
        Проверка, что email пользователя нет в системе
        '''
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(f'Username with email "{email.data}" already exists.')


class EventForm(FlaskForm):
    '''
    Форма ввода нового, изменения существующего или удаления текущего События
    '''
    title = StringField('Title', validators=[DataRequired(), Length(max=32)])
    body = StringField('Body', validators=[DataRequired(), Length(max=256)], widget=TextArea())
    start_dt = MyDateTimeField('Start DateTime', validators=[DataRequired()])
    end_dt = MyDateTimeField('End DateTime')
    submit = SubmitField('Submit')

    def validate_end_dt(self, end_dt):
        '''
        Валидируем разницу даты-времени
        Дата-время окончания должны быть больше начала
        '''
        if end_dt.data and self.start_dt.data and end_dt.data <= self.start_dt.data:
            raise ValidationError(f'{end_dt.data} le {self.start_dt.data}.')

    def disable_form(self, skip_submit=False):
        '''
        Гасим форму ввода
        Когда нужно только показать Событие
        Если есть skip_submit, то кнопку submit не гасить (нужно для функции удаления События)
        '''
        for name, field in self._fields.items():
            if not field.render_kw:
                field.render_kw = {}

            if name == 'submit' and skip_submit:
                continue

            field.render_kw['disabled'] = True


