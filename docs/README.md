# שרת אותנטיקציה מבוסס Django

שרת זה מספק שירותי אותנטיקציה והרשאות למערכת ניהול המחסן המודולרית. הוא אחראי על ניהול משתמשים, הרשאות, ותפקידים במערכת.

## תכונות עיקריות

- ניהול משתמשים ופרופילים
- ניהול הרשאות ותפקידים
- אותנטיקציה מבוססת JWT
- API מלא לניהול משתמשים והרשאות
- ממשק ניהול מובנה

## דרישות מערכת

- Python 3.9 ומעלה
- Django 4.2 ומעלה
- PostgreSQL (מומלץ) או SQLite

## התקנה

1. התקן את הדרישות:
```bash
cd MODUL_APP/django_auth_service
pip install -r requirements.txt
```

2. הגדר את משתני הסביבה בקובץ `.env`:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

3. הרץ את המיגרציות:
```bash
python manage.py migrate
```

4. צור משתמש אדמין:
```bash
python manage.py createsuperuser
```

## הפעלה

הפעל את השרת:
```bash
python manage.py runserver 0.0.0.0:8000
```

השרת יפעל בכתובת `http://localhost:8000`.

## נקודות קצה עיקריות

### אותנטיקציה
- `POST /api/auth/login/` - התחברות למערכת
- `POST /api/auth/register/` - הרשמה למערכת
- `POST /api/token/` - קבלת טוקן JWT
- `POST /api/token/refresh/` - רענון טוקן JWT
- `POST /api/token/verify/` - אימות טוקן JWT

### ניהול משתמשים
- `GET /api/auth/users/` - רשימת משתמשים
- `GET /api/auth/users/{id}/` - פרטי משתמש
- `GET /api/auth/profiles/` - רשימת פרופילים
- `GET /api/auth/user-permissions/` - הרשאות המשתמש הנוכחי

### ניהול הרשאות
- `GET /api/auth/permissions/` - רשימת הרשאות
- `GET /api/auth/roles/` - רשימת תפקידים
- `GET /api/auth/user-roles/` - רשימת תפקידי משתמשים

### בדיקת בריאות
- `GET /api/health/` - בדיקת בריאות השרת

## שימוש בבסיס נתונים היברידי

שרת האותנטיקציה משתמש בבסיס נתונים מרכזי לניהול משתמשים והרשאות. הוא מספק גישה לשירותים האחרים במערכת לצורך אימות והרשאות.

## אבטחה

- כל הסיסמאות מוצפנות בבסיס הנתונים
- שימוש ב-JWT לאימות
- הגדרת הרשאות מפורטות לכל פעולה
- תיעוד כניסות למערכת 