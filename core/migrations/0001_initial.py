# Generated by Django 5.2 on 2025-04-08 17:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('permission_group', models.ManyToManyField(blank=True, related_name='category_permissions', to='auth.group', verbose_name='Grupos de Permisos')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('display_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre a Mostrar')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('permission_group', models.ManyToManyField(blank=True, related_name='issue_permissions', to='auth.group', verbose_name='Grupos de Permisos')),
                ('issue_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='core.issuecategory', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Incidencia',
                'verbose_name_plural': 'Incidencias',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('open', 'Abierto'), ('solved', 'Solucionado'), ('closed', 'Cerrado'), ('feedback', 'Comentado')], default='open', max_length=20, verbose_name='Estado')),
                ('reported_on', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Reportada')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Cuerpo del Mensaje')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Mensaje',
                'verbose_name_plural': 'Mensajes',
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/', verbose_name='Archivo')),
                ('filename', models.CharField(max_length=255, verbose_name='Nombre del Archivo')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='core.message', verbose_name='Mensaje')),
            ],
            options={
                'verbose_name': 'Adjunto',
                'verbose_name_plural': 'Adjuntos',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('groups', models.ManyToManyField(blank=True, related_name='sectors_groups', to='auth.group')),
                ('permission_group', models.ManyToManyField(blank=True, related_name='sector_permissions', to='auth.group', verbose_name='Grupos de Permisos')),
            ],
            options={
                'verbose_name': 'Sector',
                'verbose_name_plural': 'Sectores',
            },
        ),
        migrations.AddField(
            model_name='issuecategory',
            name='sector',
            field=models.ManyToManyField(related_name='issue_categories', to='core.sector', verbose_name='Sectores'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.issue', verbose_name='Incidencia')),
                ('issue_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.issuecategory', verbose_name='Categoría')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sector', verbose_name='Sector')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.ticket', verbose_name='Ticket'),
        ),
        migrations.CreateModel(
            name='UDN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('groups', models.ManyToManyField(blank=True, related_name='udns', to='auth.group')),
                ('permission_group', models.ManyToManyField(blank=True, related_name='udn_permissions', to='auth.group', verbose_name='Grupos de Permisos')),
            ],
            options={
                'verbose_name': 'UDN',
                'verbose_name_plural': 'UDNs',
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='udn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.udn', verbose_name='UDN'),
        ),
        migrations.AddField(
            model_name='sector',
            name='udn',
            field=models.ManyToManyField(related_name='sectors', to='core.udn', verbose_name='UDNs'),
        ),
    ]
