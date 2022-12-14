# Generated by Django 4.0.2 on 2022-11-03 10:25

import django.contrib.auth.models
import django.contrib.auth.validators
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
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField()),
                ('data', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Подразделение')),
                ('ids', models.CharField(default='', max_length=70, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделение',
            },
        ),
        migrations.CreateModel(
            name='InfTech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=70, unique=True, verbose_name='Ф.И.О')),
                ('department', models.CharField(default='АЙТи отдел', max_length=250, verbose_name='Подразделение')),
                ('job', models.CharField(max_length=70, verbose_name='Должность')),
                ('is_boss', models.BooleanField(default=False, verbose_name='Начальник отдела')),
                ('phone', models.CharField(max_length=70, verbose_name='Телефон номер')),
                ('active', models.BooleanField(default=True, verbose_name='Статус')),
                ('telegram_id', models.BigIntegerField(blank=True, null=True, verbose_name='Telegram ID')),
            ],
            options={
                'verbose_name': 'АЙТишник',
                'verbose_name_plural': 'АЙТишники',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('text', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=70, unique=True, verbose_name='Ф.И.О')),
                ('job', models.CharField(max_length=70, verbose_name='Должность')),
                ('is_boss', models.BooleanField(default=False, verbose_name='Начальник отдела')),
                ('phone', models.CharField(max_length=70, verbose_name='Телефон номер')),
                ('active', models.BooleanField(default=True, verbose_name='Статус')),
                ('telegram_id', models.BigIntegerField(blank=True, null=True, verbose_name='Telegram ID')),
                ('boss', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='staff.workers', verbose_name='Главный')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.department', verbose_name='Подразделение')),
            ],
            options={
                'verbose_name': 'Сотрудники',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Total',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=10, verbose_name='Год')),
                ('month', models.CharField(choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], max_length=100, verbose_name='Месяц')),
                ('full_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.workers', verbose_name='Ф.И.О')),
            ],
            options={
                'verbose_name': 'Итого',
                'verbose_name_plural': 'Итого',
            },
        ),
        migrations.CreateModel(
            name='Salarys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(default=2022, max_length=10, verbose_name='Год')),
                ('month', models.CharField(choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], max_length=100, verbose_name='Месяц')),
                ('salary', models.IntegerField(verbose_name='Оклад')),
                ('full_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.workers', verbose_name='Ф.И.О')),
            ],
            options={
                'verbose_name': 'Зарплаты',
                'verbose_name_plural': 'Зарплаты',
            },
        ),
        migrations.CreateModel(
            name='Request_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_id', models.CharField(max_length=70)),
                ('month', models.CharField(blank=True, choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], max_length=250, null=True, verbose_name='Месяц')),
                ('price', models.BigIntegerField(verbose_name='Цена')),
                ('avans', models.BooleanField(verbose_name='Аванс')),
                ('comment', models.CharField(blank=True, default='', max_length=2560, null=True)),
                ('answer', models.BooleanField(default=False, verbose_name='Ответил')),
                ('status', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('workers', models.ManyToManyField(to='staff.Total')),
            ],
            options={
                'verbose_name': 'Зарплаты/аванс запрос',
                'verbose_name_plural': 'Зарплаты/aванс запрос',
            },
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('month', models.CharField(choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], max_length=100, verbose_name='Месяц')),
                ('year', models.CharField(default=2022, max_length=10, verbose_name='Год')),
                ('fine', models.IntegerField(default=0, verbose_name='Выплачено')),
                ('full_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.workers', verbose_name='Ф.И.О')),
            ],
            options={
                'verbose_name': 'Выплаты',
                'verbose_name_plural': 'Выплаты',
            },
        ),
        migrations.CreateModel(
            name='ITRequestPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secondId', models.IntegerField(blank=True, null=True, verbose_name='Запрос ИД')),
                ('department_id', models.CharField(max_length=70)),
                ('month', models.CharField(blank=True, choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], max_length=250, null=True)),
                ('price', models.BigIntegerField()),
                ('avans', models.BooleanField()),
                ('comment', models.CharField(default='', max_length=2560)),
                ('answer', models.BooleanField(default=False)),
                ('status', models.CharField(default='', max_length=256)),
                ('workers', models.ManyToManyField(to='staff.InfTech')),
            ],
            options={
                'verbose_name': 'АЙТи отдел Зарплаты/аванс запрос',
                'verbose_name_plural': 'АЙТи отдел Зарплаты/aванс запрос',
            },
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='Удален')),
                ('month', models.CharField(choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], max_length=100, verbose_name='Месяц')),
                ('year', models.CharField(default=2022, max_length=10, verbose_name='Год')),
                ('bonus', models.IntegerField(default=0, verbose_name='Бонус')),
                ('paid', models.IntegerField(default=0, verbose_name='Штраф')),
                ('is_deleted', models.BooleanField(default=False)),
                ('full_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.workers', verbose_name='Ф.И.О')),
            ],
            options={
                'verbose_name': 'Бонус и шртаф',
                'verbose_name_plural': 'Бонус и шртаф',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telegram_id', models.BigIntegerField(blank=True, null=True, verbose_name='Телеграм ID')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('partner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.department', verbose_name='Подразделение')),
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
    ]
