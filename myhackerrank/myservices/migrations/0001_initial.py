# Generated by Django 2.0.3 on 2018-06-15 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(default=None, null=True)),
                ('status', models.CharField(max_length=20)),
                ('hash_str', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myservices.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.CharField(max_length=20)),
                ('problem_name', models.CharField(max_length=20)),
                ('problem_path', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_id', models.IntegerField()),
                ('result', models.CharField(max_length=20)),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myservices.Interview')),
                ('problem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myservices.Problem')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myservices.Candidate')),
            ],
        ),
        migrations.AddField(
            model_name='interview',
            name='problems',
            field=models.ManyToManyField(to='myservices.Problem'),
        ),
    ]