from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


def mapa(request):
    # Coordenadas predeterminadas
    lat_default = 28.6408325  # Reemplaza con tu latitud
    lon_default = -106.1485902  # Reemplaza con tu longitud
    
    lat = lat_default
    lon = lon_default

    if request.method == 'POST':
        try:
            lat = float(request.POST.get('lat', lat_default))
            lon = float(request.POST.get('lon', lon_default))
            
            # Validar rango de coordenadas
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError("Coordenadas fuera de rango")
                
        except (ValueError, TypeError):
            # Restablecer a valores por defecto en caso de error
            lat = lat_default
            lon = lon_default

    return render(request, 'map.html', {
        'lat': lat,
        'lon': lon
    })

    context = {
        'lat': lat,
        'lon': lon
    }
    return render(request, 'map.html', context)


#INICIO DE SESION Y REGISTRO
# shop/views.py
# ... (tus imports existentes)
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm  # Asegúrate de importar tus formularios
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm  # ¡Importación clave!
from .forms import RegisterForm  # Asegúrate de importar tu RegisterForm

# ... (tus otras vistas existentes)

# Vistas de autenticación
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:product_list')  # Redirige a la lista de productos
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop:product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('shop:product_list')