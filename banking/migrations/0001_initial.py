import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import banking.models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("account_number", models.CharField(default=banking.models.create_account_number, max_length=10, unique=True)),
                ("balance", models.DecimalField(decimal_places=2, default=10000.0, max_digits=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="account", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference", models.CharField(max_length=16, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("description", models.CharField(default="Demo fund transfer", max_length=120)),
                ("from_account", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="debits", to="banking.account")),
                ("to_account", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="credits", to="banking.account")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="transaction",
            constraint=models.CheckConstraint(condition=models.Q(("amount__gt", 0)), name="transaction_amount_positive"),
        ),
    ]
