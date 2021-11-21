# Generated by Django 3.2.7 on 2021-11-21 09:26

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_principal', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=2000)),
                ('term', models.CharField(choices=[('Term one Jan- April', ' Term one Jan- April'), ('Term two May- August', 'Term two May- August'), ('Term three September- December', 'Term three September- December')], max_length=2000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('year', 'term')},
            },
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Form One', 'Form One'), ('Form Two', 'Form Two'), ('Form Three', 'Form Three'), ('Form Four ', 'Form Four')], max_length=1000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.academicyear')),
            ],
        ),
        migrations.CreateModel(
            name='Principal',
            fields=[
                ('profile_photo', models.ImageField(upload_to='Profiles/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='school.user')),
                ('staff_number', models.CharField(max_length=2000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='school.user')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='Profiles/')),
                ('staff_number', models.CharField(max_length=2000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('English', 'English'), ('Mathematics', 'Mathematics'), ('Kiswahili', 'Kiswahili'), ('Chemistry', 'Chemistry'), ('Physics', 'Physics'), ('Biology', 'Biology'), ('Geography', 'Geography'), ('History', 'History'), ('C.R.E', 'C.R.E'), ('Agriculture', 'Agriculture'), ('Business Studies', 'Business Studies')], max_length=2000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='school.classes')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher')),
            ],
            options={
                'unique_together': {('name', 'classes')},
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='school.user')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='Profiles/')),
                ('reg_number', models.CharField(max_length=2000)),
                ('hse', models.CharField(max_length=2000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('classes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.classes')),
                ('subjects', models.ManyToManyField(related_name='students', to='school.Subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam1', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)])),
                ('exam2', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)])),
                ('teacher', models.CharField(max_length=300)),
                ('endterm', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(70), django.core.validators.MinValueValidator(0)])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.classes')),
                ('subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='school.subjects')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_results', to='school.student')),
            ],
            options={
                'unique_together': {('student', 'subjects')},
            },
        ),
        migrations.CreateModel(
            name='Fees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_payable', models.FloatField()),
                ('amount_paid', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
        ),
        migrations.AddField(
            model_name='classes',
            name='class_teacher',
            field=models.ForeignKey(on_delete=models.SET('NoNe'), to='school.teacher'),
        ),
        migrations.CreateModel(
            name='subjectInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(blank=True, null=True)),
                ('mean_marks', models.IntegerField(blank=True, null=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.subjects')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
            options={
                'unique_together': {('student', 'subject')},
            },
        ),
        migrations.CreateModel(
            name='report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('p_comments', models.CharField(blank=True, max_length=100, null=True)),
                ('t_comments', models.CharField(blank=True, max_length=100, null=True)),
                ('total_marks', models.FloatField(blank=True, null=True)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('s_mean_marks', models.IntegerField(blank=True, null=True)),
                ('all_points', models.FloatField(blank=True, null=True)),
                ('all_subjects', models.ManyToManyField(to='school.Results')),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_report', to='school.classes')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_report', to='school.student')),
            ],
            options={
                'unique_together': {('classes', 'student')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='classes',
            unique_together={('name', 'year')},
        ),
    ]
