from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('adventure', 'Adventure'),
        ('kids', 'Children\'s Books'),
        ('classics', 'Classics'),
        ('comics', 'Comics and Graphic Novels'),
        ('fantasy', 'Fantasy'),
        ('historical', 'Historical Fiction'),
        ('horror', 'Horror'),
        ('literary', 'Literary Fiction'),
        ('mystery', 'Mystery'),
        ('non_fiction', 'Non-Fiction'),
    ]
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='adventure',
    )
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class UserReg(models.Model):
    CATEGORY_GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    id_num = models.CharField(max_length=100)  # Automatically set to now when created
    gender = models.CharField(
        max_length=6,
        choices=CATEGORY_GENDER,
        default='male',
    )
    reg_num = models.CharField(max_length=20, unique=True, blank=True, null=False)

    def __str__(self):
        return self.name

# Signal to generate reg_num
@receiver(pre_save, sender=UserReg)
def generate_reg_num(sender, instance, **kwargs):
    if not instance.reg_num:
        prefix = 'm-' if instance.gender == 'male' else 'f-'
        last_user = UserReg.objects.filter(gender=instance.gender).order_by('id').last()
        if last_user:
            last_id = int(last_user.reg_num.split('-')[1])
        else:
            last_id = 0
        instance.reg_num = f"{prefix}{last_id + 1:04d}"

class UserGetBooks(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_get_books')
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE, related_name='user_get_books')

    def __str__(self):
        return f"{self.user.name} - {self.book.name}"
