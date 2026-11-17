import secrets
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, TransferForm
from .models import Account, Transaction

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Account.objects.create(user=user, balance=Decimal("10000.00"))
            login(request, user)
            messages.success(request, "Your demo account has been created.")
            return redirect("dashboard")
    else:
        form = RegistrationForm()
    return render(request, "banking/register.html", {"form": form})

@login_required
def dashboard(request):
    account = request.user.account
    recent = Transaction.objects.filter(
        Q(from_account=account) | Q(to_account=account)
    )[:5]
    return render(request, "banking/dashboard.html", {"account": account, "recent": recent})

@login_required
def transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_id = request.user.account.id
            recipient_number = form.cleaned_data["recipient_account"]
            amount = form.cleaned_data["amount"].quantize(Decimal("0.01"))
            if amount <= 0:
                form.add_error("amount", "Transfer amount must be greater than zero.")
            else:
                try:
                    with transaction.atomic():
                        sender = Account.objects.select_for_update().get(pk=sender_id)
                        recipient = Account.objects.select_for_update().get(account_number=recipient_number)
                        if sender.pk == recipient.pk:
                            form.add_error("recipient_account", "You cannot transfer money to your own account.")
                        elif sender.balance < amount:
                            form.add_error("amount", "Insufficient balance.")
                        else:
                            sender.balance -= amount
                            recipient.balance += amount
                            sender.save(update_fields=["balance"])
                            recipient.save(update_fields=["balance"])
                            Transaction.objects.create(
                                reference=secrets.token_hex(8).upper(),
                                from_account=sender,
                                to_account=recipient,
                                amount=amount,
                                description=form.cleaned_data.get("description") or "Demo fund transfer",
                            )
                    if not form.errors:
                        messages.success(request, "Demo transfer completed successfully.")
                        return redirect("transactions")
                except Account.DoesNotExist:
                    form.add_error("recipient_account", "Recipient account was not found.")
    else:
        form = TransferForm()
    return render(request, "banking/transfer.html", {"form": form})

@login_required
def transactions(request):
    account = request.user.account
    rows = Transaction.objects.filter(
        Q(from_account=account) | Q(to_account=account)
    ).select_related("from_account__user", "to_account__user")
    return render(request, "banking/transactions.html", {"transactions": rows, "account": account})

@require_POST
@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("login")
