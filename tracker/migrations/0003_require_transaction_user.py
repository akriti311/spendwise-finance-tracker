# Remove orphan transactions, then require user on every row

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def delete_transactions_without_user(apps, schema_editor):
    Transaction = apps.get_model('tracker', 'Transaction')
    Transaction.objects.filter(user__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0002_transaction_user'),
    ]

    operations = [
        migrations.RunPython(
            delete_transactions_without_user,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transactions',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
