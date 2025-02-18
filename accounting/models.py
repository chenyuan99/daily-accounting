from django.db import models
from django.utils import timezone
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User, Group


class ImageModel(models.Model):
    """
    Model for storing images using Cloudinary.
    
    Attributes:
        img (CloudinaryField): The image file stored in Cloudinary
        id (CharField): Unique identifier for the image
    """
    img = CloudinaryField('image', null=True)
    id = models.CharField(max_length=16, primary_key=True)


class Currency(models.Model):
    """
    Model for storing different types of currencies.
    
    Attributes:
        name (str): Name of the currency
        icon (str): Icon representation of the currency
    """
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Account(models.Model):
    """
    Model representing a financial account.
    
    Attributes:
        name (str): Name of the account
        amount (Decimal): Current balance of the account
        currency (Currency): Foreign key to Currency model
        icon (str): Icon representation of the account
        created_date (DateTime): When the account was created
        updated_date (DateTime): When the account was last updated
        owner (User): Foreign key to User model representing account owner
    """
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=1)
    icon = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_date']


class Category(models.Model):
    """
    Model for categorizing financial transactions.
    
    Attributes:
        name (str): Name of the category
        icon (str): Icon representation of the category
        category_type (str): Type of category - either 'expense' or 'income'
    """
    CATEGORY_TYPES = (
        ("expense", "支出"),
        ("income", "收入"),
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    category_type = models.CharField(choices=CATEGORY_TYPES, default=CATEGORY_TYPES[0][0], max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class SubCategory(models.Model):
    """
    Model for sub-categorizing financial transactions.
    
    Attributes:
        name (str): Name of the sub-category
        icon (str): Icon representation of the sub-category
        parent (Category): Foreign key to Category model representing parent category
    """
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    parent = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class HistoryRecord(models.Model):
    """
    Model for storing historical financial records.
    
    Attributes:
        account (Account): Foreign key to Account model representing account associated with record
        time_of_occurrence (DateTime): When the record occurred
        category (Category): Foreign key to Category model representing category of record
        sub_category (SubCategory): Foreign key to SubCategory model representing sub-category of record
        currency (Currency): Foreign key to Currency model representing currency of record
        amount (Decimal): Amount of the record
        comment (str): Comment or description of the record
        created_date (DateTime): When the record was created
        updated_date (DateTime): When the record was last updated
        owner (User): Foreign key to User model representing owner of record
    """
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, default=1)
    time_of_occurrence = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=1)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    class Meta:
        ordering = ['-time_of_occurrence']


class TransferRecord(models.Model):
    """
    Model for storing transfer records between accounts.
    
    Attributes:
        from_account (Account): Foreign key to Account model representing account that transferred from
        to_account (Account): Foreign key to Account model representing account that transferred to
        time_of_occurrence (DateTime): When the transfer occurred
        currency (Currency): Foreign key to Currency model representing currency of transfer
        amount (Decimal): Amount of the transfer
        comment (str): Comment or description of the transfer
        created_date (DateTime): When the transfer was created
        updated_date (DateTime): When the transfer was last updated
        owner (User): Foreign key to User model representing owner of transfer
    """
    from_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, default=1,
                                     related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, default=2, related_name='to_account')
    time_of_occurrence = models.DateTimeField(default=timezone.now)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=1)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-time_of_occurrence']


class Statement(models.Model):
    """
    Model for storing financial statements.
    
    Attributes:
        created_date (DateTime): When the statement was created
    """
    created_date = models.DateTimeField(default=timezone.now)
    # HistoryRecord