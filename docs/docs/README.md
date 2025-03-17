# שירות ניהול מלאי (Flask Inventory Service)

שירות פלאסק לניהול מלאי מלא ומקיף לעסקים.

## יכולות עיקריות

- **ניהול מוצרים** - ניהול מוצרים וקטגוריות
- **ניהול מחסנים ומיקומים** - מבנה היררכי של מיקומים ומחסנים
- **ניהול מלאי** - מעקב אחר כמויות המלאי במיקומים השונים
- **תנועות מלאי** - ניהול כל סוגי התנועות: קבלה, הוצאה, העברה והתאמה
- **דוחות** - דוחות מפורטים על מצב המלאי ותנועות
- **התראות** - התראות אוטומטיות על מלאי נמוך ופגי תוקף

## ארכיטקטורה

השירות בנוי עם Flask ומורכב מהשכבות הבאות:
1. **מודלים** - הגדרת מבנה הנתונים עם SQLAlchemy
2. **סכמות** - הגדרת שכבת הממשק עם Marshmallow
3. **שירותים** - לוגיקה עסקית מורכבת
4. **API Routes** - ממשקי REST להפעלת המערכת

## התקנה

### דרישות מקדימות
- Python 3.8+
- pip

### הוראות התקנה

1. שכפול המאגר:
```bash
git clone <repository_url>
cd flask_inventory_service
```

2. יצירת סביבה וירטואלית:
```bash
python -m venv venv
source venv/bin/activate  # ב-Linux/Mac
venv\Scripts\activate     # ב-Windows
```

3. התקנת תלויות:
```bash
pip install -r requirements.txt
```

4. הגדרת משתני סביבה:
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY=your_secret_key
export DATABASE_URL=sqlite:///inventory.db  # או חיבור אחר לבסיס נתונים
```

5. יצירת בסיס נתונים:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. הפעלת השירות:
```bash
flask run
```

כעת השירות זמין בכתובת: http://localhost:5000

## שימוש ב-API

### ניהול קטגוריות
- `GET /api/v1/categories` - קבלת כל הקטגוריות
- `GET /api/v1/categories/<id>` - קבלת קטגוריה לפי מזהה
- `POST /api/v1/categories` - יצירת קטגוריה חדשה
- `PUT /api/v1/categories/<id>` - עדכון קטגוריה קיימת
- `DELETE /api/v1/categories/<id>` - מחיקת קטגוריה

### ניהול מוצרים
- `GET /api/v1/products` - קבלת כל המוצרים
- `GET /api/v1/products/<id>` - קבלת מוצר לפי מזהה
- `POST /api/v1/products` - יצירת מוצר חדש
- `PUT /api/v1/products/<id>` - עדכון מוצר קיים
- `DELETE /api/v1/products/<id>` - מחיקת מוצר

### ניהול מיקומים
- `GET /api/v1/locations` - קבלת כל המיקומים
- `GET /api/v1/locations/<id>` - קבלת מיקום לפי מזהה
- `POST /api/v1/locations` - יצירת מיקום חדש
- `PUT /api/v1/locations/<id>` - עדכון מיקום קיים
- `DELETE /api/v1/locations/<id>` - מחיקת מיקום

### ניהול פריטי מלאי
- `GET /api/v1/inventory` - קבלת כל פריטי המלאי
- `GET /api/v1/inventory/<id>` - קבלת פריט מלאי לפי מזהה
- `POST /api/v1/inventory` - יצירת פריט מלאי חדש
- `PUT /api/v1/inventory/<id>` - עדכון פריט מלאי קיים
- `DELETE /api/v1/inventory/<id>` - מחיקת פריט מלאי

### ניהול תנועות
- `GET /api/v1/transactions` - קבלת כל תנועות המלאי
- `GET /api/v1/transactions/<id>` - קבלת תנועת מלאי לפי מזהה
- `POST /api/v1/transactions` - יצירת תנועת מלאי חדשה

### פעולות מלאי מתקדמות
- `GET /api/v1/inventory/summary/<product_id>` - סיכום מלאי למוצר
- `POST /api/v1/inventory/receive` - קבלת מלאי למחסן
- `POST /api/v1/inventory/issue` - הוצאת מלאי מהמחסן
- `POST /api/v1/inventory/transfer` - העברת מלאי בין מיקומים
- `POST /api/v1/inventory/adjust` - התאמת מלאי
- `GET /api/v1/inventory/alerts` - קבלת התראות מלאי
- `GET /api/v1/inventory/expiring` - קבלת פריטי מלאי שעומדים לפוג

### דוחות מלאי
- `GET /api/v1/reports/inventory/current` - דוח מלאי נוכחי
- `GET /api/v1/reports/inventory/transactions` - דוח תנועות מלאי
- `GET /api/v1/reports/inventory/slow-moving` - דוח מלאי איטי
- `GET /api/v1/reports/inventory/value` - דוח ערך מלאי

## תיעוד נוסף

לפרטים נוספים, ראה את תיקיית התיעוד:

- [מודול ניהול מלאי](docs/inventory_module.md) - תיאור מפורט של המודול
- [תהליכים עסקיים במודול המלאי](docs/inventory_processes.md) - תיאור התהליכים העסקיים

## אודות

פותח על ידי צוות הפיתוח של מערכת ניהול עסק מודולרית.

## רישיון

MIT 