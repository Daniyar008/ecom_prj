# 🏗️ АРХИТЕКТУРА БЭКЕНДА E-COMMERCE MULTIVENDOR PLATFORM

## Оглавление
1. [Обзор архитектуры](#обзор-архитектуры)
2. [Технологический стек](#технологический-стек)
3. [Структура Django приложений](#структура-django-приложений)
4. [Модели данных](#модели-данных)
5. [API и представления](#api-и-представления)
6. [Бизнес-логика](#бизнес-логика)
7. [Асинхронные задачи](#асинхронные-задачи)
8. [Безопасность](#безопасность)
9. [Оптимизация и кеширование](#оптимизация-и-кеширование)

---

## Обзор архитектуры

### Архитектурный стиль: Монолитная MVC (MTV в Django)

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  (Browser: HTML/CSS/JavaScript + Templates + AJAX requests)     │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/HTTPS
┌─────────────────────────▼───────────────────────────────────────┐
│                      PRESENTATION LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐           │
│  │   Views     │  │  Templates  │  │  URL Router  │           │
│  │ (Django)    │  │  (Jinja2)   │  │  (urls.py)   │           │
│  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘           │
└─────────┼─────────────────┼─────────────────┼──────────────────┘
          │                 │                 │
┌─────────▼─────────────────▼─────────────────▼──────────────────┐
│                    BUSINESS LOGIC LAYER                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Django Applications (Apps)                             │   │
│  │  ┌──────┐ ┌─────────┐ ┌────────┐ ┌──────┐ ┌─────────┐ │   │
│  │  │ core │ │  goods  │ │vendors │ │orders│ │userauths│ │   │
│  │  └──────┘ └─────────┘ └────────┘ └──────┘ └─────────┘ │   │
│  │  ┌──────────┐ ┌──────────┐                             │   │
│  │  │wishlists │ │useradmin │                             │   │
│  │  └──────────┘ └──────────┘                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Forms & Validators                                     │   │
│  │  - UserLoginForm, UserRegisterForm                      │   │
│  │  - ProductForm, ReviewForm                              │   │
│  │  - Custom validators для email, цен, изображений       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Authentication & Authorization                         │   │
│  │  - EmailBackend (custom authentication)                │   │
│  │  - Permission classes для vendors, admin               │   │
│  │  - Decorators (@login_required, @vendor_required)      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Context Processors                                     │   │
│  │  - default() - категории, vendors, address            │   │
│  │  - Глобальные переменные для всех templates           │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                      DATA ACCESS LAYER                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Django ORM (Object-Relational Mapping)                 │   │
│  │  - QuerySets для сложных запросов                       │   │
│  │  - select_related() / prefetch_related() оптимизация   │   │
│  │  - Aggregation (Sum, Avg, Count)                       │   │
│  │  - Signals (post_save, pre_save для Profile, Order)   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Models (Django Models)                                 │   │
│  │  - 10+ моделей с связями (ForeignKey, ManyToMany)     │   │
│  │  - Методы модели (get_total, save overrides)          │   │
│  │  - Properties для вычисляемых полей                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                     PERSISTENCE LAYER                            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │   PostgreSQL     │  │   Redis Cache    │  │  Static Files│ │
│  │   (Supabase)     │  │   (Optional)     │  │  (WhiteNoise)│ │
│  │   - Users        │  │   - Sessions     │  │  - CSS/JS    │ │
│  │   - Products     │  │   - Cart data    │  │  - Images    │ │
│  │   - Orders       │  │   - Categories   │  │  - Fonts     │ │
│  │   - Reviews      │  │   - Queries      │  │              │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    BACKGROUND TASKS LAYER                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Celery (Distributed Task Queue)                        │   │
│  │  - EAGER mode (synchronous, free)                      │   │
│  │  - Redis as broker                                      │   │
│  │  - Tasks: email sending, order processing, reports     │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Технологический стек

### Core Technologies
| Компонент | Технология | Версия | Назначение |
|-----------|-----------|--------|------------|
| **Backend Framework** | Django | 4.2.7 | Web framework MVC/MTV |
| **Language** | Python | 3.11.0 | Язык программирования |
| **WSGI Server** | Gunicorn | 21.2.0 | Production server |
| **Database** | PostgreSQL | 15.x | Основная БД (Supabase) |
| **ORM** | Django ORM | 4.2.7 | Object-relational mapping |
| **Cache** | Redis | 7.x | Кеширование (optional) |
| **Task Queue** | Celery | 5.3.4 | Асинхронные задачи |
| **Message Broker** | Redis | 7.x | Celery broker |
| **Static Files** | WhiteNoise | 6.6.0 | Статические файлы |

### Security & Authentication
| Компонент | Технология | Назначение |
|-----------|-----------|------------|
| **Authentication** | Django Auth + Custom Backend | Email/Username login |
| **Password Hashing** | PBKDF2 SHA256 | Безопасное хранение паролей |
| **CSRF Protection** | Django Middleware | Защита от CSRF атак |
| **Session Management** | Django Sessions + Redis | Управление сессиями |

### Additional Libraries
```python
# requirements.txt key packages
django==4.2.7
psycopg2-binary==2.9.9      # PostgreSQL adapter
celery==5.3.4               # Task queue
django-celery-results==2.5.1
redis==5.0.1                # Cache & broker
django-redis==5.4.0         # Django Redis integration
gunicorn==21.2.0            # WSGI server
whitenoise==6.6.0           # Static files
Pillow==10.1.0              # Image processing
django-taggit==5.0.1        # Tags для products
shortuuid==1.0.11           # Short unique IDs
django-jazzmin==2.6.0       # Admin UI
```

---

## Структура Django приложений

### 1. **core** - Главное приложение
```
core/
├── models.py          # Category, Product, ProductImage, Review, Tax, Coupon
├── views.py           # Главная страница, каталог, поиск, фильтры
├── urls.py            # URL маршруты для core
├── context_processor.py  # Глобальные переменные (категории, vendors)
├── admin.py           # Регистрация моделей в admin
└── templates/core/    # Шаблоны (index, category, search, product_detail)
```

**Основные функции:**
- Каталог товаров с фильтрами (цена, категория, бренд)
- Поиск по товарам (AJAX search)
- Детальная страница товара с отзывами
- Система категорий
- Теги для товаров (django-taggit)

**Ключевые модели:**
- `Category` - категории товаров (parent/child иерархия)
- `Product` - товары (связь с vendor, category, tags)
- `ProductImage` - галерея изображений товара (ForeignKey to Product)
- `Review` - отзывы с рейтингом (ForeignKey to Product, User)
- `Tax` - налоги по странам/регионам
- `Coupon` - промокоды со скидками

---

### 2. **userauths** - Аутентификация и профиль
```
userauths/
├── models.py          # User (custom), Profile, ContactUs
├── views.py           # register, login, logout, profile
├── forms.py           # UserRegisterForm, UserLoginForm (custom)
├── backends.py        # EmailBackend (custom authentication)
├── urls.py            # /user/sign-up, /user/sign-in, /user/profile
├── admin.py           # User management
└── templates/userauths/
```

**Основные функции:**
- Регистрация пользователей (email + username)
- Вход (email ИЛИ username + password)
- Кастомная аутентификация через EmailBackend
- Профиль пользователя с адресом и био
- Форма обратной связи (ContactUs)

**Ключевые модели:**
- `User` (custom) - расширенная модель пользователя
  - `email` (unique) - основной идентификатор
  - `username` - дополнительный идентификатор
  - `bio` - биография
- `Profile` - профиль пользователя (OneToOne с User)
  - `image` - аватар
  - `address`, `country`, `city` - адрес доставки
  - `verified` - статус верификации
- `ContactUs` - обращения пользователей

**Custom Backend:**
```python
class EmailBackend(ModelBackend):
    """Позволяет входить через email ИЛИ username"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Пытаемся найти по email (case-insensitive)
        # Если не найден - пытаемся по username
        # Возвращаем User если пароль верный
```

---

### 3. **vendors** - Продавцы/Магазины
```
vendors/
├── models.py          # Vendor
├── views.py           # Vendor profile, vendor products
├── urls.py            # /vendor/<int:id>, /vendor/<int:id>/products
├── admin.py           # Vendor management
└── templates/vendors/
```

**Основные функции:**
- Профиль продавца с описанием и изображением
- Список товаров конкретного vendor
- Контактная информация vendor

**Ключевые модели:**
- `Vendor` - продавцы/магазины
  - `title` - название магазина
  - `image` - логотип
  - `description` - описание
  - `address`, `contact`, `mobile` - контакты
  - `user` - связь с User (ForeignKey)
  - `verified` - статус верификации

---

### 4. **goods** - Дополнительные товары (?)
```
goods/
├── models.py          # Возможно дублирует core.Product
├── views.py           # Управление товарами
├── forms.py           # Формы для создания/редактирования
├── urls.py            # CRUD для goods
└── templates/goods/
```

**Назначение:** Альтернативное/дополнительное приложение для товаров

---

### 5. **cartorders** - Корзина и заказы
```
cartorders/
├── models.py          # CartOrder, CartOrderItem
├── views.py           # add_to_cart, checkout, order_list, order_detail
├── urls.py            # /cart, /checkout, /orders
├── admin.py           # Order management
└── templates/cartorders/
```

**Основные функции:**
- Добавление товаров в корзину
- Оформление заказа (checkout)
- История заказов
- Детальная страница заказа
- Обработка статусов заказов

**Ключевые модели:**
- `CartOrder` - заказы
  - `user` - покупатель (ForeignKey)
  - `price` - общая сумма
  - `paid_status` - статус оплаты
  - `order_date` - дата заказа
  - `product_status` - статус доставки
  - `oid` - уникальный ID заказа (shortuuid)
  
- `CartOrderItem` - товары в заказе
  - `order` - связь с CartOrder (ForeignKey)
  - `product` - товар (ForeignKey)
  - `qty` - количество
  - `price` - цена
  - `total` - сумма (qty * price)
  - `vendor` - продавец (ForeignKey)

**Workflow заказа:**
```python
# 1. Пользователь добавляет товар в корзину (session/DB)
# 2. Переход на checkout
# 3. Создание CartOrder + CartOrderItem(s)
# 4. Обработка оплаты (если подключен payment gateway)
# 5. Обновление статусов (paid_status, product_status)
# 6. Отправка email (через Celery task)
```

---

### 6. **wishlists** - Избранное
```
wishlists/
├── models.py          # Wishlist
├── views.py           # add_to_wishlist, remove_from_wishlist, wishlist_view
├── urls.py            # /wishlist, /wishlist/add/<int:id>
└── templates/wishlists/
```

**Основные функции:**
- Добавление товаров в избранное
- Просмотр списка избранного
- Удаление из избранного

**Ключевые модели:**
- `Wishlist` - избранные товары
  - `user` - пользователь (ForeignKey)
  - `product` - товар (ForeignKey)
  - `date` - дата добавления

---

### 7. **useradmin** - Панель управления продавцом
```
useradmin/
├── models.py          # Возможно пустой (использует модели из других apps)
├── views.py           # Dashboard для vendor (orders, products, analytics)
├── forms.py           # Формы для vendor панели
├── decorators.py      # @vendor_required decorator
├── urls.py            # /vendor/dashboard, /vendor/products, /vendor/orders
└── templates/useradmin/
```

**Основные функции:**
- Dashboard vendor с аналитикой (продажи, заказы)
- Управление товарами vendor
- Просмотр заказов vendor
- Статистика по продажам

**Decorators:**
```python
@vendor_required
def vendor_dashboard(request):
    """Доступно только продавцам"""
    pass
```

---

## Модели данных

### Полная ERD (Entity Relationship Diagram)

```
┌─────────────────────┐
│       User          │
│ ─────────────────── │
│ PK: id              │
│ UK: email           │◄──────────┐
│ UK: username        │           │ 1:1
│     password        │           │
│     bio             │           │
│     is_active       │           │
│     is_staff        │           │
└──────┬──────────────┘           │
       │ 1:Many                   │
       │                          │
┌──────▼──────────────┐  ┌────────┴────────────┐
│      Profile        │  │      Vendor         │
│ ─────────────────── │  │ ──────────────────  │
│ PK: id              │  │ PK: id              │
│ FK: user_id         │  │ FK: user_id         │
│     image           │  │     title           │
│     address         │  │     image           │
│     country         │  │     description     │
│     city            │  │     address         │
│     verified        │  │     contact         │
└─────────────────────┘  │     verified        │
                         └──────┬──────────────┘
                                │ 1:Many
                                │
┌─────────────────────┐  ┌──────▼──────────────┐
│     Category        │  │      Product        │
│ ─────────────────── │  │ ──────────────────  │
│ PK: id              │  │ PK: id              │
│     title           │◄─┤ FK: category_id     │
│     image           │1 │ FK: user_id         │
│     parent_id (FK)  │: │ FK: vendor_id       │
└─────────────────────┘M │     title           │
                         │     image           │
                         │     description     │
                         │     price           │
       ┌─────────────────┤     old_price       │
       │                 │     specifications  │
       │ 1:Many          │     product_status  │
       │                 │     status          │
┌──────▼──────────────┐  │     in_stock        │
│  ProductImage       │  │     featured        │
│ ─────────────────── │  │     digital         │
│ PK: id              │  │     sku             │
│ FK: product_id      │  │     mfd (date)      │
│     images          │  │     tags (TagField) │
│     date            │  └──────┬──────────────┘
└─────────────────────┘         │
                                │ 1:Many
    ┌───────────────────────────┼───────────────────────┐
    │                           │                       │
┌───▼──────────────┐  ┌─────────▼────────┐  ┌──────────▼─────────┐
│     Review       │  │   CartOrderItem  │  │      Wishlist      │
│ ──────────────── │  │ ──────────────── │  │ ─────────────────  │
│ PK: id           │  │ PK: id           │  │ PK: id             │
│ FK: user_id      │  │ FK: order_id     │  │ FK: user_id        │
│ FK: product_id   │  │ FK: product_id   │  │ FK: product_id     │
│     review       │  │ FK: vendor_id    │  │     date           │
│     rating       │  │     qty          │  └────────────────────┘
│     date         │  │     price        │
└──────────────────┘  │     total        │
                      │     image        │
                      └─────────┬────────┘
                                │ Many:1
                                │
                      ┌─────────▼────────┐
                      │    CartOrder     │
                      │ ──────────────── │
                      │ PK: id           │
                      │ FK: user_id      │
                      │     price        │
                      │     paid_status  │
                      │     order_date   │
                      │     product_status│
                      │     oid (UUID)   │
                      │     stripe_payment_intent│
                      └──────────────────┘

┌─────────────────────┐  ┌─────────────────────┐
│       Tax           │  │      Coupon         │
│ ─────────────────── │  │ ──────────────────  │
│ PK: id              │  │ PK: id              │
│     country         │  │     code            │
│     rate            │  │     discount        │
│     active          │  │     active          │
└─────────────────────┘  └─────────────────────┘

┌─────────────────────┐
│     ContactUs       │
│ ─────────────────── │
│ PK: id              │
│     full_name       │
│     email           │
│     phone           │
│     subject         │
│     message         │
└─────────────────────┘
```

### Связи между таблицами

#### 1:1 Relationships (One-to-One)
```python
# User ←→ Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
```

#### 1:Many Relationships (One-to-Many / ForeignKey)
```python
# User → Products (один user создает много products)
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

# User → Vendor (один user может иметь один vendor, но технически FK)
class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

# Vendor → Products (один vendor продает много products)
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

# Category → Products (одна категория содержит много products)
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

# Product → ProductImages (один product имеет много изображений)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

# Product → Reviews (один product имеет много отзывов)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# CartOrder → CartOrderItems (один заказ содержит много товаров)
class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
```

#### Many:Many Relationships (через промежуточную таблицу)
```python
# User ←→ Products (через Wishlist)
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Эта модель служит промежуточной таблицей для Many:Many

# Product ←→ Tags (через django-taggit)
class Product(models.Model):
    tags = TaggableManager()
    # TaggableManager автоматически создает промежуточную таблицу
```

---

## API и представления

### URL Structure (Routing)

```python
# ecomprj/urls.py (главный router)
urlpatterns = [
    path('admin/', admin.site.urls),                    # Django Admin
    path('', include('core.urls')),                     # Главная, каталог
    path('user/', include('userauths.urls')),           # Аутентификация
    path('vendor/', include('vendors.urls')),           # Vendor профили
    path('cart/', include('cartorders.urls')),          # Корзина и заказы
    path('wishlist/', include('wishlists.urls')),       # Избранное
    path('dashboard/', include('useradmin.urls')),      # Vendor dashboard
]
```

### Core App Views (core/views.py)

```python
# Главная страница
def index(request):
    """
    GET /
    - Выводит featured products
    - Последние товары
    - Категории
    """
    products = Product.objects.filter(featured=True, status="published")[:10]
    context = {"products": products}
    return render(request, "core/index.html", context)


# Каталог товаров
def product_list_view(request):
    """
    GET /products/
    GET /products/?category=electronics&min_price=100&max_price=1000
    - Фильтрация по категориям
    - Фильтрация по цене (min_price, max_price)
    - Фильтрация по vendor
    - Pagination
    """
    products = Product.objects.filter(status="published")
    
    # Фильтр по категории
    if category_slug := request.GET.get('category'):
        products = products.filter(category__slug=category_slug)
    
    # Фильтр по цене
    if min_price := request.GET.get('min_price'):
        products = products.filter(price__gte=min_price)
    if max_price := request.GET.get('max_price'):
        products = products.filter(price__lte=max_price)
    
    # Фильтр по vendor
    if vendor_id := request.GET.get('vendor'):
        products = products.filter(vendor_id=vendor_id)
    
    return render(request, "core/product_list.html", {"products": products})


# Детальная страница товара
def product_detail_view(request, slug):
    """
    GET /product/<slug>/
    - Детали товара
    - Галерея изображений
    - Отзывы с пагинацией
    - Похожие товары (related products)
    - Форма добавления в корзину
    """
    product = get_object_or_404(Product, slug=slug, status="published")
    
    # Отзывы с оптимизацией
    reviews = Review.objects.filter(product=product).select_related('user')
    
    # Похожие товары из той же категории
    related_products = Product.objects.filter(
        category=product.category,
        status="published"
    ).exclude(id=product.id)[:4]
    
    # Средний рейтинг
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        "product": product,
        "reviews": reviews,
        "related_products": related_products,
        "avg_rating": avg_rating
    }
    return render(request, "core/product_detail.html", context)


# AJAX поиск
def search_view(request):
    """
    GET /search/?q=laptop
    - Полнотекстовый поиск по названию и описанию
    - Возвращает JSON для AJAX или HTML
    """
    query = request.GET.get('q', '')
    
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        status="published"
    )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX запрос - возвращаем JSON
        data = list(products.values('id', 'title', 'price', 'image'))
        return JsonResponse({"products": data})
    
    return render(request, "core/search.html", {"products": products, "query": query})


# Категория
def category_view(request, slug):
    """
    GET /category/<slug>/
    - Товары конкретной категории
    - Subcategories (если есть дочерние)
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, status="published")
    
    return render(request, "core/category.html", {
        "category": category,
        "products": products
    })
```

### UserAuths App Views (userauths/views.py)

```python
def register_view(request):
    """
    GET /user/sign-up/ - форма регистрации
    POST /user/sign-up/ - обработка регистрации
    
    Workflow:
    1. Валидация формы (UserRegisterForm)
    2. Создание User
    3. Создание Profile (через signal post_save)
    4. Автоматический вход (login)
    5. Редирект на dashboard
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                new_user = form.save()
                # Profile создается автоматически через signal
                
                # Автоматический вход
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                
                messages.success(request, "Registration successful!")
                return redirect('core:index')
            except Exception as e:
                logger.error(f"Registration error: {e}")
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            # Показываем ошибки валидации
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    
    return render(request, 'userauths/sign-up.html', {'form': form})


def login_view(request):
    """
    GET /user/sign-in/ - форма входа
    POST /user/sign-in/ - обработка входа
    
    Использует кастомный EmailBackend:
    - Можно войти через email
    - Можно войти через username
    - Email case-insensitive
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # EmailBackend автоматически проверяет email и username
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('core:index')
            else:
                messages.error(request, "Invalid email/username or password.")
        else:
            messages.error(request, form.errors)
    else:
        form = UserLoginForm()
    
    return render(request, 'userauths/sign-in.html', {'form': form})


@login_required
def logout_view(request):
    """
    GET /user/sign-out/
    - Выход из системы
    - Очистка сессии
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('userauths:sign-in')


@login_required
def profile_view(request):
    """
    GET /user/profile/ - просмотр профиля
    POST /user/profile/ - обновление профиля
    """
    profile = request.user.profile
    
    if request.method == 'POST':
        # Обновление данных профиля
        profile.address = request.POST.get('address')
        profile.country = request.POST.get('country')
        profile.city = request.POST.get('city')
        
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('userauths:profile')
    
    return render(request, 'userauths/profile.html', {'profile': profile})
```

### CartOrders App Views (cartorders/views.py)

```python
@login_required
def add_to_cart(request, product_id):
    """
    POST /cart/add/<int:product_id>/
    - Добавление товара в корзину
    - Использует session для хранения корзины
    """
    product = get_object_or_404(Product, id=product_id)
    
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)]['qty'] += 1
    else:
        cart[str(product_id)] = {
            'product_id': product.id,
            'title': product.title,
            'price': str(product.price),
            'qty': 1,
            'image': product.image.url if product.image else None
        }
    
    request.session['cart'] = cart
    messages.success(request, f"{product.title} added to cart!")
    return redirect('cartorders:cart')


@login_required
def cart_view(request):
    """
    GET /cart/
    - Просмотр корзины
    - Расчет общей суммы
    - Кнопка checkout
    """
    cart = request.session.get('cart', {})
    
    total = 0
    for item in cart.values():
        total += Decimal(item['price']) * item['qty']
    
    return render(request, 'cartorders/cart.html', {
        'cart': cart,
        'total': total
    })


@login_required
def checkout_view(request):
    """
    GET /checkout/ - форма оформления заказа
    POST /checkout/ - создание заказа
    
    Workflow:
    1. Получить данные из корзины (session)
    2. Создать CartOrder
    3. Создать CartOrderItem для каждого товара
    4. Очистить корзину
    5. Отправить email (через Celery)
    6. Редирект на payment или success page
    """
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect('cartorders:cart')
        
        # Создаем заказ
        total_price = sum(Decimal(item['price']) * item['qty'] for item in cart.values())
        
        order = CartOrder.objects.create(
            user=request.user,
            price=total_price,
            paid_status=False,
            oid=shortuuid.uuid()
        )
        
        # Создаем товары заказа
        for item in cart.values():
            product = Product.objects.get(id=item['product_id'])
            CartOrderItem.objects.create(
                order=order,
                product=product,
                vendor=product.vendor,
                qty=item['qty'],
                price=product.price,
                total=product.price * item['qty']
            )
        
        # Очищаем корзину
        request.session['cart'] = {}
        
        # Отправляем email (через Celery)
        # send_order_confirmation_email.delay(order.id)
        
        messages.success(request, f"Order #{order.oid} created successfully!")
        return redirect('cartorders:order_detail', oid=order.oid)
    
    return render(request, 'cartorders/checkout.html')


@login_required
def order_list_view(request):
    """
    GET /orders/
    - Список всех заказов пользователя
    - Сортировка по дате (новые первыми)
    """
    orders = CartOrder.objects.filter(user=request.user).order_by('-order_date')
    
    return render(request, 'cartorders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, oid):
    """
    GET /order/<oid>/
    - Детали конкретного заказа
    - Список товаров
    - Статусы оплаты и доставки
    """
    order = get_object_or_404(CartOrder, oid=oid, user=request.user)
    items = CartOrderItem.objects.filter(order=order).select_related('product', 'vendor')
    
    return render(request, 'cartorders/order_detail.html', {
        'order': order,
        'items': items
    })
```

---

## Бизнес-логика

### Signals (Автоматическая обработка)

```python
# userauths/models.py
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически создает Profile при создании User
    """
    if created:
        try:
            Profile.objects.create(user=instance)
            logger.info(f"Profile created for user {instance.username}")
        except Exception as e:
            logger.error(f"Error creating profile for {instance.username}: {e}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Автоматически сохраняет Profile при сохранении User
    """
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Если профиль не существует - создаем
        Profile.objects.create(user=instance)
    except Exception as e:
        logger.error(f"Error saving profile for {instance.username}: {e}")
```

### Context Processors (Глобальные переменные)

```python
# core/context_processor.py
def default(request):
    """
    Добавляет переменные во все templates
    - categories: список всех категорий
    - vendors: список всех продавцов
    - address: адрес пользователя (если залогинен)
    """
    try:
        categories = Category.objects.all()
    except Exception as e:
        logger.error(f"Error loading categories: {e}")
        categories = []
    
    try:
        vendors = Vendor.objects.filter(verified=True)
    except Exception as e:
        logger.error(f"Error loading vendors: {e}")
        vendors = []
    
    try:
        address = None
        if request.user.is_authenticated:
            address = request.user.profile.address
    except Exception as e:
        logger.error(f"Error loading user address: {e}")
        address = None
    
    return {
        "categories": categories,
        "vendors": vendors,
        "address": address
    }
```

Зарегистрирован в `settings.py`:
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ...
                'core.context_processor.default',
            ],
        },
    },
]
```

---

## Асинхронные задачи

### Celery Configuration (ecomprj/settings.py)

```python
# Celery Configuration
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# EAGER mode для development (синхронное выполнение)
CELERY_TASK_ALWAYS_EAGER = True  # В production = False
CELERY_TASK_EAGER_PROPAGATES = False  # Не прокидывать исключения
```

### Примеры Celery Tasks

```python
# cartorders/tasks.py (пример)
from celery import shared_task
from django.core.mail import send_mail
from .models import CartOrder

@shared_task
def send_order_confirmation_email(order_id):
    """
    Отправка email подтверждения заказа
    """
    try:
        order = CartOrder.objects.get(id=order_id)
        user = order.user
        
        subject = f"Order Confirmation #{order.oid}"
        message = f"""
        Dear {user.username},
        
        Your order #{order.oid} has been received.
        Total amount: ${order.price}
        
        Thank you for your purchase!
        """
        
        send_mail(
            subject,
            message,
            'noreply@multivendor.com',
            [user.email],
            fail_silently=False,
        )
        
        return f"Email sent to {user.email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"


@shared_task
def generate_sales_report():
    """
    Генерация отчета по продажам (запускается периодически)
    """
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    
    # Продажи за последние 30 дней
    last_month = datetime.now() - timedelta(days=30)
    
    orders = CartOrder.objects.filter(
        order_date__gte=last_month,
        paid_status=True
    )
    
    total_sales = orders.aggregate(Sum('price'))['price__sum'] or 0
    total_orders = orders.count()
    
    # Сохраняем отчет или отправляем email админам
    report = f"Total sales (30 days): ${total_sales}, Orders: {total_orders}"
    
    return report
```

---

## Безопасность

### Authentication Backend (Custom)

```python
# userauths/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Кастомный backend для аутентификации через email ИЛИ username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Сначала пытаемся найти по email (case-insensitive)
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            try:
                # Если не найден - пытаемся по username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        # Проверяем пароль
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
```

Зарегистрирован в `settings.py`:
```python
AUTHENTICATION_BACKENDS = [
    'userauths.backends.EmailBackend',  # Наш custom backend
    'django.contrib.auth.backends.ModelBackend',  # Fallback
]
```

### Security Settings (settings.py)

```python
# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# HTTPS/SSL (production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# CSRF
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = False

# Session
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = False

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### Permissions & Decorators

```python
# useradmin/decorators.py
from django.shortcuts import redirect
from functools import wraps

def vendor_required(function):
    """
    Декоратор для проверки, что пользователь является vendor
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('userauths:sign-in')
        
        try:
            if request.user.vendor:
                return function(request, *args, **kwargs)
        except:
            pass
        
        return redirect('core:index')
    
    return wrap


# Использование:
@vendor_required
def vendor_dashboard(request):
    """Доступно только продавцам"""
    pass
```

---

## Оптимизация и кеширование

### Database Query Optimization

```python
# ПЛОХО - N+1 queries problem
products = Product.objects.all()
for product in products:
    print(product.vendor.title)  # Запрос к БД для каждого vendor
    print(product.category.title)  # Запрос к БД для каждой category

# ХОРОШО - select_related (для ForeignKey, OneToOne)
products = Product.objects.select_related('vendor', 'category').all()
for product in products:
    print(product.vendor.title)  # Без дополнительных запросов
    print(product.category.title)


# ПЛОХО - N+1 для reverse ForeignKey
for order in CartOrder.objects.all():
    items = order.cartorderitem_set.all()  # Запрос для каждого order

# ХОРОШО - prefetch_related (для reverse ForeignKey, ManyToMany)
orders = CartOrder.objects.prefetch_related('cartorderitem_set__product').all()
for order in orders:
    items = order.cartorderitem_set.all()  # Без дополнительных запросов


# Aggregation
from django.db.models import Sum, Avg, Count

# Средний рейтинг товара
avg_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))

# Общая сумма заказов пользователя
total_spent = CartOrder.objects.filter(
    user=request.user,
    paid_status=True
).aggregate(Sum('price'))

# Количество товаров в категории
category_counts = Product.objects.values('category__title').annotate(
    count=Count('id')
)
```

### Redis Caching (settings.py)

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.client.DefaultClient",
        "LOCATION": os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Используем стандартный PythonParser (HiredisParser несовместим)
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "retry_on_timeout": True
            },
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
        "KEY_PREFIX": "ecomprj",
        "TIMEOUT": 300,  # 5 minutes default
    }
}

# Fallback к LocMemCache если Redis недоступен
try:
    from django_redis import get_redis_connection
    get_redis_connection('default').ping()
except:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
```

### Использование кеша в views

```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Кешировать целую view (5 минут)
@cache_page(60 * 5)
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})


# Кешировать конкретные данные
def category_view(request, slug):
    # Ключ кеша
    cache_key = f'category_products_{slug}'
    
    # Попытка получить из кеша
    products = cache.get(cache_key)
    
    if products is None:
        # Если нет в кеше - запрос к БД
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category, status="published")
        
        # Сохраняем в кеш на 10 минут
        cache.set(cache_key, products, 60 * 10)
    
    return render(request, 'core/category.html', {'products': products})


# Инвалидация кеша при изменении данных
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Обновляем товар
    product.price = request.POST.get('price')
    product.save()
    
    # Удаляем связанный кеш
    cache.delete(f'product_detail_{product.slug}')
    cache.delete(f'category_products_{product.category.slug}')
    
    return redirect('core:product_detail', slug=product.slug)
```

### Static Files Optimization

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# WhiteNoise для production
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # После SecurityMiddleware
    # ...
]

# Сжатие и кеширование статики
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## Логирование

### Logging Configuration (settings.py)

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'userauths': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'cartorders': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
```

### Использование логирования

```python
import logging

logger = logging.getLogger(__name__)

def register_view(request):
    try:
        # Код регистрации
        new_user = form.save()
        logger.info(f"New user registered: {new_user.username}")
        
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}", exc_info=True)
        messages.error(request, "Registration failed. Please try again.")
```

---

## Заключение

Бэкенд построен на Django с использованием:
- ✅ **MVC (MTV) архитектура**
- ✅ **10+ моделей** с правильными связями (1:1, 1:Many, Many:Many)
- ✅ **Custom authentication** (email/username)
- ✅ **Оптимизированные SQL запросы** (select_related, prefetch_related)
- ✅ **Redis кеширование** с fallback
- ✅ **Celery** для асинхронных задач
- ✅ **Security best practices** (HTTPS, CSRF, password validation)
- ✅ **Signals** для автоматических действий
- ✅ **Context processors** для глобальных переменных
- ✅ **Logging** для debugging и мониторинга

Следующие документы:
- FRONTEND_ARCHITECTURE.md
- INTEGRATION_WORKFLOW.md
- USE_CASE_DIAGRAMS.md
- PROJECT_REPORT.md
