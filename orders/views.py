from django.contrib import messages
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'orders/order/detail.html',
                  {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
    "order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response)
    return response


def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    orderItem = OrderItem.objects.all().filter(order_id=order_id)
    list_of_products = []
    list_of_quantity = []
    list_price = []
    for i in orderItem:
        list_of_products.append(i.product.name)
        list_of_quantity.append(i.quantity)
        list_price.append(i.price*i.quantity)

    subject = 'Order № {}'.format(order_id)
    message = 'Dear {} {},\nYou have successfully placed an order.\
                \nYour order id is {}.\nProduct: {} , \
                \nQuantity: {} шт In accordance, \
                \nTotal Price: {} ₴ '.format(order.first_name, order.last_name,order.id, (', '.join(list_of_products)),
                                             (', '.join(map(str,list_of_quantity))), sum(list_price))
    mail = EmailMessage(subject, message, 'dimoj15@ukr.net',
                     [order.email])
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)
    # Прикрепляем PDF к электронному сообщению.

    mail.attach('order_{}.pdf'.format(order.id),
                 out.getvalue(),
                 'application/pdf')
    mail.send()


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            order_created(order.id)
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})

