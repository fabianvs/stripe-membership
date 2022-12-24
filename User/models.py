from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    """Model definition for Profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField(upload_to='user/picture', blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    university = models.CharField(max_length=50, null=True, blank=True)
    carrer = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(blank=True)


    class Meta:
        """Meta definition for Profile."""
        abstract = True


class Profesor(Profile):
    """Model definition for Profesor."""

    visibility = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Profesor."""

        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesors'

    def __str__(self):
        """Unicode representation of Profesor."""
        return self.user.__str__()


class Student(Profile):
    """Model definition for Student."""

    studing = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        """Meta definition for Student."""

        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        """Unicode representation of Profesor."""
        return self.user.__str__()

# No se usa con TBK
class Pay_method(models.Model):
    """Model definition for Pay_method."""

    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    card_number = models.CharField(max_length=16, null=False, blank=False)
    card_date = models.DateField()
    security_num = models.CharField(max_length=3, null=False, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Pay_method."""

        verbose_name = 'Pay_method'
        verbose_name_plural = 'Pay_methods'

    def __str__(self):
        """Unicode representation of Pay_method."""
        pass


class Document(models.Model):
    """Model definition for Document."""

    doc_path = models.FileField(upload_to='documents/File/')
    doc_img = models.ImageField(upload_to='documents/File_img/')
    file_name = models.CharField(max_length=30)
    file_type = models.CharField(max_length=30)
    file_desc = models.TextField(max_length=70)
    stu_rel = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        """Meta definition for Document."""

        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        """Unicode representation of Document."""
        return self.file_name.__str__()


class Post_file(models.Model):
    """Model definition for Post_file."""

    user_rel = models.ForeignKey(User, on_delete=models.CASCADE)
    file_rel = models.OneToOneField(Document,on_delete=models.CASCADE)

    post_title = models.CharField(max_length=30, null=False, blank=False)
    post_desc = models.TextField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    

    class Meta:
        """Meta definition for Post_file."""

        verbose_name = 'Post_File'
        verbose_name_plural = 'Post_files'

    def __str__(self):
        """Unicode representation of Post_file."""
        return '{} post {}'.format(self.user_rel, self.post_title.__str__())

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    finish = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Order Status'

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    tax = models.IntegerField()
    total = models.IntegerField()
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buy_order = models.CharField(max_length=26, null=True, blank=True)
    session_id = models.CharField(max_length=61, null=True, blank=True)
    amount = models.FloatField(max_length=17, null=True, blank=True)
    vci = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=64, null=True, blank=True)
    card_number = models.CharField(max_length=19, null=True, blank=True)
    accounting_date = models.CharField(max_length=4, null=True, blank=True)
    transaction_date = models.CharField(max_length=24, null=True, blank=True)
    authorization_code = models.CharField(max_length=6, null=True, blank=True)
    payment_type_code = models.CharField(max_length=10, null=True, blank=True)
    response_code = models.IntegerField(null=True, blank=True)
    installments_amount = models.IntegerField(max_length=17, null=True, blank=True)
    installments_number = models.IntegerField(max_length=2, null=True, blank=True)
    balance = models.CharField(max_length=17, null=True, blank=True)
    class Meta:
        verbose_name = 'Payment History'
        verbose_name_plural = 'Payments History'

    def __str__(self):
        return self.buy_order

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    number = models.IntegerField()
    document = models.FileField(upload_to='documents/Invoices/', blank=True, null=True)

    def __str__(self):
        return self.number