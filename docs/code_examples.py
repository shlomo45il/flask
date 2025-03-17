"""
דוגמאות קוד לשימוש במודול ניהול המשתמשים
"""

from django.contrib.auth.models import User
from auth_app.models import (
    UserProfile, SupplierProfile, Permission, 
    Role, UserRole, UserActivityLog
)


def create_user_examples():
    """
    דוגמאות ליצירת משתמשים מסוגים שונים
    """
    # יצירת מנהל
    admin_user = User.objects.create_user(
        username='admin1',
        email='admin1@example.com',
        password='secure_admin_password',
        first_name='מנהל',
        last_name='ראשי',
        is_staff=True
    )
    admin_profile = admin_user.profile
    admin_profile.phone_number = '050-1111111'
    admin_profile.position = 'מנהל מערכת'
    admin_profile.department = 'הנהלה'
    admin_profile.save()
    
    # יצירת עובד
    employee_user = User.objects.create_user(
        username='emp1',
        email='emp1@example.com',
        password='secure_emp_password',
        first_name='עובד',
        last_name='ישראלי'
    )
    employee_profile = employee_user.profile
    employee_profile.phone_number = '050-2222222'
    employee_profile.position = 'נציג שירות'
    employee_profile.department = 'שירות לקוחות'
    employee_profile.save()
    
    # יצירת לקוח
    customer_user = User.objects.create_user(
        username='customer1',
        email='customer1@example.com',
        password='secure_customer_password',
        first_name='לקוח',
        last_name='ישראלי'
    )
    customer_profile = customer_user.profile
    customer_profile.phone_number = '050-3333333'
    customer_profile.user_type = 'customer'
    customer_profile.save()
    
    # יצירת ספק
    supplier_user = User.objects.create_user(
        username='supplier1',
        email='supplier1@example.com',
        password='secure_supplier_password',
        first_name='ספק',
        last_name='ישראלי'
    )
    supplier_profile = supplier_user.profile
    supplier_profile.phone_number = '050-4444444'
    supplier_profile.user_type = 'supplier'
    supplier_profile.save()
    
    # עדכון פרטי ספק
    supplier_details = supplier_profile.supplier_profile
    supplier_details.company_name = 'חברה לדוגמה בע"מ'
    supplier_details.business_number = '123456789'
    supplier_details.tax_number = '987654321'
    supplier_details.address = 'רחוב הדוגמה 123, תל אביב'
    supplier_details.contact_person = 'ישראל ישראלי'
    supplier_details.payment_terms = 'שוטף + 30'
    supplier_details.credit_limit = 10000.00
    supplier_details.rating = 4
    supplier_details.notes = 'ספק מוצרי חשמל'
    supplier_details.save()
    
    return {
        'admin': admin_user,
        'employee': employee_user,
        'customer': customer_user,
        'supplier': supplier_user
    }


def create_permissions_examples():
    """
    דוגמאות ליצירת הרשאות
    """
    permissions = []
    
    # הרשאות מודול מלאי
    inventory_permissions = [
        ('view_inventory', 'view', 'inventory', 'צפייה במלאי'),
        ('add_inventory', 'add', 'inventory', 'הוספת פריט למלאי'),
        ('edit_inventory', 'change', 'inventory', 'עריכת פריט במלאי'),
        ('delete_inventory', 'delete', 'inventory', 'מחיקת פריט מהמלאי'),
        ('export_inventory', 'export', 'inventory', 'ייצוא דוח מלאי'),
    ]
    
    # הרשאות מודול הזמנות
    orders_permissions = [
        ('view_orders', 'view', 'orders', 'צפייה בהזמנות'),
        ('add_order', 'add', 'orders', 'יצירת הזמנה חדשה'),
        ('edit_order', 'change', 'orders', 'עריכת הזמנה'),
        ('delete_order', 'delete', 'orders', 'מחיקת הזמנה'),
        ('approve_order', 'approve', 'orders', 'אישור הזמנה'),
    ]
    
    # הרשאות מודול לקוחות
    customers_permissions = [
        ('view_customers', 'view', 'customers', 'צפייה בלקוחות'),
        ('add_customer', 'add', 'customers', 'הוספת לקוח'),
        ('edit_customer', 'change', 'customers', 'עריכת לקוח'),
        ('delete_customer', 'delete', 'customers', 'מחיקת לקוח'),
    ]
    
    # הרשאות מודול ספקים
    suppliers_permissions = [
        ('view_suppliers', 'view', 'suppliers', 'צפייה בספקים'),
        ('add_supplier', 'add', 'suppliers', 'הוספת ספק'),
        ('edit_supplier', 'change', 'suppliers', 'עריכת ספק'),
        ('delete_supplier', 'delete', 'suppliers', 'מחיקת ספק'),
    ]
    
    # הרשאות מודול משתמשים
    users_permissions = [
        ('view_users', 'view', 'users', 'צפייה במשתמשים'),
        ('add_user', 'add', 'users', 'הוספת משתמש'),
        ('edit_user', 'change', 'users', 'עריכת משתמש'),
        ('delete_user', 'delete', 'users', 'מחיקת משתמש'),
        ('assign_role', 'change', 'users', 'הקצאת תפקיד למשתמש'),
    ]
    
    # יצירת כל ההרשאות
    for perm_list in [inventory_permissions, orders_permissions, 
                      customers_permissions, suppliers_permissions, 
                      users_permissions]:
        for code, perm_type, module, name in perm_list:
            perm = Permission.objects.create(
                name=name,
                code=code,
                permission_type=perm_type,
                module=module,
                description=f'הרשאה ל{name}'
            )
            permissions.append(perm)
    
    return permissions


def create_roles_examples(permissions):
    """
    דוגמאות ליצירת תפקידים
    """
    # תפקיד מנהל מערכת
    admin_role = Role.objects.create(
        name='מנהל מערכת',
        description='גישה מלאה לכל המערכת'
    )
    # הקצאת כל ההרשאות למנהל מערכת
    admin_role.permissions.add(*permissions)
    
    # תפקיד מנהל מלאי
    inventory_manager_role = Role.objects.create(
        name='מנהל מלאי',
        description='ניהול מלאי המערכת'
    )
    # הקצאת הרשאות מלאי
    inventory_perms = Permission.objects.filter(module='inventory')
    inventory_manager_role.permissions.add(*inventory_perms)
    
    # תפקיד נציג מכירות
    sales_rep_role = Role.objects.create(
        name='נציג מכירות',
        description='טיפול בהזמנות ולקוחות'
    )
    # הקצאת הרשאות הזמנות ולקוחות (צפייה בלבד במלאי)
    sales_perms = list(Permission.objects.filter(module='orders'))
    sales_perms.extend(list(Permission.objects.filter(module='customers')))
    sales_perms.append(Permission.objects.get(code='view_inventory'))
    sales_rep_role.permissions.add(*sales_perms)
    
    # תפקיד מנהל רכש
    procurement_role = Role.objects.create(
        name='מנהל רכש',
        description='ניהול ספקים והזמנות רכש'
    )
    # הקצאת הרשאות ספקים ומלאי
    procurement_perms = list(Permission.objects.filter(module='suppliers'))
    procurement_perms.extend(list(Permission.objects.filter(module='inventory')))
    procurement_role.permissions.add(*procurement_perms)
    
    return {
        'admin': admin_role,
        'inventory_manager': inventory_manager_role,
        'sales_rep': sales_rep_role,
        'procurement': procurement_role
    }


def assign_roles_to_users(users, roles, admin_user):
    """
    דוגמאות להקצאת תפקידים למשתמשים
    """
    # הקצאת תפקיד מנהל מערכת למנהל
    UserRole.objects.create(
        user=users['admin'],
        role=roles['admin'],
        assigned_by=admin_user
    )
    
    # הקצאת תפקיד מנהל מלאי לעובד
    UserRole.objects.create(
        user=users['employee'],
        role=roles['inventory_manager'],
        assigned_by=admin_user
    )
    
    # הקצאת תפקיד נציג מכירות לעובד
    UserRole.objects.create(
        user=users['employee'],
        role=roles['sales_rep'],
        assigned_by=admin_user
    )
    
    # הקצאת תפקיד מנהל רכש למנהל
    UserRole.objects.create(
        user=users['admin'],
        role=roles['procurement'],
        assigned_by=admin_user
    )


def log_activity_examples(users):
    """
    דוגמאות לתיעוד פעילות משתמשים
    """
    # תיעוד התחברות
    UserActivityLog.objects.create(
        user=users['admin'],
        activity_type='login',
        description='התחברות למערכת',
        ip_address='192.168.1.1',
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    # תיעוד יצירת משתמש
    UserActivityLog.objects.create(
        user=users['admin'],
        activity_type='create',
        description=f'יצירת משתמש חדש: {users["employee"].username}',
        ip_address='192.168.1.1',
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    # תיעוד שינוי הרשאות
    UserActivityLog.objects.create(
        user=users['admin'],
        activity_type='role_change',
        description=f'הקצאת תפקיד מנהל מלאי למשתמש: {users["employee"].username}',
        ip_address='192.168.1.1',
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    # תיעוד התנתקות
    UserActivityLog.objects.create(
        user=users['admin'],
        activity_type='logout',
        description='התנתקות מהמערכת',
        ip_address='192.168.1.1',
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )


def check_permissions_example(user, permission_code, module):
    """
    דוגמה לבדיקת הרשאות
    """
    has_permission = user.user_roles.filter(
        role__permissions__code=permission_code,
        role__permissions__module=module,
        role__is_active=True
    ).exists()
    
    return has_permission


def run_all_examples():
    """
    הרצת כל הדוגמאות
    """
    # יצירת משתמשים
    users = create_user_examples()
    
    # יצירת הרשאות
    permissions = create_permissions_examples()
    
    # יצירת תפקידים
    roles = create_roles_examples(permissions)
    
    # הקצאת תפקידים למשתמשים
    assign_roles_to_users(users, roles, users['admin'])
    
    # תיעוד פעילות
    log_activity_examples(users)
    
    # בדיקת הרשאות
    admin_can_view_inventory = check_permissions_example(
        users['admin'], 'view_inventory', 'inventory'
    )
    employee_can_add_order = check_permissions_example(
        users['employee'], 'add_order', 'orders'
    )
    
    print(f"מנהל יכול לצפות במלאי: {admin_can_view_inventory}")
    print(f"עובד יכול ליצור הזמנה: {employee_can_add_order}")


if __name__ == "__main__":
    # הערה: קוד זה מיועד להדגמה בלבד ולא להרצה ישירה
    # run_all_examples()
    pass 