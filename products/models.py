from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    pass


class Customer(CustomUser):
    otchestvo = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=20, null=False, blank=False, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


class Employer(CustomUser):
    otchestvo = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    image = models.ImageField(null=True, blank=True, upload_to='image/', verbose_name='Фотография сотрудника')
    employer_position = models.ForeignKey(to='EmployerPosition', on_delete=models.CASCADE, null=True, blank=True,
                                            verbose_name='Должность')
    category = models.ForeignKey(to='UslugaCategory', on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name="Категория услуги")
    phone_number = models.CharField(max_length=20, null=False, blank=False, verbose_name='Номер телефона')
    date_of_employment = models.DateField(null=True, blank=False, verbose_name='Дата приема на работу')
    date_of_dismissal = models.DateField(null=True, blank=True, verbose_name='Дата увольнения')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class EmployerPosition(models.Model):
    title = models.CharField(max_length=40, null=False, blank=False, verbose_name='Должность')

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class ZayavkaState(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='Статус заявки')

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявки'


class DogovorState(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='Статус договора')

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Статус договора'
        verbose_name_plural = 'Статусы договора'


class Price(models.Model):
    number = models.CharField(max_length=20, null=False, blank=False, verbose_name='Номер прайс-листа')
    data = models.DateField(verbose_name="Дата утверждения прайс-листа", auto_now_add=True)
    employer = models.ForeignKey(to='Employer', on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name="Сотрудник")

    def __str__(self):
        return '%s ' % self.data

    class Meta:
        verbose_name = 'Прайс-лист',
        verbose_name_plural = 'Прайс-листы'


class Position_Price(models.Model):
    usluga = models.ForeignKey('Usluga', on_delete=models.CASCADE, blank=True, null=True,
            related_name="positions_prices", verbose_name="Услуга")
    cost_product = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False,
                                       verbose_name="Стоимость услуги")
    price_list = models.ForeignKey('Price', on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='Прайс-лист')

    def __str__(self):
        return '%s %s руб.' % (self.usluga,  self.cost_product)

    class Meta:
        verbose_name = 'Позиция прайс-листа',
        verbose_name_plural = 'Позиции прайс-листа'


class Zayavka(models.Model):
    number = models.CharField(max_length=10, null=False, blank=False, verbose_name='Номер заявки')
    date_document = models.DateField(null=False, blank=False, verbose_name='Дата исполнения')
    position = models.ManyToManyField(to='Position_Price', null=True, blank=True,
                                 verbose_name='Позиция прайс-листа')
    address = models.CharField(max_length=1000, null=False, blank=False, verbose_name='Адрес исполнения')
    description = models.TextField(null=True, blank=True, verbose_name='Комментарий к заявке')
    customer = models.ForeignKey(to='Customer', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Заказчик')
    employer = models.ForeignKey(to='Employer', on_delete=models.CASCADE, null=True, blank=True,
                verbose_name='Сотрудник')
    positions_and_prices = models.TextField(max_length=1000, default='',
                                            verbose_name='Позиции и количество')
    total_price = models.PositiveIntegerField(default=0, verbose_name='Итого')

    def __str__(self):
        return '%s %s %s' % (self.number, self.date_document, self.customer)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class UslugaCategory(models.Model):
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')

    title = models.CharField(max_length=60, null=False, blank=False, verbose_name='Категория услуги')
    image = models.ImageField(upload_to="images/", blank=True, verbose_name="Изображение")

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуги'

class Usluga(models.Model):
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')

    title = models.CharField(max_length=60, null=False, blank=False, verbose_name='Наименование услуги')
    description = models.TextField(verbose_name='Описание услуги')
    image = models.ImageField(upload_to="images/", blank=True, verbose_name="Изображение")
    category = models.ForeignKey(to='UslugaCategory', on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name="Категория услуги")

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Comment(models.Model):
    user = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=True, blank=True,
            verbose_name='Заказчик')
    zayavka = models.ForeignKey(to=Zayavka, on_delete=models.CASCADE, verbose_name='Завка')
    text = models.TextField(max_length=1000, verbose_name='Текст отзыва')
    publication = models.BooleanField(default=False, verbose_name='Опубликовать')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'        

    def __str__(self):
        return f'Отзыв пользователя {self.user.username} к заявке {self.zayavka.number}'


class Dogovor(models.Model):
    number = models.CharField(max_length=30, null=False, blank=False, verbose_name='Номер договора')
    date_oformlenie = models.DateField(verbose_name='Дата оформления договора', null=False, blank=False)
    date_ispolnenie = models.DateField(verbose_name='Дата расторжения', null=True, blank=True)
    summa = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name='Сумма договора')
    zayavka = models.OneToOneField(Zayavka, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Номер заявки')

    def __str__(self):
        return '%s %s %s' % (self.number, self.date_oformlenie, self.summa)

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'


class StateofDogovor(models.Model):
    dogovor = models.ForeignKey(to='Dogovor', on_delete=models.CASCADE, verbose_name='Договор', null=True, blank=True)
    status = models.ForeignKey(to='DogovorState', on_delete=models.CASCADE, verbose_name='Статус договора', null=True,
                                blank=True)
    date = models.DateField(verbose_name='Дата статуса', null=False, blank=False)
    employer = models.ForeignKey(to='Employer', on_delete=models.CASCADE, verbose_name='Сотрудник', null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.dogovor, self.status, self.date)

    class Meta:
        verbose_name = 'Статус в договоре'
        verbose_name_plural = 'Статусы в договоре'


class StateofZayavka(models.Model):
    zayavka = models.ForeignKey(to='Zayavka', on_delete=models.CASCADE, verbose_name='Заявка', 
                                related_name='stateozayvkas', null=True, blank=True)
    status = models.ForeignKey(to='ZayavkaState', on_delete=models.CASCADE, verbose_name='Статус заявки',
                                related_name='stateozayvkas', null=True, blank=True)
    date = models.DateField(verbose_name='Дата статуса', null=False, blank=False)
    employer = models.ForeignKey(to='Employer', on_delete=models.CASCADE, verbose_name='Сотрудник',
                                    null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.zayavka, self.status, self.date)

    class Meta:
        verbose_name = 'Статус в заявке'
        verbose_name_plural = 'Статусы в заявке'


class Contact(models.Model):
    username = models.CharField(max_length=255)
    message = models.TextField(max_length=200, blank=False, null=True, verbose_name='Сообщение')
    data = models.DateField(verbose_name="Дата отправки", default=timezone.now)
    time_send = models.TimeField(verbose_name='Время отправки', default=timezone.now)

    def __str__(self):
        return '%s %s %s' % (self.username, self.data, self.time_send)

    class Meta:
        verbose_name = 'Сообщение',
        verbose_name_plural = 'Сообщения'


class Act(models.Model):
    number = models.CharField(max_length=30, null=False, blank=False, verbose_name='Номер акта')
    date_document = models.DateField(null=False, blank=False, verbose_name='Дата документа')
    zayavka = models.OneToOneField(to='Zayavka', on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='Номер заявки')
    summa = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name='Итого')

    def __str__(self):
        return '%s %s' % (self.number, self.date_document)

    class Meta:
        verbose_name = 'Акт выполненных работ',
        verbose_name_plural = 'Акты выполненных работ'


class Position_Act(models.Model):
    act = models.ForeignKey(to='Act', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Номер акта')
    position = models.ForeignKey(to='Position_Price', on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='Позиция прайс-листа')
    kolichestvo = models.CharField(max_length=30, null=False, blank=False, verbose_name='Количество услуг')
    itogo = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name='Итого по позиции')

    def __str__(self):
        return '%s' % self.act

    class Meta:
        verbose_name = 'Позиция акта выполненных работ',
        verbose_name_plural = 'Позиции акта выполненных работ'