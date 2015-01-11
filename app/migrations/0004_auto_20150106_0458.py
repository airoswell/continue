# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150106_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='availability',
            field=models.CharField(default=b'In use', max_length=20, choices=[(b'Available', b'Available'), (b'In use', b'In use'), (b'Lent', b'Lent'), (b'Given away', b'Given away'), (b'Disposed', b'Disposed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='visibility',
            field=models.CharField(default=b'Private', max_length=2, choices=[(b'Private', b'Private'), (b'Ex-owners', b'Ex-owners'), (b'Public', b'Public')]),
            preserve_default=True,
        ),
    ]
