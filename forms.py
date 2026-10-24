from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, FloatField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username or Student ID', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class StudentRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    
    student_id = StringField('Student Roll / College ID', validators=[DataRequired(), Length(min=2, max=50)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    course = StringField('Course / Program', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    guardian_name = StringField('Guardian / Parent Name', validators=[Optional(), Length(max=100)])
    guardian_phone = StringField('Guardian Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Permanent Address', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Register Account')


class StudentProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    guardian_name = StringField('Guardian / Parent Name', validators=[Optional(), Length(max=100)])
    guardian_phone = StringField('Guardian Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Permanent Address', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Profile')


class AdminStudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password (leave blank to keep unchanged for existing student)', validators=[Optional(), Length(min=6, max=64)])
    student_id = StringField('Student Roll / College ID', validators=[DataRequired(), Length(min=2, max=50)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    course = StringField('Course / Program', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    guardian_name = StringField('Guardian / Parent Name', validators=[Optional(), Length(max=100)])
    guardian_phone = StringField('Guardian Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Permanent Address', validators=[Optional(), Length(max=500)])
    is_active = BooleanField('Active Account', default=True)
    submit = SubmitField('Save Student')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=64)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Change Password')


class RoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[DataRequired(), Length(min=1, max=30)])
    room_type = SelectField('Room Type', choices=[
        ('Single Bed', 'Single Bed'),
        ('Double Sharing', 'Double Sharing'),
        ('Triple Sharing', 'Triple Sharing'),
        ('Dormitory', 'Dormitory')
    ], validators=[DataRequired()])
    capacity = IntegerField('Capacity (Beds)', validators=[DataRequired(), NumberRange(min=1, max=20)])
    monthly_rent = FloatField('Monthly Rent (₹)', validators=[DataRequired(), NumberRange(min=0.0)])
    description = TextAreaField('Description / Facilities', validators=[Optional(), Length(max=255)])
    is_available = BooleanField('Available for Allocation', default=True)
    submit = SubmitField('Save Room')


class RoomRequestForm(FlaskForm):
    room_id = SelectField('Preferred Room (Optional)', coerce=int, validators=[Optional()])
    remarks = TextAreaField('Notes / Special Request', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Submit Room Request')


class RoomAllocationForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    room_id = SelectField('Room', coerce=int, validators=[DataRequired()])
    monthly_rent = FloatField('Agreed Monthly Rent (₹)', validators=[DataRequired(), NumberRange(min=0.0)])
    allocated_date = DateField('Allocation Date', default=date.today, validators=[DataRequired()])
    notes = TextAreaField('Allocation Notes', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Allocate Room')


class BillForm(FlaskForm):
    target = SelectField('Billing Target', choices=[('single', 'Specific Student'), ('all_allocated', 'All Allocated Students')], default='single')
    student_id = SelectField('Student', coerce=int, validators=[Optional()])
    fee_type = SelectField('Fee Type', choices=[
        ('Hostel Rent', 'Hostel Rent'),
        ('Mess Fee', 'Mess Fee'),
        ('Electricity & Utilities', 'Electricity & Utilities'),
        ('Maintenance Fee', 'Maintenance Fee'),
        ('Other Charges', 'Other Charges')
    ], validators=[DataRequired()])
    billing_period = StringField('Billing Period (e.g. October 2026)', validators=[DataRequired(), Length(min=3, max=40)])
    amount = FloatField('Amount (₹)', validators=[DataRequired(), NumberRange(min=1.0)])
    due_date = DateField('Due Date', default=date.today, validators=[DataRequired()])
    description = TextAreaField('Description / Notes', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Generate Bill')


class PaymentForm(FlaskForm):
    amount = FloatField('Payment Amount (₹)', validators=[DataRequired(), NumberRange(min=1.0)])
    payment_date = DateField('Payment Date', default=date.today, validators=[DataRequired()])
    payment_mode = SelectField('Payment Mode', choices=[
        ('Cash', 'Cash'),
        ('Bank Transfer / NEFT', 'Bank Transfer / NEFT'),
        ('UPI / QR Offline Receipt', 'UPI / QR Offline Receipt'),
        ('Cheque / DD', 'Cheque / DD')
    ], validators=[DataRequired()])
    reference_note = StringField('Receipt / Transaction Reference', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Record Payment')
