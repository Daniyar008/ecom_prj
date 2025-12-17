# 📊 USE CASE DIAGRAMS & USER STORIES

## Оглавление
1. [Актеры системы](#актеры-системы)
2. [Главная Use Case диаграмма](#главная-use-case-диаграмма)
3. [Use Cases по модулям](#use-cases-по-модулям)
4. [Детальные сценарии](#детальные-сценарии)
5. [Sequence диаграммы](#sequence-диаграммы)

---

## Актеры системы

### 1. **Guest (Гость)** - Неавторизованный пользователь
**Возможности:**
- Просмотр каталога товаров
- Поиск товаров
- Просмотр деталей товара
- Просмотр отзывов
- Фильтрация по категориям, цене
- Просмотр профилей vendors
- Регистрация
- Вход в систему

**Ограничения:**
- ❌ Нельзя добавить в корзину
- ❌ Нельзя добавить в избранное
- ❌ Нельзя оставить отзыв
- ❌ Нельзя оформить заказ

---

### 2. **Customer (Покупатель)** - Авторизованный пользователь
**Возможности:**
- ✅ Все возможности Guest
- ✅ Управление профилем (редактировать адрес, аватар, био)
- ✅ Добавление товаров в корзину
- ✅ Добавление товаров в избранное
- ✅ Оформление заказов
- ✅ Просмотр истории заказов
- ✅ Отслеживание статуса заказа
- ✅ Написание отзывов на товары
- ✅ Изменение количества товаров в корзине
- ✅ Удаление товаров из корзины
- ✅ Смена пароля

**Dashboard:**
- Статистика заказов
- Последние заказы
- Избранные товары
- Настройки профиля

---

### 3. **Vendor (Продавец)** - Владелец магазина
**Возможности:**
- ✅ Все возможности Customer
- ✅ Управление своими товарами (CRUD)
- ✅ Просмотр заказов своих товаров
- ✅ Обновление статусов заказов
- ✅ Просмотр отзывов на свои товары
- ✅ Просмотр аналитики продаж
- ✅ Управление информацией о магазине
- ✅ Просмотр финансовой статистики

**Dashboard:**
- Продажи за период
- Топ товары
- Заказы (новые, в обработке, доставлено)
- Финансовая статистика
- Управление товарами

---

### 4. **Admin (Администратор)** - Суперпользователь
**Возможности:**
- ✅ Все возможности Vendor
- ✅ Управление всеми пользователями
- ✅ Управление всеми товарами (всех vendors)
- ✅ Управление категориями
- ✅ Управление всеми заказами
- ✅ Модерация отзывов
- ✅ Управление налогами (Tax)
- ✅ Управление промокодами (Coupon)
- ✅ Просмотр логов
- ✅ Настройки системы

**Django Admin Panel:**
- Полный доступ к базе данных
- CRUD для всех моделей
- Массовые операции
- Экспорт данных

---

## Главная Use Case диаграмма

```
                    E-COMMERCE MULTIVENDOR PLATFORM
                           USE CASE DIAGRAM

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│                                 SYSTEM BOUNDARY                               │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                                                                     │    │
│   │                          ┌──────────────┐                          │    │
│   │                          │   Browse     │                          │    │
│   │                          │   Products   │                          │    │
│   │                          └──────┬───────┘                          │    │
│   │                                 │                                   │    │
│   │     ┌──────────┐         ┌─────▼──────┐         ┌──────────┐     │    │
│   │     │  Search  │         │  View      │         │  Filter  │     │    │
│   │     │ Products │◄────────┤  Product   ├────────►│ Products │     │    │
│   │     └──────────┘         │  Details   │         └──────────┘     │    │
│   │                          └─────┬──────┘                           │    │
│   │                                │                                   │    │
│   │                          ┌─────▼──────┐                           │    │
│   │                          │  View      │                           │    │
│   │                          │  Reviews   │                           │    │
│   │                          └────────────┘                           │    │
│   │                                                                     │    │
│   │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │    │
│   │                  GUEST CAPABILITIES (above)                       │    │
│   │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │    │
│   │                                                                     │    │
│   │                          ┌──────────────┐                          │    │
│   │                          │   Register   │                          │    │
│   │                          └──────┬───────┘                          │    │
│   │                                 │                                   │    │
│   │                          ┌──────▼───────┐                          │    │
│   │                          │    Login     │                          │    │
│   │                          └──────┬───────┘                          │    │
│   │                                 │                                   │    │
│   └─────────────────────────────────┼───────────────────────────────────┘    │
│                                     │                                        │
│     ┌───────┐                       │                                        │
│     │ Guest │───────────────────────┘                                        │
│     └───────┘                                                                │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                  CUSTOMER CAPABILITIES                              │  │
│   │                                                                       │  │
│   │     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │  │
│   │     │  Add to      │      │  Add to      │      │   Manage     │  │  │
│   │     │  Cart        │      │  Wishlist    │      │   Profile    │  │  │
│   │     └──────┬───────┘      └──────────────┘      └──────────────┘  │  │
│   │            │                                                         │  │
│   │            │                                                         │  │
│   │     ┌──────▼───────┐      ┌──────────────┐      ┌──────────────┐  │  │
│   │     │  View Cart   │      │   Checkout   │      │  View Orders │  │  │
│   │     └──────────────┘      └──────┬───────┘      └──────────────┘  │  │
│   │                                   │                                  │  │
│   │                            ┌──────▼───────┐                         │  │
│   │                            │ Place Order  │                         │  │
│   │                            └──────┬───────┘                         │  │
│   │                                   │                                  │  │
│   │                            ┌──────▼───────┐                         │  │
│   │                            │    Track     │                         │  │
│   │                            │  Order Status│                         │  │
│   │                            └──────────────┘                         │  │
│   │                                                                       │  │
│   │                            ┌──────────────┐                         │  │
│   │                            │    Write     │                         │  │
│   │                            │    Review    │                         │  │
│   │                            └──────────────┘                         │  │
│   │                                                                       │  │
│   └───────────────────────────────────────────────────────────────────────┘  │
│                                     │                                        │
│     ┌──────────┐                    │                                        │
│     │ Customer │────────────────────┘                                        │
│     └──────────┘                                                             │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                   VENDOR CAPABILITIES                               │  │
│   │                                                                       │  │
│   │     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │  │
│   │     │  Create      │      │    Edit      │      │   Delete     │  │  │
│   │     │  Product     │      │  Product     │      │   Product    │  │  │
│   │     └──────────────┘      └──────────────┘      └──────────────┘  │  │
│   │                                                                       │  │
│   │     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │  │
│   │     │  View Vendor │      │   Update     │      │   View       │  │  │
│   │     │  Orders      │      │Order Status  │      │  Analytics   │  │  │
│   │     └──────────────┘      └──────────────┘      └──────────────┘  │  │
│   │                                                                       │  │
│   │     ┌──────────────┐      ┌──────────────┐                         │  │
│   │     │   Manage     │      │    View      │                         │  │
│   │     │  Store Info  │      │   Reviews    │                         │  │
│   │     └──────────────┘      └──────────────┘                         │  │
│   │                                                                       │  │
│   └───────────────────────────────────────────────────────────────────────┘  │
│                                     │                                        │
│     ┌────────┐                      │                                        │
│     │ Vendor │──────────────────────┘                                        │
│     └────────┘                                                               │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    ADMIN CAPABILITIES                               │  │
│   │                                                                       │  │
│   │     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │  │
│   │     │   Manage     │      │   Manage     │      │   Manage     │  │  │
│   │     │    Users     │      │ Categories   │      │  All Orders  │  │  │
│   │     └──────────────┘      └──────────────┘      └──────────────┘  │  │
│   │                                                                       │  │
│   │     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │  │
│   │     │   Moderate   │      │   Manage     │      │   Manage     │  │  │
│   │     │   Reviews    │      │    Taxes     │      │   Coupons    │  │  │
│   │     └──────────────┘      └──────────────┘      └──────────────┘  │  │
│   │                                                                       │  │
│   │     ┌──────────────┐      ┌──────────────┐                         │  │
│   │     │  View System │      │   Configure  │                         │  │
│   │     │    Logs      │      │   Settings   │                         │  │
│   │     └──────────────┘      └──────────────┘                         │  │
│   │                                                                       │  │
│   └───────────────────────────────────────────────────────────────────────┘  │
│                                     │                                        │
│     ┌───────┐                       │                                        │
│     │ Admin │───────────────────────┘                                        │
│     └───────┘                                                                │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Use Cases по модулям

### Модуль: Аутентификация (userauths app)

| UC ID | Use Case | Актер | Описание |
|-------|----------|-------|----------|
| **UC-001** | Register Account | Guest | Регистрация нового аккаунта (email, username, password) |
| **UC-002** | Login | Guest | Вход в систему (email OR username + password) |
| **UC-003** | Logout | Customer/Vendor/Admin | Выход из системы |
| **UC-004** | View Profile | Customer/Vendor/Admin | Просмотр своего профиля |
| **UC-005** | Edit Profile | Customer/Vendor/Admin | Редактирование профиля (address, bio, avatar) |
| **UC-006** | Change Password | Customer/Vendor/Admin | Смена пароля |
| **UC-007** | Reset Password | Guest | Восстановление забытого пароля (via email) |

---

### Модуль: Каталог товаров (core app)

| UC ID | Use Case | Актер | Описание |
|-------|----------|-------|----------|
| **UC-101** | Browse Products | All | Просмотр списка всех товаров (пагинация) |
| **UC-102** | View Product Detail | All | Просмотр детальной информации о товаре |
| **UC-103** | Search Products | All | Поиск товаров по ключевым словам (AJAX) |
| **UC-104** | Filter by Category | All | Фильтрация товаров по категории |
| **UC-105** | Filter by Price Range | All | Фильтрация товаров по диапазону цен |
| **UC-106** | Filter by Vendor | All | Фильтрация товаров по продавцу |
| **UC-107** | Sort Products | All | Сортировка (по цене, рейтингу, дате) |
| **UC-108** | View Product Reviews | All | Просмотр отзывов на товар |
| **UC-109** | View Product Gallery | All | Просмотр галереи изображений товара |
| **UC-110** | View Related Products | All | Просмотр похожих товаров |

---

### Модуль: Корзина и заказы (cartorders app)

| UC ID | Use Case | Актер | Описание |
|-------|----------|-------|----------|
| **UC-201** | Add to Cart | Customer/Vendor/Admin | Добавление товара в корзину (AJAX) |
| **UC-202** | View Cart | Customer/Vendor/Admin | Просмотр содержимого корзины |
| **UC-203** | Update Cart Quantity | Customer/Vendor/Admin | Изменение количества товара в корзине |
| **UC-204** | Remove from Cart | Customer/Vendor/Admin | Удаление товара из корзины |
| **UC-205** | Apply Coupon | Customer/Vendor/Admin | Применение промокода к заказу |
| **UC-206** | Checkout | Customer/Vendor/Admin | Оформление заказа (форма с адресом) |
| **UC-207** | Place Order | Customer/Vendor/Admin | Подтверждение и создание заказа |
| **UC-208** | View Order History | Customer/Vendor/Admin | Просмотр истории всех заказов |
| **UC-209** | View Order Detail | Customer/Vendor/Admin | Просмотр деталей конкретного заказа |
| **UC-210** | Track Order Status | Customer/Vendor/Admin | Отслеживание статуса заказа |
| **UC-211** | Cancel Order | Customer | Отмена заказа (до определенного статуса) |

---

### Модуль: Избранное (wishlists app)

| UC ID | Use Case | Актер | Описание |
|-------|----------|-------|----------|
| **UC-301** | Add to Wishlist | Customer/Vendor/Admin | Добавление товара в избранное (AJAX) |
| **UC-302** | View Wishlist | Customer/Vendor/Admin | Просмотр списка избранных товаров |
| **UC-303** | Remove from Wishlist | Customer/Vendor/Admin | Удаление товара из избранного |
| **UC-304** | Move to Cart | Customer/Vendor/Admin | Перемещение товара из избранного в корзину |

---

### Модуль: Отзывы (core app - Review model)

| UC ID | Use Case | Актер | Описание |
|-------|----------|-------|----------|
| **UC-401** | Write Review | Customer/Vendor/Admin | Написание отзыва на товар (rating + text) |
| **UC-402** | Edit Review | Customer/Vendor/Admin | Редактирование своего отзыва |
| **UC-403** | Delete Review | Customer/Vendor/Admin | Удаление своего отзыва |
| **UC-404** | View All Product Reviews | All | Просмотр всех отзывов на товар |
| **UC-405** | Moderate Reviews | Admin | Модерация отзывов (одобрение/удаление) |

---

### Модуль: Vendor Dashboard (useradmin app)

| UC ID | Use Case | Актер | Описание |
|-------|----------|-------|----------|
| **UC-501** | View Vendor Dashboard | Vendor | Просмотр панели управления (аналитика) |
| **UC-502** | Create Product | Vendor | Создание нового товара |
| **UC-503** | Edit Product | Vendor | Редактирование товара |
| **UC-504** | Delete Product | Vendor | Удаление товара |
| **UC-505** | View Vendor Orders | Vendor | Просмотр заказов своих товаров |
| **UC-506** | Update Order Status | Vendor | Обновление статуса заказа (processing/shipped/delivered) |
| **UC-507** | View Vendor Sales Analytics | Vendor | Просмотр аналитики продаж (графики, статистика) |
| **UC-508** | Manage Store Info | Vendor | Редактирование информации о магазине |
| **UC-509** | View Product Reviews | Vendor | Просмотр отзывов на свои товары |
| **UC-510** | View Financial Report | Vendor | Просмотр финансового отчета |

---

### Модуль: Admin Panel (Django Admin)

| UC ID | Use Case | Актер | Описание |
|-------|----------|-------|----------|
| **UC-601** | Manage Users | Admin | CRUD операции с пользователями |
| **UC-602** | Manage Categories | Admin | CRUD операции с категориями |
| **UC-603** | Manage All Products | Admin | CRUD операции со всеми товарами |
| **UC-604** | Manage All Orders | Admin | Просмотр и управление всеми заказами |
| **UC-605** | Manage Vendors | Admin | Управление продавцами (verify/ban) |
| **UC-606** | Manage Taxes | Admin | Управление налогами по регионам |
| **UC-607** | Manage Coupons | Admin | Создание/редактирование промокодов |
| **UC-608** | View System Logs | Admin | Просмотр логов системы |
| **UC-609** | Configure Settings | Admin | Настройка параметров системы |

---

## Детальные сценарии

### UC-001: Register Account (Регистрация)

**Актер:** Guest  
**Предусловие:** Пользователь не авторизован  
**Основной сценарий:**

1. Guest открывает страницу `/user/sign-up/`
2. Система отображает форму регистрации (username, email, password, password confirmation)
3. Guest заполняет форму
4. Guest нажимает кнопку "Register"
5. Система валидирует данные:
   - Username уникален
   - Email уникален (case-insensitive)
   - Password соответствует требованиям (минимум 8 символов, не только цифры)
   - Password confirmation совпадает
6. Система создает нового User
7. Система создает связанный Profile (через signal)
8. Система автоматически авторизует пользователя (login)
9. Система создает сессию
10. Система перенаправляет на `/dashboard/`
11. Система отображает сообщение успеха

**Альтернативные сценарии:**

**5a. Username уже существует:**
- Система отображает ошибку "Username already taken"
- Возврат к шагу 3

**5b. Email уже существует:**
- Система отображает ошибку "Email already registered"
- Возврат к шагу 3

**5c. Пароли не совпадают:**
- Система отображает ошибку "Passwords do not match"
- Возврат к шагу 3

**Постусловие:**
- Новый User создан в БД
- Profile создан и связан с User
- Пользователь авторизован
- Сессия создана

---

### UC-207: Place Order (Оформление заказа)

**Актер:** Customer  
**Предусловие:** 
- Пользователь авторизован
- Корзина не пустая (минимум 1 товар)

**Основной сценарий:**

1. Customer переходит на страницу `/cart/`
2. Система отображает товары в корзине с общей суммой
3. Customer нажимает "Proceed to Checkout"
4. Система перенаправляет на `/checkout/`
5. Система отображает форму оформления заказа (адрес доставки, заметки)
6. Customer проверяет/редактирует адрес доставки
7. Customer (опционально) применяет промокод
8. Система пересчитывает итоговую сумму (если промокод валидный)
9. Customer нажимает "Place Order"
10. Система начинает транзакцию (BEGIN TRANSACTION)
11. Система создает CartOrder запись в БД
12. Система создает CartOrderItem записи для каждого товара в корзине
13. Система фиксирует транзакцию (COMMIT)
14. Система очищает корзину (session['cart'] = {})
15. Система (опционально) отправляет email подтверждения (via Celery)
16. Система перенаправляет на `/order/<oid>/`
17. Система отображает детали созданного заказа

**Альтернативные сценарии:**

**1a. Корзина пустая:**
- Система отображает сообщение "Your cart is empty"
- Система перенаправляет на `/products/`

**7a. Промокод невалидный:**
- Система отображает ошибку "Invalid or expired coupon"
- Скидка не применяется
- Продолжение с шага 9

**10-13a. Ошибка при создании заказа:**
- Система откатывает транзакцию (ROLLBACK)
- Система отображает ошибку "Failed to create order"
- Корзина остается без изменений
- Возврат к шагу 4

**15a. Email не отправлен (timeout/error):**
- Заказ создан успешно
- Email будет отправлен позже (retry)
- Продолжение с шага 16

**Постусловие:**
- CartOrder создан в БД
- CartOrderItem записи созданы
- Корзина очищена
- Email подтверждения отправлен (или в очереди)
- Пользователь на странице деталей заказа

---

### UC-502: Create Product (Создание товара Vendor)

**Актер:** Vendor  
**Предусловие:** 
- Пользователь авторизован как Vendor
- Vendor верифицирован

**Основной сценарий:**

1. Vendor переходит на `/vendor/dashboard/products/`
2. Система отображает список товаров Vendor
3. Vendor нажимает "Add New Product"
4. Система отображает форму создания товара (title, description, price, category, images, etc.)
5. Vendor заполняет форму:
   - Title (обязательно)
   - Description
   - Price (обязательно)
   - Old Price (опционально, для скидки)
   - Category (обязательно, выбор из списка)
   - Main Image (обязательно)
   - Additional Images (до 5 штук)
   - Specifications (текст/HTML)
   - Stock quantity
   - Tags
6. Vendor нажимает "Create Product"
7. Система валидирует данные:
   - Title не пустой
   - Price > 0
   - Category выбрана
   - Main Image загружена
8. Система создает Product запись в БД
9. Система связывает Product с Vendor (FK)
10. Система загружает изображения в media/products/
11. Система создает ProductImage записи для дополнительных изображений
12. Система отображает сообщение "Product created successfully"
13. Система перенаправляет на страницу товара `/product/<slug>/`

**Альтернативные сценарии:**

**1a. Vendor не верифицирован:**
- Система отображает сообщение "Your vendor account is pending verification"
- Доступ запрещен

**7a. Валидация не прошла:**
- Система отображает ошибки (например, "Title is required", "Price must be positive")
- Возврат к шагу 5

**10a. Ошибка загрузки изображения:**
- Система отображает ошибку "Failed to upload image"
- Возврат к шагу 5

**Постусловие:**
- Product создан в БД
- Product связан с Vendor
- Изображения загружены
- ProductImage записи созданы
- Товар доступен для покупателей (если status="published")

---

## Sequence диаграммы

### Sequence Diagram: Add to Cart (AJAX)

```
┌────────┐         ┌─────────┐         ┌────────┐         ┌──────────┐
│ Browser│         │JavaScript│         │ Django │         │PostgreSQL│
└────┬───┘         └────┬────┘         └───┬────┘         └────┬─────┘
     │                  │                   │                    │
     │ 1. Click "Add   │                   │                    │
     │    to Cart"     │                   │                    │
     ├─────────────────►│                   │                    │
     │                  │                   │                    │
     │                  │ 2. AJAX POST      │                    │
     │                  │ /cart/add/123/    │                    │
     │                  │ (X-CSRFToken)     │                    │
     │                  ├──────────────────►│                    │
     │                  │                   │                    │
     │                  │                   │ 3. Check @login_  │
     │                  │                   │    required       │
     │                  │                   │ (session valid?)  │
     │                  │                   │                    │
     │                  │                   │ 4. SELECT * FROM  │
     │                  │                   │    product        │
     │                  │                   │    WHERE id=123   │
     │                  │                   ├───────────────────►│
     │                  │                   │                    │
     │                  │                   │ 5. Return product │
     │                  │                   │◄───────────────────┤
     │                  │                   │                    │
     │                  │                   │ 6. Get cart from  │
     │                  │                   │    session (Redis)│
     │                  │                   │                    │
     │                  │                   │ 7. Update cart    │
     │                  │                   │    data structure │
     │                  │                   │                    │
     │                  │                   │ 8. Save session   │
     │                  │                   │    (Redis SET)    │
     │                  │                   │                    │
     │                  │ 9. JSON response  │                    │
     │                  │ {success: true,   │                    │
     │                  │  cart_count: 3}   │                    │
     │                  │◄──────────────────┤                    │
     │                  │                   │                    │
     │ 10. Update UI    │                   │                    │
     │ - Badge count    │                   │                    │
     │ - Notification   │                   │                    │
     │◄─────────────────┤                   │                    │
     │                  │                   │                    │
```

---

### Sequence Diagram: Checkout Process

```
┌────────┐    ┌────────┐    ┌──────────┐    ┌──────────┐    ┌─────┐
│Customer│    │ Django │    │PostgreSQL│    │  Redis   │    │Email│
└───┬────┘    └───┬────┘    └────┬─────┘    └────┬─────┘    └──┬──┘
    │             │              │               │               │
    │ 1. POST /checkout/         │               │               │
    │ (confirm order)            │               │               │
    ├────────────►│              │               │               │
    │             │              │               │               │
    │             │ 2. Get cart from session     │               │
    │             ├─────────────────────────────►│               │
    │             │              │               │               │
    │             │ 3. Return cart               │               │
    │             │◄─────────────────────────────┤               │
    │             │              │               │               │
    │             │ 4. BEGIN TRANSACTION         │               │
    │             ├─────────────►│               │               │
    │             │              │               │               │
    │             │ 5. INSERT CartOrder          │               │
    │             ├─────────────►│               │               │
    │             │              │               │               │
    │             │ 6. Return order_id=999       │               │
    │             │◄─────────────┤               │               │
    │             │              │               │               │
    │             │ 7. Loop: INSERT CartOrderItem│               │
    │             │    (for each cart item)      │               │
    │             ├─────────────►│               │               │
    │             ├─────────────►│               │               │
    │             ├─────────────►│               │               │
    │             │              │               │               │
    │             │ 8. COMMIT TRANSACTION        │               │
    │             │◄─────────────┤               │               │
    │             │              │               │               │
    │             │ 9. Clear cart (session)      │               │
    │             ├─────────────────────────────►│               │
    │             │              │               │               │
    │             │ 10. Queue email task (Celery)│               │
    │             │───────────────────────────────────────────────►│
    │             │              │               │               │
    │ 11. HTTP 302 Redirect      │               │               │
    │    /order/xyz789abc/       │               │               │
    │◄────────────┤              │               │               │
    │             │              │               │               │
    │ 12. GET /order/xyz789abc/  │               │               │
    │────────────►│              │               │               │
    │             │              │               │               │
    │             │ 13. SELECT * FROM CartOrder  │               │
    │             │     WHERE oid='xyz789abc'    │               │
    │             ├─────────────►│               │               │
    │             │              │               │               │
    │             │ 14. SELECT * FROM CartOrderItem│              │
    │             │     WHERE order_id=999       │               │
    │             ├─────────────►│               │               │
    │             │              │               │               │
    │             │ 15. Return order details     │               │
    │             │◄─────────────┤               │               │
    │             │              │               │               │
    │ 16. HTTP 200 Order detail page             │               │
    │◄────────────┤              │               │               │
    │             │              │               │               │
    │             │              │               │  17. Send email│
    │             │              │               │    (async)    │
    │             │              │               │◄──────────────┤
    │             │              │               │               │
```

---

## URL Маршрутизация (Sitemap)

### Public URLs (доступны всем)

```
/                             → core.views.index (Главная страница)
/products/                    → core.views.product_list (Каталог)
/product/<slug>/              → core.views.product_detail (Детали товара)
/category/<slug>/             → core.views.category_view (Категория)
/search/                      → core.views.search_view (Поиск)
/vendor/<int:id>/             → vendors.views.vendor_detail (Профиль vendor)
/contact/                     → core.views.contact (Контакты)
/about/                       → core.views.about (О нас)
```

### Authentication URLs

```
/user/sign-up/                → userauths.views.register_view
/user/sign-in/                → userauths.views.login_view
/user/sign-out/               → userauths.views.logout_view
/user/password-reset/         → userauths.views.password_reset
```

### Customer Dashboard URLs (требуется авторизация)

```
/user/dashboard/              → userauths.views.dashboard
/user/profile/                → userauths.views.profile_view
/user/change-password/        → userauths.views.change_password
```

### Cart & Orders URLs (требуется авторизация)

```
/cart/                        → cartorders.views.cart_view
/cart/add/<int:id>/           → cartorders.views.add_to_cart (AJAX)
/cart/update/<int:id>/        → cartorders.views.update_cart
/cart/remove/<int:id>/        → cartorders.views.remove_from_cart
/checkout/                    → cartorders.views.checkout_view
/orders/                      → cartorders.views.order_list
/order/<str:oid>/             → cartorders.views.order_detail
```

### Wishlist URLs (требуется авторизация)

```
/wishlist/                    → wishlists.views.wishlist_view
/wishlist/add/<int:id>/       → wishlists.views.add_to_wishlist (AJAX)
/wishlist/remove/<int:id>/    → wishlists.views.remove_from_wishlist
```

### Vendor Dashboard URLs (требуется Vendor role)

```
/vendor/dashboard/            → useradmin.views.vendor_dashboard
/vendor/products/             → useradmin.views.product_list
/vendor/product/create/       → useradmin.views.product_create
/vendor/product/<int:id>/edit/→ useradmin.views.product_edit
/vendor/product/<int:id>/delete/→ useradmin.views.product_delete
/vendor/orders/               → useradmin.views.vendor_orders
/vendor/order/<int:id>/       → useradmin.views.vendor_order_detail
/vendor/analytics/            → useradmin.views.vendor_analytics
/vendor/settings/             → useradmin.views.vendor_settings
/vendor/reviews/              → useradmin.views.vendor_reviews
```

### Admin URLs (требуется Admin role)

```
/admin/                       → Django Admin (полный доступ к БД)
```

---

## Заключение Use Cases

✅ **4 актера определены:**
- Guest (гость)
- Customer (покупатель)
- Vendor (продавец)
- Admin (администратор)

✅ **60+ Use Cases документированы:**
- Аутентификация: 7 UC
- Каталог: 10 UC
- Корзина/Заказы: 11 UC
- Избранное: 4 UC
- Отзывы: 5 UC
- Vendor Dashboard: 10 UC
- Admin Panel: 9 UC

✅ **Детальные сценарии:**
- Основной flow
- Альтернативные пути
- Предусловия/Постусловия

✅ **Sequence диаграммы:**
- Add to Cart (AJAX)
- Checkout Process
- Взаимодействие компонентов

✅ **URL маршрутизация:**
- 30+ маршрутов
- Разделение по ролям

Следующий документ:
- PROJECT_REPORT.md (финальный отчет)
