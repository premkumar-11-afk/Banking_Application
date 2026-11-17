# SecureBank – Manual Testing Practice Project

A simulated online banking web application built with Python, Django, SQLite/PostgreSQL, HTML, CSS and Bootstrap. It is designed for learning development and manual QA. **It is not a real banking product and must never be used to store or transfer real money.**

## Features
- Customer registration and login
- Demo account creation with an initial balance of ₹10,000
- Dashboard and balance enquiry
- Demo account-to-account transfer
- Transaction history
- Server-side validation and CSRF protection
- Automated Django tests for key transfer scenarios

## Requirements
- Python 3.10+
- Git
- A terminal / command prompt

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```
Open http://127.0.0.1:8000/

For macOS/Linux, activate with `source .venv/bin/activate` and run commands with `python`.

## Manual demo flow
1. Register two separate users in two browser sessions (or use separate browsers).
2. Copy the recipient's account number from their dashboard.
3. Log in as the sender and open Transfer funds.
4. Enter recipient account number and amount.
5. Confirm sender debit, recipient credit and transaction history.

## Run automated tests
```bash
python manage.py test
```

## Useful commands
```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## GitHub upload
Create a new empty GitHub repository named `securebank-manual-testing`. In this project folder:
```bash
git init
git add .
git commit -m "Build SecureBank demo banking app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/securebank-manual-testing.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. Never commit `.env`, passwords, secret keys or real customer data.

## Deployment on Render
1. Push the project to GitHub.
2. Create a PostgreSQL database on Render.
3. Create a new Web Service connected to the repository.
4. Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
5. Start command: `gunicorn securebank.wsgi:application`
6. Set environment variables:
   - `DJANGO_SECRET_KEY`: generate a long random secret
   - `DJANGO_DEBUG`: `False`
   - `DJANGO_ALLOWED_HOSTS`: your Render hostname, e.g. `your-app.onrender.com`
   - `DATABASE_URL`: Render PostgreSQL internal connection string
7. Deploy and test registration, login, transfer and transaction history.

For a production-grade application, additional security, audit logging, monitoring, security review and payment-provider integration would be required. This training project is intentionally not production-ready.

## Suggested repository contents
- `banking/`: models, forms, views, urls and tests
- `templates/`: Django HTML templates
- `securebank/`: project configuration
- `README.md`: setup and deployment instructions
- `MANUAL_TEST_PLAN.md`: QA plan and test cases
- `BUG_REPORT_TEMPLATE.md`: defect reporting template
