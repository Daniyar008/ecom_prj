# 🎨 АРХИТЕКТУРА ФРОНТЕНДА E-COMMERCE MULTIVENDOR PLATFORM

## Оглавление
1. [Обзор архитектуры](#обзор-архитектуры)
2. [Технологический стек](#технологический-стек)
3. [Структура templates](#структура-templates)
4. [Статические файлы](#статические-файлы)
5. [JavaScript функционал](#javascript-функционал)
6. [UI/UX компоненты](#uiux-компоненты)
7. [Responsive design](#responsive-design)
8. [Интеграция с бэкендом](#интеграция-с-бэкендом)

---

## Обзор архитектуры

### Frontend Architecture Pattern: Server-Side Rendering (SSR) + Progressive Enhancement

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                                                                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │  HTML/CSS     │  │  JavaScript   │  │  AJAX/Fetch   │       │
│  │  (Rendered)   │  │  (jQuery)     │  │  (Dynamic)    │       │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘       │
└──────────┼──────────────────┼──────────────────┼────────────────┘
           │                  │                  │
           │ HTTP Request     │ Event Handlers   │ API Calls
           │                  │                  │
┌──────────▼──────────────────▼──────────────────▼────────────────┐
│                      DJANGO BACKEND                              │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Template Engine (Jinja2-style)                         │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │   │
│  │  │  base.html │  │ index.html │  │ product.   │       │   │
│  │  │  (Layout)  │  │ (Extend)   │  │ html       │       │   │
│  │  └────────────┘  └────────────┘  └────────────┘       │   │
│  │                                                          │   │
│  │  Template Tags & Filters:                               │   │
│  │  - {% url 'app:view' %}                                │   │
│  │  - {{ user.username }}                                  │   │
│  │  - {% for product in products %}                       │   │
│  │  - {{ product.price|floatformat:2 }}                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Context Processors (Global Variables)                  │   │
│  │  - categories (все категории)                          │   │
│  │  - vendors (все продавцы)                              │   │
│  │  - address (адрес текущего пользователя)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Views (Data Preparation)                               │   │
│  │  - Подготовка данных (ORM queries)                     │   │
│  │  - Пагинация                                            │   │
│  │  - Фильтрация                                           │   │
│  │  - Сериализация в context                              │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     STATIC FILES LAYER                           │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │    CSS      │  │ JavaScript  │  │   Images    │            │
│  │  - Main     │  │  - jQuery   │  │  - Logos    │            │
│  │  - Vendor   │  │  - Custom   │  │  - Products │            │
│  │  - Responsive│ │  - Plugins  │  │  - Icons    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                   │
│  Served by: WhiteNoise (Django) / Nginx (Docker)               │
└───────────────────────────────────────────────────────────────┘
```

---

## Технологический стек

### Core Technologies
| Компонент | Технология | Версия | Назначение |
|-----------|-----------|--------|------------|
| **Template Engine** | Django Templates | 4.2.7 | Server-side rendering |
| **CSS Framework** | Custom CSS + Bootstrap-like | - | Стилизация и layout |
| **JavaScript Library** | jQuery | 3.x | DOM manipulation, AJAX |
| **Icons** | Font Awesome / Custom | - | Иконки UI |
| **Image Processing** | Pillow (backend) | 10.1.0 | Обработка загруженных изображений |

### Frontend Libraries & Plugins
```html
<!-- jQuery -->
<script src="{% static 'assets/js/jquery-3.6.0.min.js' %}"></script>

<!-- Слайдер (Slick / Owl Carousel) -->
<script src="{% static 'assets/js/slick.min.js' %}"></script>

<!-- Lightbox для галереи -->
<script src="{% static 'assets/js/lightbox.min.js' %}"></script>

<!-- Select2 (для dropdowns) -->
<script src="{% static 'assets/js/select2.min.js' %}"></script>

<!-- Validation (возможно jQuery Validate) -->
<script src="{% static 'assets/js/validation.js' %}"></script>

<!-- Custom scripts -->
<script src="{% static 'assets/js/main.js' %}"></script>
<script src="{% static 'assets/js/function.js' %}"></script>
```

---

## Структура templates

### Иерархия шаблонов

```
templates/
├── partials/
│   └── base.html                  # Главный layout (header, footer, navbar)
│
├── core/                          # Шаблоны приложения core
│   ├── index.html                 # Главная страница
│   ├── category.html              # Страница категории
│   ├── product-list.html          # Каталог товаров
│   ├── product-detail.html        # Детальная страница товара
│   └── search.html                # Результаты поиска
│
├── userauths/                     # Шаблоны аутентификации
│   ├── sign-up.html               # Регистрация
│   ├── sign-in.html               # Вход
│   ├── profile.html               # Профиль пользователя
│   ├── change_password.html       # Смена пароля
│   └── dashboard.html             # Dashboard пользователя
│
├── cartorders/                    # Шаблоны заказов
│   ├── cart.html                  # Корзина
│   ├── checkout.html              # Оформление заказа
│   ├── order-list.html            # Список заказов
│   ├── order-detail.html          # Детали заказа
│   └── payment-success.html       # Успешная оплата
│
├── vendors/                       # Шаблоны vendor
│   └── vendor-profile.html        # Профиль продавца
│
├── wishlists/                     # Шаблоны избранного
│   └── wishlist.html              # Список избранного
│
└── useradmin/                     # Vendor dashboard
    ├── dashboard.html             # Панель управления vendor
    ├── product-list.html          # Товары vendor
    ├── product-create.html        # Создание товара
    ├── order-list.html            # Заказы vendor
    ├── order-detail.html          # Детали заказа vendor
    ├── reviews.html               # Отзывы на товары vendor
    ├── settings.html              # Настройки vendor
    └── transactions.html          # Финансовые транзакции
```

---

## base.html - Главный Layout

```html
<!-- templates/partials/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}MultiVendor Shop{% endblock %}</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="{% block description %}E-commerce multivendor platform{% endblock %}">
    <meta name="keywords" content="{% block keywords %}e-commerce, shop, online store{% endblock %}">
    
    <!-- Favicon -->
    <link rel="icon" href="{% static 'assets/imgs/favicon.ico' %}">
    
    <!-- CSS Files -->
    <link rel="stylesheet" href="{% static 'assets/css/main.css' %}">
    <link rel="stylesheet" href="{% static 'assets/css/vendors/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/css/plugins/slick.css' %}">
    
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Custom CSS для конкретных страниц -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- ============ HEADER ============ -->
    <header class="header">
        <div class="container">
            <!-- Top Bar -->
            <div class="header-top">
                <div class="row">
                    <div class="col-md-6">
                        <span>Welcome to MultiVendor Shop!</span>
                    </div>
                    <div class="col-md-6 text-end">
                        {% if user.is_authenticated %}
                            <a href="{% url 'userauths:profile' %}">
                                <i class="fas fa-user"></i> {{ user.username }}
                            </a>
                            <a href="{% url 'userauths:sign-out' %}">
                                <i class="fas fa-sign-out-alt"></i> Logout
                            </a>
                        {% else %}
                            <a href="{% url 'userauths:sign-in' %}">
                                <i class="fas fa-sign-in-alt"></i> Login
                            </a>
                            <a href="{% url 'userauths:sign-up' %}">
                                <i class="fas fa-user-plus"></i> Register
                            </a>
                        {% endif %}
                    </div>
                </div>
            </div>
            
            <!-- Main Header -->
            <div class="header-main">
                <div class="row align-items-center">
                    <!-- Logo -->
                    <div class="col-md-3">
                        <a href="{% url 'core:index' %}" class="logo">
                            <img src="{% static 'assets/imgs/logo.png' %}" alt="MultiVendor Shop">
                        </a>
                    </div>
                    
                    <!-- Search Bar -->
                    <div class="col-md-6">
                        <form action="{% url 'core:search' %}" method="GET" class="search-form">
                            <input type="text" name="q" placeholder="Search products..." 
                                   class="search-input" id="search-input">
                            <button type="submit" class="search-btn">
                                <i class="fas fa-search"></i>
                            </button>
                        </form>
                        
                        <!-- AJAX Search Results -->
                        <div id="search-results" class="search-dropdown" style="display: none;">
                            <!-- Динамически заполняется через AJAX -->
                        </div>
                    </div>
                    
                    <!-- Icons (Cart, Wishlist) -->
                    <div class="col-md-3 text-end">
                        <a href="{% url 'wishlists:wishlist' %}" class="icon-link">
                            <i class="fas fa-heart"></i>
                            <span class="badge">{{ wishlist_count }}</span>
                        </a>
                        <a href="{% url 'cartorders:cart' %}" class="icon-link">
                            <i class="fas fa-shopping-cart"></i>
                            <span class="badge">{{ cart_count }}</span>
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Navigation Menu -->
            <nav class="navbar">
                <ul class="nav-menu">
                    <li><a href="{% url 'core:index' %}">Home</a></li>
                    <li class="dropdown">
                        <a href="{% url 'core:product-list' %}">
                            Shop <i class="fas fa-chevron-down"></i>
                        </a>
                        <ul class="dropdown-menu">
                            {% for category in categories %}
                                <li>
                                    <a href="{% url 'core:category' category.slug %}">
                                        {{ category.title }}
                                    </a>
                                </li>
                            {% endfor %}
                        </ul>
                    </li>
                    <li><a href="{% url 'vendors:vendor-list' %}">Vendors</a></li>
                    <li><a href="{% url 'core:contact' %}">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <!-- ============ MAIN CONTENT ============ -->
    <main class="main-content">
        {% if messages %}
            <div class="container">
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
        
        <!-- Динамический контент страниц -->
        {% block content %}
        {% endblock %}
    </main>
    
    <!-- ============ FOOTER ============ -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <!-- About -->
                <div class="col-md-3">
                    <h4>About Us</h4>
                    <p>MultiVendor Shop - your trusted online marketplace.</p>
                </div>
                
                <!-- Quick Links -->
                <div class="col-md-3">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="{% url 'core:index' %}">Home</a></li>
                        <li><a href="{% url 'core:product-list' %}">Shop</a></li>
                        <li><a href="{% url 'core:about' %}">About</a></li>
                        <li><a href="{% url 'core:contact' %}">Contact</a></li>
                    </ul>
                </div>
                
                <!-- Categories -->
                <div class="col-md-3">
                    <h4>Categories</h4>
                    <ul>
                        {% for category in categories|slice:":5" %}
                            <li>
                                <a href="{% url 'core:category' category.slug %}">
                                    {{ category.title }}
                                </a>
                            </li>
                        {% endfor %}
                    </ul>
                </div>
                
                <!-- Contact Info -->
                <div class="col-md-3">
                    <h4>Contact</h4>
                    <p><i class="fas fa-map-marker-alt"></i> 123 Street, City</p>
                    <p><i class="fas fa-phone"></i> +1 234 567 890</p>
                    <p><i class="fas fa-envelope"></i> info@multivendor.com</p>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2024 MultiVendor Shop. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <!-- ============ SCRIPTS ============ -->
    <!-- jQuery -->
    <script src="{% static 'assets/js/jquery-3.6.0.min.js' %}"></script>
    
    <!-- Bootstrap -->
    <script src="{% static 'assets/js/vendors/bootstrap.bundle.min.js' %}"></script>
    
    <!-- Plugins -->
    <script src="{% static 'assets/js/plugins/slick.min.js' %}"></script>
    
    <!-- Custom Scripts -->
    <script src="{% static 'assets/js/main.js' %}"></script>
    <script src="{% static 'assets/js/function.js' %}"></script>
    
    <!-- Page-specific scripts -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## Ключевые страницы

### 1. Главная страница (index.html)

```html
<!-- templates/core/index.html -->
{% extends 'partials/base.html' %}
{% load static %}

{% block title %}Home - MultiVendor Shop{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero-section">
    <div class="container">
        <div class="hero-slider">
            <!-- Слайдер с промо-баннерами -->
            <div class="hero-slide">
                <img src="{% static 'assets/imgs/banner1.jpg' %}" alt="Banner">
                <div class="hero-caption">
                    <h1>Summer Sale 2024</h1>
                    <p>Up to 50% off on selected items</p>
                    <a href="{% url 'core:product-list' %}" class="btn btn-primary">Shop Now</a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Featured Categories -->
<section class="categories-section">
    <div class="container">
        <h2 class="section-title">Popular Categories</h2>
        <div class="row">
            {% for category in categories|slice:":8" %}
                <div class="col-md-3 col-sm-6">
                    <div class="category-card">
                        <a href="{% url 'core:category' category.slug %}">
                            <img src="{{ category.image.url }}" alt="{{ category.title }}">
                            <h3>{{ category.title }}</h3>
                            <span>{{ category.product_set.count }} products</span>
                        </a>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Featured Products -->
<section class="products-section">
    <div class="container">
        <h2 class="section-title">Featured Products</h2>
        <div class="row">
            {% for product in products %}
                <div class="col-md-3 col-sm-6">
                    {% include 'core/partials/product-card.html' with product=product %}
                </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Top Vendors -->
<section class="vendors-section">
    <div class="container">
        <h2 class="section-title">Top Vendors</h2>
        <div class="row">
            {% for vendor in vendors|slice:":4" %}
                <div class="col-md-3 col-sm-6">
                    <div class="vendor-card">
                        <a href="{% url 'vendors:vendor-detail' vendor.id %}">
                            <img src="{{ vendor.image.url }}" alt="{{ vendor.title }}">
                            <h3>{{ vendor.title }}</h3>
                            <p>{{ vendor.description|truncatewords:10 }}</p>
                        </a>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}

{% block extra_js %}
<script>
    // Инициализация слайдера
    $(document).ready(function(){
        $('.hero-slider').slick({
            autoplay: true,
            autoplaySpeed: 5000,
            arrows: true,
            dots: true
        });
    });
</script>
{% endblock %}
```

---

### 2. Product Card Component (многократно используемый)

```html
<!-- templates/core/partials/product-card.html -->
<div class="product-card">
    <div class="product-image">
        <a href="{% url 'core:product-detail' product.slug %}">
            {% if product.image %}
                <img src="{{ product.image.url }}" alt="{{ product.title }}">
            {% else %}
                <img src="{% static 'assets/imgs/no-image.jpg' %}" alt="No image">
            {% endif %}
        </a>
        
        <!-- Badges -->
        {% if product.featured %}
            <span class="badge badge-featured">Featured</span>
        {% endif %}
        {% if product.old_price and product.old_price > product.price %}
            {% widthratio product.old_price|floatformat:0|add:"0" 100 product.price|floatformat:0|add:"0" as discount %}
            <span class="badge badge-sale">-{{ discount|floatformat:0 }}%</span>
        {% endif %}
        
        <!-- Quick Actions -->
        <div class="product-actions">
            <button class="btn-icon add-to-wishlist" data-product-id="{{ product.id }}">
                <i class="far fa-heart"></i>
            </button>
            <button class="btn-icon quick-view" data-product-id="{{ product.id }}">
                <i class="fas fa-eye"></i>
            </button>
        </div>
    </div>
    
    <div class="product-info">
        <!-- Category -->
        <span class="product-category">{{ product.category.title }}</span>
        
        <!-- Title -->
        <h3 class="product-title">
            <a href="{% url 'core:product-detail' product.slug %}">
                {{ product.title|truncatewords:5 }}
            </a>
        </h3>
        
        <!-- Rating -->
        <div class="product-rating">
            {% with avg_rating=product.get_average_rating %}
                {% for i in "12345" %}
                    {% if forloop.counter <= avg_rating %}
                        <i class="fas fa-star"></i>
                    {% else %}
                        <i class="far fa-star"></i>
                    {% endif %}
                {% endfor %}
                <span class="rating-count">({{ product.review_set.count }})</span>
            {% endwith %}
        </div>
        
        <!-- Price -->
        <div class="product-price">
            <span class="price-current">${{ product.price|floatformat:2 }}</span>
            {% if product.old_price and product.old_price > product.price %}
                <span class="price-old">${{ product.old_price|floatformat:2 }}</span>
            {% endif %}
        </div>
        
        <!-- Add to Cart Button -->
        <button class="btn btn-primary btn-add-to-cart" data-product-id="{{ product.id }}">
            <i class="fas fa-shopping-cart"></i> Add to Cart
        </button>
    </div>
</div>
```

---

### 3. Детальная страница товара (product-detail.html)

```html
<!-- templates/core/product-detail.html -->
{% extends 'partials/base.html' %}
{% load static %}

{% block title %}{{ product.title }} - MultiVendor Shop{% endblock %}

{% block content %}
<div class="container product-detail-page">
    <div class="row">
        <!-- Product Images -->
        <div class="col-md-6">
            <div class="product-gallery">
                <!-- Main Image -->
                <div class="main-image">
                    <img src="{{ product.image.url }}" alt="{{ product.title }}" id="main-product-image">
                </div>
                
                <!-- Thumbnail Gallery -->
                <div class="thumbnail-gallery">
                    <img src="{{ product.image.url }}" class="thumbnail active" 
                         onclick="changeImage('{{ product.image.url }}')">
                    
                    {% for image in product.productimage_set.all %}
                        <img src="{{ image.images.url }}" class="thumbnail"
                             onclick="changeImage('{{ image.images.url }}')">
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <!-- Product Info -->
        <div class="col-md-6">
            <div class="product-details">
                <!-- Breadcrumbs -->
                <nav class="breadcrumb">
                    <a href="{% url 'core:index' %}">Home</a> /
                    <a href="{% url 'core:category' product.category.slug %}">{{ product.category.title }}</a> /
                    <span>{{ product.title }}</span>
                </nav>
                
                <!-- Title -->
                <h1 class="product-title">{{ product.title }}</h1>
                
                <!-- Rating -->
                <div class="product-rating">
                    {% with avg_rating=product.get_average_rating %}
                        <div class="stars">
                            {% for i in "12345" %}
                                {% if forloop.counter <= avg_rating %}
                                    <i class="fas fa-star"></i>
                                {% else %}
                                    <i class="far fa-star"></i>
                                {% endif %}
                            {% endfor %}
                        </div>
                        <span class="rating-text">{{ avg_rating|floatformat:1 }} ({{ reviews.count }} reviews)</span>
                    {% endwith %}
                </div>
                
                <!-- Price -->
                <div class="product-price">
                    <span class="price-current">${{ product.price|floatformat:2 }}</span>
                    {% if product.old_price and product.old_price > product.price %}
                        <span class="price-old">${{ product.old_price|floatformat:2 }}</span>
                        {% widthratio product.old_price|floatformat:0|add:"0" 100 product.price|floatformat:0|add:"0" as discount %}
                        <span class="discount-badge">Save {{ discount|floatformat:0 }}%</span>
                    {% endif %}
                </div>
                
                <!-- Stock Status -->
                <div class="stock-status">
                    {% if product.in_stock %}
                        <span class="in-stock"><i class="fas fa-check-circle"></i> In Stock</span>
                    {% else %}
                        <span class="out-of-stock"><i class="fas fa-times-circle"></i> Out of Stock</span>
                    {% endif %}
                </div>
                
                <!-- Description -->
                <div class="product-description">
                    <p>{{ product.description|linebreaks }}</p>
                </div>
                
                <!-- Vendor Info -->
                <div class="vendor-info">
                    <span>Sold by: </span>
                    <a href="{% url 'vendors:vendor-detail' product.vendor.id %}">
                        <strong>{{ product.vendor.title }}</strong>
                    </a>
                </div>
                
                <!-- Add to Cart Form -->
                <form class="add-to-cart-form" method="POST" action="{% url 'cartorders:add-to-cart' product.id %}">
                    {% csrf_token %}
                    
                    <!-- Quantity Selector -->
                    <div class="quantity-selector">
                        <label>Quantity:</label>
                        <button type="button" class="qty-btn" onclick="decreaseQty()">-</button>
                        <input type="number" name="quantity" id="quantity" value="1" min="1" max="{{ product.in_stock }}">
                        <button type="button" class="qty-btn" onclick="increaseQty()">+</button>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="action-buttons">
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-shopping-cart"></i> Add to Cart
                        </button>
                        <button type="button" class="btn btn-outline-secondary btn-lg add-to-wishlist" 
                                data-product-id="{{ product.id }}">
                            <i class="far fa-heart"></i> Wishlist
                        </button>
                    </div>
                </form>
                
                <!-- Tags -->
                {% if product.tags.all %}
                    <div class="product-tags">
                        <strong>Tags:</strong>
                        {% for tag in product.tags.all %}
                            <a href="{% url 'core:tag' tag.slug %}" class="tag">{{ tag.name }}</a>
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Tabs (Specifications, Reviews) -->
    <div class="product-tabs">
        <ul class="nav nav-tabs">
            <li class="nav-item">
                <a class="nav-link active" data-toggle="tab" href="#specifications">Specifications</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="tab" href="#reviews">Reviews ({{ reviews.count }})</a>
            </li>
        </ul>
        
        <div class="tab-content">
            <!-- Specifications Tab -->
            <div id="specifications" class="tab-pane active">
                <div class="specifications-content">
                    {{ product.specifications|safe }}
                </div>
            </div>
            
            <!-- Reviews Tab -->
            <div id="reviews" class="tab-pane">
                <!-- Reviews List -->
                <div class="reviews-list">
                    {% for review in reviews %}
                        <div class="review-item">
                            <div class="review-header">
                                <strong>{{ review.user.username }}</strong>
                                <div class="review-rating">
                                    {% for i in "12345" %}
                                        {% if forloop.counter <= review.rating %}
                                            <i class="fas fa-star"></i>
                                        {% else %}
                                            <i class="far fa-star"></i>
                                        {% endif %}
                                    {% endfor %}
                                </div>
                                <span class="review-date">{{ review.date|date:"M d, Y" }}</span>
                            </div>
                            <div class="review-body">
                                <p>{{ review.review }}</p>
                            </div>
                        </div>
                    {% empty %}
                        <p>No reviews yet. Be the first to review this product!</p>
                    {% endfor %}
                </div>
                
                <!-- Add Review Form -->
                {% if user.is_authenticated %}
                    <div class="add-review-form">
                        <h3>Write a Review</h3>
                        <form method="POST" action="{% url 'core:add-review' product.id %}">
                            {% csrf_token %}
                            
                            <div class="form-group">
                                <label>Rating:</label>
                                <div class="rating-input">
                                    <input type="radio" name="rating" value="5" id="star5">
                                    <label for="star5"><i class="fas fa-star"></i></label>
                                    <input type="radio" name="rating" value="4" id="star4">
                                    <label for="star4"><i class="fas fa-star"></i></label>
                                    <input type="radio" name="rating" value="3" id="star3">
                                    <label for="star3"><i class="fas fa-star"></i></label>
                                    <input type="radio" name="rating" value="2" id="star2">
                                    <label for="star2"><i class="fas fa-star"></i></label>
                                    <input type="radio" name="rating" value="1" id="star1">
                                    <label for="star1"><i class="fas fa-star"></i></label>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>Your Review:</label>
                                <textarea name="review" rows="5" required></textarea>
                            </div>
                            
                            <button type="submit" class="btn btn-primary">Submit Review</button>
                        </form>
                    </div>
                {% else %}
                    <p><a href="{% url 'userauths:sign-in' %}">Login</a> to write a review.</p>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Related Products -->
    <div class="related-products">
        <h2 class="section-title">Related Products</h2>
        <div class="row">
            {% for related_product in related_products %}
                <div class="col-md-3 col-sm-6">
                    {% include 'core/partials/product-card.html' with product=related_product %}
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Смена главного изображения
    function changeImage(imageUrl) {
        document.getElementById('main-product-image').src = imageUrl;
        
        // Убираем active class у всех thumbnails
        document.querySelectorAll('.thumbnail').forEach(thumb => {
            thumb.classList.remove('active');
        });
        
        // Добавляем active class к выбранному
        event.target.classList.add('active');
    }
    
    // Количество
    function increaseQty() {
        const input = document.getElementById('quantity');
        const max = parseInt(input.getAttribute('max'));
        if (parseInt(input.value) < max) {
            input.value = parseInt(input.value) + 1;
        }
    }
    
    function decreaseQty() {
        const input = document.getElementById('quantity');
        if (parseInt(input.value) > 1) {
            input.value = parseInt(input.value) - 1;
        }
    }
</script>
{% endblock %}
```

---

## Статические файлы

### Структура static/

```
static/
├── assets/
│   ├── css/
│   │   ├── main.css              # Главные стили
│   │   ├── responsive.css        # Media queries
│   │   ├── vendors/              # Vendor CSS (Bootstrap, etc.)
│   │   └── plugins/              # Plugin styles (slick, lightbox)
│   │
│   ├── js/
│   │   ├── jquery-3.6.0.min.js   # jQuery
│   │   ├── main.js               # Главные скрипты
│   │   ├── function.js           # Вспомогательные функции
│   │   ├── vendors/              # Vendor JS (Bootstrap, etc.)
│   │   └── plugins/              # Plugin scripts
│   │
│   ├── imgs/
│   │   ├── logo.png              # Логотип
│   │   ├── favicon.ico           # Иконка сайта
│   │   ├── no-image.jpg          # Placeholder для товаров без фото
│   │   ├── banners/              # Баннеры для главной
│   │   └── categories/           # Изображения категорий
│   │
│   ├── fonts/                    # Шрифты
│   │   └── ...
│   │
│   └── sass/                     # SASS/SCSS исходники (если используются)
│       ├── _variables.scss
│       ├── _mixins.scss
│       ├── _layout.scss
│       └── main.scss
│
└── assets2/                      # Альтернативная тема (если есть)
    └── ...
```

---

## JavaScript функционал

### main.js - Основные функции

```javascript
// static/assets/js/main.js

$(document).ready(function() {
    
    // ==================== SEARCH ====================
    // AJAX поиск
    $('#search-input').on('keyup', function() {
        const query = $(this).val();
        
        if (query.length >= 3) {
            $.ajax({
                url: '/search/',
                data: { 'q': query },
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                success: function(data) {
                    displaySearchResults(data.products);
                }
            });
        } else {
            $('#search-results').hide();
        }
    });
    
    function displaySearchResults(products) {
        const resultsDiv = $('#search-results');
        resultsDiv.empty();
        
        if (products.length > 0) {
            products.forEach(product => {
                resultsDiv.append(`
                    <div class="search-result-item">
                        <img src="${product.image}" alt="${product.title}">
                        <div class="result-info">
                            <a href="/product/${product.id}/">${product.title}</a>
                            <span class="result-price">$${product.price}</span>
                        </div>
                    </div>
                `);
            });
            resultsDiv.show();
        } else {
            resultsDiv.html('<p>No results found</p>').show();
        }
    }
    
    // Закрыть поиск при клике вне
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.search-form, #search-results').length) {
            $('#search-results').hide();
        }
    });
    
    
    // ==================== ADD TO CART ====================
    $('.btn-add-to-cart').on('click', function(e) {
        e.preventDefault();
        
        const productId = $(this).data('product-id');
        const button = $(this);
        
        $.ajax({
            url: `/cart/add/${productId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Обновляем счетчик корзины
                updateCartCount();
                
                // Показываем уведомление
                showNotification('Product added to cart!', 'success');
                
                // Меняем иконку кнопки
                button.html('<i class="fas fa-check"></i> Added');
                button.addClass('btn-success');
                
                setTimeout(() => {
                    button.html('<i class="fas fa-shopping-cart"></i> Add to Cart');
                    button.removeClass('btn-success');
                }, 2000);
            },
            error: function() {
                showNotification('Failed to add product to cart', 'error');
            }
        });
    });
    
    
    // ==================== ADD TO WISHLIST ====================
    $('.add-to-wishlist').on('click', function(e) {
        e.preventDefault();
        
        const productId = $(this).data('product-id');
        const button = $(this);
        
        $.ajax({
            url: `/wishlist/add/${productId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                updateWishlistCount();
                showNotification('Added to wishlist!', 'success');
                
                // Меняем иконку
                button.find('i').removeClass('far').addClass('fas');
            },
            error: function() {
                showNotification('Failed to add to wishlist', 'error');
            }
        });
    });
    
    
    // ==================== PRODUCT FILTERS ====================
    // Фильтр по цене
    $('#price-filter-form').on('submit', function(e) {
        e.preventDefault();
        
        const minPrice = $('#min-price').val();
        const maxPrice = $('#max-price').val();
        const category = $('#category-filter').val();
        
        let url = '/products/?';
        if (minPrice) url += `min_price=${minPrice}&`;
        if (maxPrice) url += `max_price=${maxPrice}&`;
        if (category) url += `category=${category}&`;
        
        window.location.href = url;
    });
    
    
    // ==================== UTILITIES ====================
    // Получить CSRF token из cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Обновить счетчик корзины
    function updateCartCount() {
        $.ajax({
            url: '/cart/count/',
            success: function(data) {
                $('.icon-link .badge').text(data.count);
            }
        });
    }
    
    // Обновить счетчик wishlist
    function updateWishlistCount() {
        $.ajax({
            url: '/wishlist/count/',
            success: function(data) {
                $('.icon-link .badge').eq(0).text(data.count);
            }
        });
    }
    
    // Показать уведомление
    function showNotification(message, type) {
        const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        const notification = $(`
            <div class="alert ${alertClass} alert-dismissible fade show notification">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').prepend(notification);
        
        setTimeout(() => {
            notification.alert('close');
        }, 3000);
    }
    
    
    // ==================== SLIDERS ====================
    // Инициализация слайдера товаров
    $('.product-slider').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        arrows: true,
        dots: false,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });
    
});
```

---

## UI/UX компоненты

### Ключевые компоненты интерфейса

1. **Navigation Menu** (Dropdown navigation с категориями)
2. **Product Card** (Карточка товара с изображением, ценой, рейтингом)
3. **Search Bar** (Поиск с автодополнением AJAX)
4. **Shopping Cart Icon** (С счетчиком товаров)
5. **Wishlist Icon** (С счетчиком избранного)
6. **Breadcrumbs** (Навигационная цепочка)
7. **Alert Messages** (Success/Error уведомления)
8. **Product Gallery** (Галерея изображений с thumbnails)
9. **Rating Stars** (Визуализация рейтинга)
10. **Add to Cart Button** (С loading state)
11. **Quantity Selector** (+/- controls)
12. **Filters** (Боковая панель фильтров)
13. **Pagination** (Пагинация результатов)
14. **Modal Windows** (Quick view, confirmation dialogs)
15. **Tabs** (Specifications, Reviews)

### Responsive Breakpoints

```css
/* responsive.css */

/* Extra small devices (phones, less than 576px) */
@media (max-width: 575.98px) {
    .container { padding: 0 15px; }
    .product-card { width: 100%; }
    .nav-menu { display: none; }
    .mobile-menu-toggle { display: block; }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) and (max-width: 767.98px) {
    .product-card { width: 48%; }
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) and (max-width: 991.98px) {
    .product-card { width: 32%; }
    .nav-menu { display: flex; }
}

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) and (max-width: 1199.98px) {
    .container { max-width: 960px; }
}

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
    .container { max-width: 1140px; }
}
```

---

## Интеграция с бэкендом

### Django Template Tags & Filters

```django
{# Вывод переменных #}
{{ variable }}
{{ variable|filter }}
{{ variable|filter:"argument" }}

{# URL routing #}
{% url 'app:view_name' %}
{% url 'app:view_name' arg1 arg2 %}

{# Static files #}
{% load static %}
{% static 'path/to/file.css' %}

{# Условия #}
{% if condition %}
    ...
{% elif other_condition %}
    ...
{% else %}
    ...
{% endif %}

{# Циклы #}
{% for item in items %}
    {{ item }}
{% empty %}
    <p>No items</p>
{% endfor %}

{# Include #}
{% include 'partials/component.html' with var=value %}

{# Filters #}
{{ value|default:"N/A" }}
{{ text|truncatewords:10 }}
{{ number|floatformat:2 }}
{{ date|date:"M d, Y" }}
{{ html|safe }}
{{ text|linebreaks }}
{{ list|slice:":5" }}
```

### CSRF Protection в AJAX

```javascript
// Все POST/PUT/DELETE запросы должны включать CSRF token

// Способ 1: Из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajax({
    url: '/cart/add/',
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken')
    },
    data: { product_id: 123 }
});


// Способ 2: Из hidden input в форме
const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

$.ajax({
    url: '/cart/add/',
    method: 'POST',
    headers: {
        'X-CSRFToken': csrfToken
    },
    data: { product_id: 123 }
});
```

---

## Performance Optimization

### Lazy Loading Images

```html
<!-- Используем data-src вместо src -->
<img data-src="{{ product.image.url }}" alt="{{ product.title }}" class="lazy">

<script>
// Intersection Observer для lazy loading
document.addEventListener("DOMContentLoaded", function() {
    const lazyImages = document.querySelectorAll('img.lazy');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
});
</script>
```

### Asset Minification

```python
# settings.py (production)

# Minify and compress static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Enable GZip compression
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # Первым
    # ...
]
```

---

## Заключение

Фронтенд построен на:
- ✅ **Django Templates (SSR)** для основного рендеринга
- ✅ **jQuery** для DOM manipulation и AJAX
- ✅ **Custom CSS** + Bootstrap-like grid
- ✅ **Progressive Enhancement** (работает без JS)
- ✅ **Responsive Design** (mobile-first)
- ✅ **AJAX** для динамического контента (search, cart, wishlist)
- ✅ **Template inheritance** для DRY
- ✅ **Reusable components** (product card, etc.)
- ✅ **Performance optimizations** (lazy loading, minification)
- ✅ **Security** (CSRF protection, XSS prevention)

Следующие документы:
- INTEGRATION_WORKFLOW.md
- USE_CASE_DIAGRAMS.md
- PROJECT_REPORT.md
