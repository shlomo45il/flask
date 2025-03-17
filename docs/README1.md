# שירות ניהול לקוחות

מודול לניהול לקוחות במערכת עסקית מודולרית, מיושם ב-Flask.

## מבנה המערכת

השירות מאורגן בצורה מודולרית עם הפרדה ברורה בין שכבות:

- **מודלים**: הגדרת מבנה נתוני הלקוח בבסיס הנתונים
- **שירותים**: לוגיקה עסקית לטיפול בלקוחות
- **API**: נקודות קצה ומימוש REST API
- **סכימות**: הגדרת פורמט הנתונים וחוקי האימות

## התקנה

### תלויות

```bash
pip install -r requirements.txt
```

### הגדרות סביבה

יש להגדיר את משתני הסביבה הבאים בקובץ `.env`:

```
DATABASE_URL=postgresql://username:password@host:port/db_name
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
APP_SETTINGS=config.DevelopmentConfig
```

### יצירת בסיס נתונים

```bash
flask db init
flask db migrate
flask db upgrade
```

## הפעלה

### פיתוח

```bash
python run.py
```

### ייצור

```bash
gunicorn --bind 0.0.0.0:5002 wsgi:app
```

## נקודות קצה של ה-API

### לקוחות

1. **קבלת כל הלקוחות**
   - `GET /api/customers`
   - פרמטרים: `page`, `per_page`, `is_active`

2. **קבלת לקוח ספציפי**
   - `GET /api/customers/<customer_id>`

3. **יצירת לקוח חדש**
   - `POST /api/customers`
   - גוף בקשה: `name`, `email`, `phone`, ו-שדות אופציונליים אחרים

4. **עדכון לקוח**
   - `PUT /api/customers/<customer_id>`
   - גוף בקשה: שדות לעדכון

5. **מחיקת לקוח**
   - `DELETE /api/customers/<customer_id>`

6. **חיפוש לקוחות**
   - `GET /api/customers/search?q=<query>`
   - פרמטרים: `q`, `page`, `per_page`, `is_active`

7. **סינון לקוחות**
   - `GET /api/customers/filter`
   - פרמטרים: `is_active`, `category`, `city`, `country`, `page`, `per_page`

8. **קבלת היסטוריית פעולות של לקוח**
   - `GET /api/customers/<customer_id>/logs`
   - פרמטרים: `page`, `per_page`

9. **קבלת סטטיסטיקות לקוחות**
   - `GET /api/customers/stats`

## פיתוח עתידי

1. שילוב עם מודול אימות והרשאות
2. שילוב עם מודול הזמנות
3. יצוא נתוני לקוחות לפורמטים שונים (CSV, Excel)
4. ייבוא לקוחות ממקורות חיצוניים
5. ניתוח התנהגות לקוחות 