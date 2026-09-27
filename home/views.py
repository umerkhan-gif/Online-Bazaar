from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Product, Category, Order, OrderItem
from .forms import ProductForm, CheckoutForm
from django.core.mail import send_mail


def home(request):

    categories = Category.objects.all()

    featured_products = Product.objects.all()[:8]

    return render(
        request,
        'home/index.html',
        {
            'categories': categories,
            'featured_products': featured_products
        }
    )


def products(request):

    products = Product.objects.all()

    return render(
        request,
        'home/products.html',
        {
            'products': products
        }
    )


def showformdata(request):

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('products')

    else:

        form = ProductForm()

    return render(
        request,
        'home/add_product.html',
        {
            'form': form
        }
    )


def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    return render(
        request,
        'home/product_detail.html',
        {
            'product': product,
            'related_products': related_products
        }
    )


def search(request):

    q = request.GET.get('q', '')

    products = Product.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(category__name__icontains=q)
    )

    return render(
        request,
        'home/search.html',
        {
            'products': products,
            'q': q
        }
    )


def categories(request):

    category_list = Category.objects.all()

    return render(
        request,
        'home/categories.html',
        {
            'categories': category_list
        }
    )


def category_products(request, category):

    selected_category = get_object_or_404(
        Category,
        name=category
    )

    products = Product.objects.filter(
        category=selected_category
    )

    return render(
        request,
        'home/category_products.html',
        {
            'products': products,
            'category': selected_category
        }
    )


def add_to_cart(request, id):

    cart = request.session.get(
        'cart',
        {}
    )

    id = str(id)

    if request.method == 'POST':

        quantity = int(
            request.POST.get(
                'quantity',
                1
            )
        )

        if quantity < 1:
            quantity = 1

        if id in cart:

            cart[id] += quantity

        else:

            cart[id] = quantity

    else:

        if id in cart:

            cart[id] += 1

        else:

            cart[id] = 1

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):

    cart_data = request.session.get(
        'cart',
        {}
    )

    products = []

    total = 0

    for id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=id
        )

        item_total = (
            product.price * quantity
        )

        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(
        request,
        'home/cart.html',
        {
            'products': products,
            'total': total
        }
    )


def remove_from_cart(request, id):

    cart = request.session.get(
        'cart',
        {}
    )

    id = str(id)

    if id in cart:

        del cart[id]

    request.session['cart'] = cart

    return redirect('cart')


def increase_quantity(request, id):

    cart = request.session.get(
        'cart',
        {}
    )

    id = str(id)

    if id in cart:

        cart[id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, id):

    cart = request.session.get(
        'cart',
        {}
    )

    id = str(id)

    if id in cart:

        cart[id] -= 1

        if cart[id] <= 0:

            del cart[id]

    request.session['cart'] = cart

    return redirect('cart')


@login_required(login_url='login')
def checkout(request):

    cart_data = request.session.get(
        'cart',
        {}
    )

    if not cart_data:

        return redirect('cart')

    products = []

    total = 0

    for id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=id
        )

        item_total = (
            product.price * quantity
        )

        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })
@login_required(login_url='login')
def buy_now(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            quantity = 1

        item_total = product.price * quantity

        products = [{
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        }]

        total = item_total

        if request.method == 'POST':
            form = CheckoutForm(initial={
                'customer_name': request.user.username,
                'email': request.user.email
            })

            if request.POST.get('customer_name'):
                form = CheckoutForm(request.POST)

                if form.is_valid():

                    order = Order.objects.create(
                        user=request.user,
                        customer_name=form.cleaned_data['customer_name'],
                        email=form.cleaned_data['email'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'],
                        total_amount=total
                    )

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )

                    return redirect(
                        'order_success',
                        order_id=order.id
                    )

        return render(request, 'home/checkout.html', {
            'products': products,
            'total': total,
            'form': form,
            'buy_now': True
        })

    return redirect('product_detail', id=id)

    if request.method == 'POST':

        form = CheckoutForm(
            request.POST
        )

        if form.is_valid():

            order = Order.objects.create(

                user=request.user,

                customer_name=form.cleaned_data[
                    'customer_name'
                ],

                email=form.cleaned_data[
                    'email'
                ],

                phone=form.cleaned_data[
                    'phone'
                ],

                address=form.cleaned_data[
                    'address'
                ],

                total_amount=total
            )

            for item in products:

                OrderItem.objects.create(

                    order=order,

                    product=item['product'],

                    quantity=item['quantity'],

                    price=item['product'].price
                )

            request.session['cart'] = {}

            return redirect(
                'order_success',
                order_id=order.id
            )

    else:

        form = CheckoutForm(
            initial={
                'customer_name': request.user.username,
                'email': request.user.email
            }
        )

    return render(
        request,
        'home/checkout.html',
        {
            'products': products,
            'total': total,
            'form': form
        }
    )


@login_required(login_url='login')
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'home/order_success.html',
        {
            'order': order
        }
    )

@login_required(login_url='login')
def buy_now_checkout(request):

    buy_now_data = request.session.get('buy_now')

    if not buy_now_data:
        return redirect('products')

    product = get_object_or_404(
        Product,
        id=buy_now_data['product_id']
    )

    quantity = buy_now_data['quantity']
    total = product.price * quantity

    products = [{
        'product': product,
        'quantity': quantity,
        'item_total': total
    }]

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = Order.objects.create(
                user=request.user,
                customer_name=form.cleaned_data['customer_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total_amount=total
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            del request.session['buy_now']

            return redirect(
                'order_success',
                order_id=order.id
            )

    else:

        form = CheckoutForm(initial={
            'customer_name': request.user.username,
            'email': request.user.email
        })

    return render(request, 'home/checkout.html', {
        'products': products,
        'total': total,
        'form': form
    })


@login_required(login_url='login')
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'home/my_orders.html',
        {
            'orders': orders
        }
    )


def signup(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'home/signup.html',
                {
                    'error':
                    'Username already exists.'
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        return redirect('home')

    return render(
        request,
        'home/signup.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            next_page = request.GET.get(
                'next'
            )

            if next_page:

                return redirect(
                    next_page
                )

            return redirect('home')

        return render(
            request,
            'home/login.html',
            {
                'error':
                'Invalid username or password.'
            }
        )

    return render(
        request,
        'home/login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('home')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Abhi message database/email mein save nahi hoga.
        # Form submit hone ke baad success page show hoga.

        return render(request, 'home/contact.html', {
            'success': 'Your message has been sent successfully!'
        })

    return render(request, 'home/contact.html')
