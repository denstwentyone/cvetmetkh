from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'client'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'manager'


class Metal(models.Model):
    metal_id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'metal'


class OrderStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order_status'


class Receipt(models.Model):
    client = models.ForeignKey(Client, models.DO_NOTHING)
    order_id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(Manager, models.DO_NOTHING)
    status = models.ForeignKey(OrderStatus, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'receipt'


class ReceiptHasMetal(models.Model):
    order = models.OneToOneField(Receipt, models.DO_NOTHING, primary_key=True)
    metal = models.ForeignKey(Metal, models.DO_NOTHING)
    count = models.IntegerField(db_column='Count')  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'receipt_has_metal'
        unique_together = (('order', 'metal'),)


class Supply(models.Model):
    manager = models.ForeignKey(Manager, models.DO_NOTHING)
    supply_id = models.AutoField(primary_key=True)
    status = models.ForeignKey('SupplyStatus', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'supply'


class SupplyHasMetal(models.Model):
    metal = models.OneToOneField(Metal, models.DO_NOTHING, primary_key=True)
    supply = models.ForeignKey(Supply, models.DO_NOTHING)
    count = models.IntegerField(db_column='Count')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'supply_has_metal'
        unique_together = (('metal', 'supply'),)


class SupplyStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'supply_status'