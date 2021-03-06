# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("lists", "0003_list")]

    operations = [
        migrations.AddField(
            model_name="item",
            name="list",
            field=models.ForeignKey(to="lists.List", default=None),
            preserve_default=True,
        )
    ]
