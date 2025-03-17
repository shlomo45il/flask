# מודול ניהול משתמשים - מדריך טכני

## סקירה כללית
מודול ניהול המשתמשים מבוסס על Django ומרחיב את מודל המשתמש המובנה כדי לספק תמיכה בסוגי משתמשים שונים (מנהלים, עובדים, לקוחות וספקים) ומערכת הרשאות מתקדמת.

## דרישות מערכת
- Python 3.8+
- Django 4.0+
- Pillow (לתמיכה בתמונות פרופיל)
- django-rest-framework (לממשקי API)

## התקנה

### 1. התקנת חבילות נדרשות
```bash
pip install -r requirements.txt
```

### 2. הגדרת הגדרות Django
הוסף את האפליקציה לרשימת האפליקציות המותקנות ב-`settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'auth_app',
    # ...
]
```

### 3. הגדרת מודל המשתמש המותאם
```python
AUTH_USER_MODEL = 'auth.User'  # אנו משתמשים במודל המובנה ומרחיבים אותו
```

### 4. הרצת מיגרציות
```bash
python manage.py makemigrations
python manage.py migrate
```

## מבנה המודול

### מודלים

#### UserProfile
מרחיב את מודל המשתמש הבסיסי של Django:
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    # שדות נוספים...
```

#### SupplierProfile
מודל ייעודי לניהול פרטי ספקים:
```python
class SupplierProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='supplier_profile')
    company_name = models.CharField(max_length=200)
    # שדות נוספים...
```

#### Permission, Role, UserRole
מודלים לניהול הרשאות ותפקידים:
```python
class Permission(models.Model):
    name = models.CharField(max_length=100)
    # שדות נוספים...

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, related_name='roles')
    # שדות נוספים...

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    # שדות נוספים...
```

#### UserActivityLog
מודל לניהול היסטוריית פעולות משתמשים:
```python
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    # שדות נוספים...
```

## שימוש במודול

### 1. יצירת משתמש חדש
```python
from django.contrib.auth.models import User
from auth_app.models import UserProfile

# יצירת משתמש בסיסי
user = User.objects.create_user(
    username='customer1',
    email='customer1@example.com',
    password='secure_password',
    first_name='ישראל',
    last_name='ישראלי'
)

# עדכון פרטי פרופיל
profile = user.profile  # נוצר אוטומטית על ידי signal
profile.phone_number = '050-1234567'
profile.user_type = 'customer'
profile.save()
```

### 2. יצירת ספק חדש
```python
from django.contrib.auth.models import User
from auth_app.models import UserProfile, SupplierProfile

# יצירת משתמש בסיסי
user = User.objects.create_user(
    username='supplier1',
    email='supplier1@example.com',
    password='secure_password',
    first_name='חברה',
    last_name='בע"מ'
)

# עדכון פרטי פרופיל
profile = user.profile
profile.user_type = 'supplier'
profile.save()  # יצירת פרופיל ספק תתבצע אוטומטית

# עדכון פרטי ספק
supplier_profile = profile.supplier_profile
supplier_profile.company_name = 'חברה לדוגמה בע"מ'
supplier_profile.business_number = '123456789'
supplier_profile.address = 'רחוב הדוגמה 123, תל אביב'
supplier_profile.contact_person = 'ישראל ישראלי'
supplier_profile.save()
```

### 3. ניהול הרשאות ותפקידים
```python
from auth_app.models import Permission, Role, UserRole

# יצירת הרשאה
permission = Permission.objects.create(
    name='צפייה במלאי',
    code='view_inventory',
    permission_type='view',
    module='inventory',
    description='הרשאה לצפייה במלאי המערכת'
)

# יצירת תפקיד
role = Role.objects.create(
    name='מנהל מלאי',
    description='תפקיד לניהול מלאי המערכת'
)
role.permissions.add(permission)

# הקצאת תפקיד למשתמש
user_role = UserRole.objects.create(
    user=user,
    role=role,
    assigned_by=admin_user  # משתמש מנהל שמקצה את התפקיד
)
```

### 4. בדיקת הרשאות
```python
def check_user_permission(user, permission_code, module):
    """
    בדיקה אם למשתמש יש הרשאה מסוימת
    """
    return user.user_roles.filter(
        role__permissions__code=permission_code,
        role__permissions__module=module,
        role__is_active=True
    ).exists()

# שימוש
if check_user_permission(request.user, 'view_inventory', 'inventory'):
    # המשתמש רשאי לצפות במלאי
    pass
else:
    # אין הרשאה
    pass
```

### 5. תיעוד פעילות משתמש
```python
from auth_app.models import UserActivityLog

def log_user_activity(user, activity_type, description, request=None):
    """
    תיעוד פעילות משתמש
    """
    ip_address = None
    user_agent = None
    
    if request:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
    
    UserActivityLog.objects.create(
        user=user,
        activity_type=activity_type,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent
    )

# שימוש
log_user_activity(
    user=request.user,
    activity_type='login',
    description='התחברות למערכת',
    request=request
)
```

## ממשקי API

המודול מספק ממשקי REST API לניהול משתמשים:

### 1. רשימת משתמשים
```
GET /api/users/
```

### 2. פרטי משתמש
```
GET /api/users/{id}/
```

### 3. יצירת משתמש חדש
```
POST /api/users/
```

### 4. עדכון משתמש
```
PUT /api/users/{id}/
```

### 5. מחיקת משתמש
```
DELETE /api/users/{id}/
```

### 6. רשימת ספקים
```
GET /api/suppliers/
```

## דוגמאות לשימוש ב-API

### יצירת משתמש חדש
```json
POST /api/users/
{
    "username": "customer1",
    "email": "customer1@example.com",
    "password": "secure_password",
    "first_name": "ישראל",
    "last_name": "ישראלי",
    "profile": {
        "phone_number": "050-1234567",
        "user_type": "customer"
    }
}
```

### יצירת ספק חדש
```json
POST /api/users/
{
    "username": "supplier1",
    "email": "supplier1@example.com",
    "password": "secure_password",
    "first_name": "חברה",
    "last_name": "בע\"מ",
    "profile": {
        "phone_number": "03-1234567",
        "user_type": "supplier"
    },
    "supplier_profile": {
        "company_name": "חברה לדוגמה בע\"מ",
        "business_number": "123456789",
        "address": "רחוב הדוגמה 123, תל אביב",
        "contact_person": "ישראל ישראלי"
    }
}
```

## שיקולי אבטחה

1. **הצפנת סיסמאות**: כל הסיסמאות מוצפנות באמצעות אלגוריתם ההצפנה של Django.
2. **הגנה מפני CSRF**: שימוש ב-CSRF token בכל טפסי המערכת.
3. **הגבלת ניסיונות התחברות**: חסימה זמנית לאחר מספר ניסיונות התחברות כושלים.
4. **תיעוד פעילות**: תיעוד כל פעולות המשתמשים לצורכי אבטחה וביקורת.

## פתרון בעיות נפוצות

### בעיה: פרופיל משתמש לא נוצר אוטומטית
פתרון: ודא שה-signal `post_save` רשום כראוי:
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

### בעיה: שגיאת הרשאות
פתרון: בדוק את הקצאת התפקידים וההרשאות למשתמש:
```python
# בדיקת תפקידים של משתמש
user_roles = user.user_roles.all()
for user_role in user_roles:
    print(f"תפקיד: {user_role.role.name}")
    print(f"הרשאות: {[p.code for p in user_role.role.permissions.all()]}")
```

## פיתוח עתידי

1. **אימות דו-שלבי**: הוספת תמיכה באימות דו-שלבי.
2. **אינטגרציה עם OAuth**: תמיכה בהתחברות באמצעות ספקי זהות חיצוניים.
3. **ניהול הסכמי שירות**: מודול לניהול הסכמי שירות עם ספקים.
4. **פורטל ספקים/לקוחות**: ממשקים ייעודיים לספקים ולקוחות.

## תרומה לפרויקט

אנו מעודדים תרומה לפרויקט. אנא עקבו אחר הנחיות אלה:
1. צרו fork של הפרויקט
2. צרו branch חדש לתכונה או תיקון
3. הגישו pull request עם תיאור מפורט של השינויים

## רישיון

פרויקט זה מופץ תחת רישיון MIT. ראה קובץ LICENSE למידע נוסף. 