from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Order, OrderItem

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {'products': products, 'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {'products': products, 'categories': categories, 'selected_category': category})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'products/cart_detail.html', {'products': products, 'total': total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
    request.session['cart'] = cart
    return redirect('cart_detail')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'products/register.html', {'form': form})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    total = 0
    items_data = []
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        items_data.append({'product': product, 'quantity': quantity, 'price': product.price})

    order = Order.objects.create(user=request.user, total=total)
    for item in items_data:
        OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['price'])

    request.session['cart'] = {}
    return render(request, 'products/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/order_history.html', {'orders': orders})