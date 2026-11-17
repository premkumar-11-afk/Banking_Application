# SecureBank – Manual Test Plan

## 1. Objective
Validate the core customer journeys of the simulated SecureBank application: registration, login, dashboard, balance enquiry, fund transfer, transaction history and logout.

## 2. Scope
In scope: functional, positive, negative, UI, validation, integration, basic security checks and regression testing.
Out of scope: real banking rails, payment gateways, OTP/SMS, KYC, production penetration testing and real financial transactions.

## 3. Test environment
- Browser: latest Chrome / Firefox
- OS: Windows 10/11 or macOS
- App: local Django development server
- Database: SQLite
- Test data: synthetic users and demo balances only

## 4. Entry criteria
- App starts successfully.
- Database migrations completed.
- Two demo users can be registered.
- Tester has this test plan and test data.

## 5. Exit criteria
- All critical test cases executed.
- No open Critical/High defects for core flows.
- Failed tests have linked defect reports.
- Regression tests rerun after fixes.

## 6. Test cases

| TC ID | Module | Scenario | Test data / steps | Expected result | Priority |
|---|---|---|---|---|---|
| SB-REG-001 | Registration | Register with valid details | Unique username, valid email, matching strong passwords | Account created; dashboard opens | High |
| SB-REG-002 | Registration | Duplicate username | Register using an existing username | Validation error; no duplicate user | High |
| SB-REG-003 | Registration | Password mismatch | Enter different password values | Validation error; account not created | High |
| SB-REG-004 | Registration | Invalid email | Enter malformed email | Email validation shown | Medium |
| SB-LOG-001 | Login | Valid login | Correct username and password | User reaches dashboard | High |
| SB-LOG-002 | Login | Invalid password | Correct username, wrong password | Error shown; user remains logged out | High |
| SB-LOG-003 | Login | Protected page without login | Open /dashboard/ in logged-out browser | Redirected to login | High |
| SB-DASH-001 | Dashboard | View account balance | Login with a demo user | Correct balance and account number displayed | High |
| SB-TRF-001 | Transfer | Valid transfer | Recipient account exists; amount 100.00 | Sender debited and recipient credited by 100.00 | Critical |
| SB-TRF-002 | Transfer | Insufficient balance | Balance 1000.00; transfer 5000.00 | Transfer rejected; balances unchanged | Critical |
| SB-TRF-003 | Transfer | Unknown recipient | Use non-existing account number | Validation error; no transaction created | High |
| SB-TRF-004 | Transfer | Transfer to own account | Enter own account number | Transfer rejected | High |
| SB-TRF-005 | Transfer | Zero amount | Enter 0.00 | Validation error; no transaction created | High |
| SB-TRF-006 | Transfer | Negative amount | Enter -10.00 | Validation error; no transaction created | Critical |
| SB-TRF-007 | Transfer | Amount with 3 decimal places | Enter 10.123 | Validation error | Medium |
| SB-TRF-008 | Transfer | Blank recipient | Leave recipient blank | Required-field validation shown | Medium |
| SB-HIS-001 | History | View debit record | Complete a transfer as sender | Debit appears with correct amount and reference | High |
| SB-HIS-002 | History | View credit record | Receive a transfer | Credit appears with correct amount and sender | High |
| SB-OUT-001 | Logout | Logout from application | Click Logout | Session ends; protected page redirects to login | High |
| SB-SEC-001 | Security | CSRF check | Submit transfer without CSRF token | Request rejected | High |
| SB-UI-001 | UI | Responsive layout | Open pages at desktop and mobile widths | Content remains readable and usable | Medium |

## 7. Important test data
- Sender: `qa_sender` (register through UI)
- Recipient: `qa_receiver` (register through a separate browser)
- Initial demo balance: ₹10,000.00 per newly registered account
- Valid test amount: ₹100.00
- Insufficient-balance test: ₹50,000.00

## 8. Execution result template
Record each test as Pass / Fail / Blocked / Not Run. Add actual result, tester, date, browser and defect ID. Do not mark a case Pass without executing it.

## 9. Regression checklist
After a fix, retest login, dashboard, valid transfer, insufficient balance, self-transfer, transaction history and logout.

## 10. Important QA note
A test plan is not evidence that tests passed. Execute the cases against the running app and record actual results honestly.
