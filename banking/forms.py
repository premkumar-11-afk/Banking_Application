from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from decimal import Decimal

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class TransferForm(forms.Form):
    recipient_account = forms.CharField(max_length=10, label="Recipient account number")
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
    )
    description = forms.CharField(max_length=120, required=False)

    def clean_recipient_account(self):
        value = self.cleaned_data["recipient_account"].strip().upper()
        if not value.startswith("SB") or len(value) != 10:
            raise forms.ValidationError("Enter a valid 10-character demo account number.")
        return value

# Add Bootstrap classes to generated form controls.
for _form_class in (RegistrationForm, TransferForm):
    for _field in _form_class.base_fields.values():
        _field.widget.attrs.setdefault("class", "form-control")
