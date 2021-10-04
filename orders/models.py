from django.core.validators import RegexValidator
from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField('first_name', max_length=50, validators=[RegexValidator(
        regex=r'^([а-яА-Яё\s]+|[a-zA-Z\s]+)$',  message='Имя должно состоять из букв')], help_text="Example: Ivan, Dmytro, Vasya")
    last_name = models.CharField('last_name', max_length=50, validators=[RegexValidator(
        regex=r'^([а-яА-Яё\s]+|[a-zA-Z\s]+)$', message='Фамилия должна состоять из букв')], help_text="Example: Miroshnichenko, Yarosh, Galagan")
    email = models.EmailField(validators=[RegexValidator(regex=r'\w[\w\.-]*@\w[\w\.-]+\.\w+')],
                              help_text="Example: example@gmail.com")
    address = models.CharField(max_length=250, validators=[RegexValidator(
        regex=r'^[0-9a-zA-Zа-яА-Яё. ]+$', message='В адресе не должно быть *,\//')], help_text="Example: Pushkinska 13")
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Телефон должен состоять из цыфр')],
                             help_text="Example: +380663846078 / 0663846078")
    postal_code = models.CharField(max_length=5, validators=[RegexValidator( regex = r'^(^[0-9]{5}(?:-[0-9]{4})?$|^$)', message='Почтовый индекс должен состоять из 5 цыфр')],
                                   help_text="Example: 20501, 30512")
    city = models.CharField(max_length=50, validators=[RegexValidator(
        regex=r'^([а-яА-Яё\s]+|[a-zA-Z\s]+)$', message='Название города должно состоять из букв')], help_text="Example: Kharkov, Kyiv")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity