# 🚀 Quick Start Guide - Aashray Platform

## Get Started in 3 Steps

### Step 1: Create Admin Account
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### Step 2: Start Server
```bash
python manage.py runserver
```

### Step 3: Open Browser
Navigate to: **http://127.0.0.1:8000/**

---

## First Time Setup

### Create Your First Volunteer Account
1. Click "Register as a Volunteer"
2. Fill in your details
3. Login automatically redirects to Volunteer Home

### Appoint Team Members (Admin Only)
1. Login as superuser
2. Go to Admin Dashboard
3. Find a volunteer in the list
4. Click "Appoint to Team"

### Report Your First Case
1. Login as any user
2. Click "Report Case"
3. Fill in case details:
   - Case Type (e.g., "Food Shortage")
   - Location
   - Description of needs
   - Priority level
   - Upload image (optional)
4. Submit

---

## User Roles & Access

| Role | Login Redirect | Can Do |
|------|---------------|---------|
| **Volunteer** | `/volunteer/home/` | Report cases, view case board |
| **Team** | `/team/dashboard/` | Validate cases, update status, manage cases |
| **Admin** | `/admin/dashboard/` | Everything + appoint team members |

---

## Common Tasks

### View All Cases
- Navigate to "View Cases" in navigation
- Filter by status or priority
- Click on cases to see details

### Update Case Status (Team/Admin)
1. Go to Team Dashboard or Case Board
2. Find the case
3. Select new status from dropdown
4. Click "Update"

### Manage Users (Admin Only)
1. Go to Admin Dashboard
2. View Team Members and Volunteers
3. Appoint or remove team members

---

## API Usage

### Report Case via API
```bash
POST http://127.0.0.1:8000/api/report/
Content-Type: multipart/form-data

Parameters:
- case_type (required)
- place_spotted (required)
- needs (required)
- priority (optional: HIGH, MEDIUM, LOW)
- image (optional: file upload)
```

**Note:** Requires authentication

---

## Troubleshooting

### Server won't start?
```bash
# Check if port 8000 is in use
# Try a different port:
python manage.py runserver 8080
```

### Can't upload images?
- Ensure Pillow is installed: `pip install pillow`
- Check that `media/` directory exists

### Forgot admin password?
```bash
python manage.py changepassword <username>
```

---

## Project Structure
```
Aashray2/
├── manage.py           # Django management
├── db.sqlite3          # Database
├── aashray/            # Project settings
├── cases/              # Main app
├── templates/          # HTML files
├── static/             # CSS files
└── media/              # Uploaded images
```

---

## Need Help?

📖 See [README.md](file:///c:/Users/YAHWIN%20LUKOSE/OneDrive/Desktop/Aashray2/README.md) for full documentation

🎯 Check [walkthrough.md](file:///C:/Users/YAHWIN%20LUKOSE/.gemini/antigravity/brain/972381cf-875e-448d-8d7e-c4c94e7eb2ed/walkthrough.md) for implementation details

---

**Aashray** - Together, we fight hunger. 🌾
