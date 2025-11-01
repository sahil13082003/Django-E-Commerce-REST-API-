# 🛒 E-Commerce REST API

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive, production-ready e-commerce backend REST API built with Django REST Framework featuring role-based access control, JWT authentication, and complete shopping functionality.

[Features](#-features) • [Installation](#-installation) • [API Documentation](#-api-documentation) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Schema](#-database-schema)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [User Roles & Permissions](#-user-roles--permissions)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

This E-Commerce REST API provides a robust backend solution for building modern e-commerce applications. It implements industry-standard practices including JWT authentication, role-based access control (RBAC), and comprehensive product management capabilities.

### Key Highlights

- 🔐 **Secure Authentication**: JWT-based token authentication
- 👥 **Role-Based Access Control**: Three-tier user hierarchy (Super Admin, Admin, User)
- 🛍️ **Complete Shopping Flow**: Cart management, order processing, and payment integration-ready
- 📦 **Product Management**: Categories, brands, variants, and images
- ⭐ **Review System**: Product ratings and reviews
- 💰 **Discount System**: Coupons and discount management
- 📱 **Notification System**: Real-time user notifications
- 📊 **Admin Dashboard**: Full-featured Django admin interface

---

## ✨ Features

### User Management
- ✅ User registration and authentication
- ✅ JWT token-based security
- ✅ Profile management
- ✅ Address management
- ✅ Role-based permissions

### Product Management
- ✅ Categories with hierarchical structure
- ✅ Brand management
- ✅ Product variants (size, color, etc.)
- ✅ Multiple product images
- ✅ Stock management
- ✅ Product search and filtering

### Shopping Experience
- ✅ Shopping cart functionality
- ✅ Add/update/remove cart items
- ✅ Order creation and tracking
- ✅ Order status management
- ✅ Coupon code application
- ✅ Order history

### Additional Features
- ✅ Product reviews and ratings
- ✅ Discount and coupon system
- ✅ User notifications
- ✅ Admin order approval workflow
- ✅ Pagination and filtering
- ✅ CORS support for frontend integration

---

## 🛠️ Tech Stack

### Backend Framework
- **Django 4.2.7** - High-level Python web framework
- **Django REST Framework 3.14.0** - Powerful toolkit for building Web APIs

### Authentication & Security
- **djangorestframework-simplejwt 5.3.0** - JSON Web Token authentication
- **Django CORS Headers 4.3.0** - Cross-Origin Resource Sharing support

### Database
- **SQLite** (Development) - Lightweight database
- **PostgreSQL/MySQL** (Production Ready) - Scalable database options

### Additional Libraries
- **Pillow 10.1.0** - Image processing and handling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│              (Web App / Mobile App / Admin Panel)            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTPS/REST API
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      API Gateway Layer                       │
│                  (Django REST Framework)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Authentication (JWT) │ CORS │ Rate Limiting           │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Business Logic Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Users &   │  │  Products   │  │   Orders & Cart     │ │
│  │    Auth     │  │ Management  │  │    Management       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Reviews   │  │  Discounts  │  │   Notifications     │ │
│  │   & Ratings │  │  & Coupons  │  │      System         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      Data Access Layer                       │
│                      (Django ORM)                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      Database Layer                          │
│                   (SQLite/PostgreSQL)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Virtual environment tool (venv)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ecommerce_project.git
cd ecommerce_project
```

2. **Create and activate virtual environment**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Create .env file in project root
cp .env.example .env

# Edit .env with your configurations
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser (Super Admin)**
```bash
python manage.py createsuperuser
```

7. **Set superuser role to SUPER_ADMIN**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from core.models import UserProfile

user = User.objects.get(username='your_username')
profile = UserProfile.objects.get(user=user)
profile.role = 'SUPER_ADMIN'
profile.save()
exit()
```

8. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=300  # 5 hours
JWT_REFRESH_TOKEN_LIFETIME=86400  # 1 day

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Media Files
MEDIA_ROOT=media/
MEDIA_URL=/media/
```

### Database Configuration

**Development (SQLite):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🗄️ Database Schema

### Core Models

**User Management:**
- `User` - Django default user model
- `UserProfile` - Extended user information with role
- `Address` - User shipping addresses

**Product Management:**
- `Category` - Product categories (hierarchical)
- `Brand` - Product brands
- `Product` - Main product model
- `ProductVariant` - Product variants (size, color, etc.)
- `ProductImage` - Product images

**Shopping:**
- `Cart` - User shopping cart
- `CartItem` - Items in cart
- `Order` - Customer orders
- `OrderItem` - Items in order

**Marketing:**
- `Discount` - Discount campaigns
- `Coupon` - Promotional coupon codes
- `Review` - Product reviews and ratings
- `Notification` - User notifications

### Entity Relationship Diagram

```
User ──────────┬──────── UserProfile (role)
               ├──────── Address
               ├──────── Cart ──────── CartItem ──── ProductVariant
               ├──────── Order ─────── OrderItem ─── ProductVariant
               ├──────── Review ────── Product
               └──────── Notification

Category ───── Product ──┬─── ProductVariant
Brand ───────────────────┤
                         ├─── ProductImage
                         └─── Review

Discount ────────── (Admin Created)
Coupon ──────────── (Admin Created)
```

---

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/auth/register/` | Register new user | Public |
| POST | `/auth/login/` | Login user | Public |
| POST | `/auth/token/refresh/` | Refresh JWT token | Public |
| GET/PUT | `/auth/profile/` | Get/Update profile | Authenticated |
| POST | `/auth/create-admin/` | Create admin user | Super Admin |
| GET | `/auth/users/` | List all users | Super Admin |

### Category & Brand Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/categories/` | List categories | All |
| POST | `/categories/` | Create category | Admin+ |
| GET | `/categories/{id}/` | Category detail | All |
| PUT | `/categories/{id}/` | Update category | Admin+ |
| DELETE | `/categories/{id}/` | Delete category | Admin+ |
| GET | `/brands/` | List brands | All |
| POST | `/brands/` | Create brand | Admin+ |

### Product Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/products/` | List products | All |
| POST | `/products/` | Create product | Admin+ |
| GET | `/products/{id}/` | Product detail | All |
| PUT | `/products/{id}/` | Update product | Admin+ |
| DELETE | `/products/{id}/` | Delete product | Admin+ |
| POST | `/products/{id}/add_variant/` | Add product variant | Admin+ |
| POST | `/products/{id}/add_image/` | Upload product image | Admin+ |
| GET | `/products/{id}/reviews/` | Get product reviews | All |

### Cart Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/cart/` | View cart | User |
| POST | `/cart/add/` | Add item to cart | User |
| PUT | `/cart/update/{item_id}/` | Update cart item | User |
| DELETE | `/cart/remove/{item_id}/` | Remove cart item | User |

### Order Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/orders/create/` | Create order | User |
| GET | `/orders/` | List orders | Authenticated |
| GET | `/orders/{id}/` | Order detail | Authenticated |
| PUT | `/orders/{id}/update-status/` | Update order status | Admin+ |
| POST | `/orders/{id}/approve/` | Approve order | Admin+ |

### Review Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/products/{id}/reviews/` | Create review | User |
| DELETE | `/reviews/{id}/` | Delete review | Admin+ |

### Discount & Coupon Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/discounts/` | List discounts | All |
| POST | `/discounts/` | Create discount | Admin+ |
| GET | `/coupons/validate_coupon/?code=CODE` | Validate coupon | User |
| POST | `/coupons/` | Create coupon | Admin+ |

### Notification Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/notifications/` | List notifications | Authenticated |
| POST | `/notifications/{id}/mark-read/` | Mark as read | Authenticated |
| POST | `/notifications/send/` | Send notification | Super Admin |

### Address Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/addresses/` | List addresses | User |
| POST | `/addresses/` | Create address | User |
| PUT | `/addresses/{id}/` | Update address | User |
| DELETE | `/addresses/{id}/` | Delete address | User |

---

## 🔐 Authentication

This API uses JWT (JSON Web Token) authentication.

### Obtaining Tokens

**Request:**
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "user123",
  "password": "password123"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "role": "USER"
  }
}
```

### Using Access Token

Include the access token in the Authorization header:

```bash
GET /api/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refreshing Token

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 👥 User Roles & Permissions

### Role Hierarchy

| Role | Description | Capabilities |
|------|-------------|--------------|
| **SUPER_ADMIN** | System administrator | Full system access, manage admins, all CRUD operations |
| **ADMIN** | Store manager | Manage products, categories, orders, discounts |
| **USER** | Customer | Browse products, manage cart, place orders, write reviews |

### Permission Matrix

| Action | Super Admin | Admin | User |
|--------|-------------|-------|------|
| View Products | ✅ | ✅ | ✅ |
| Create/Edit Products | ✅ | ✅ | ❌ |
| Delete Products | ✅ | ✅ | ❌ |
| View Orders | ✅ (All) | ✅ (All) | ✅ (Own) |
| Approve Orders | ✅ | ✅ | ❌ |
| Manage Users | ✅ | ❌ | ❌ |
| Create Admins | ✅ | ❌ | ❌ |
| Manage Cart | ✅ | ✅ | ✅ |
| Write Reviews | ✅ | ✅ | ✅ |
| Delete Reviews | ✅ | ✅ | ❌ |
| Create Discounts | ✅ | ✅ | ❌ |
| Send Notifications | ✅ | ❌ | ❌ |

---

## 💡 Usage Examples

### 1. Register a New User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890"
  }'
```

### 2. Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123"
  }'
```

### 3. Create a Product (Admin)

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "description": "Latest Apple smartphone",
    "category": 1,
    "brand": 1,
    "base_price": 999.99,
    "stock": 50
  }'
```

### 4. Add Item to Cart

```bash
curl -X POST http://127.0.0.1:8000/api/cart/add/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_variant": 5,
    "quantity": 2
  }'
```

### 5. Create Order

```bash
curl -X POST http://127.0.0.1:8000/api/orders/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address": 1,
    "coupon_code": "WELCOME10"
  }'
```

### 6. Add Product Review

```bash
curl -X POST http://127.0.0.1:8000/api/products/1/reviews/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Excellent product! Highly recommended."
  }'
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test core

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Manual API Testing

**Using Postman:**
1. Import the Postman collection (if provided)
2. Set environment variables (base_url, access_token)
3. Test endpoints

**Using cURL:**
See usage examples above

**Using HTTPie:**
```bash
# Install HTTPie
pip install httpie

# Test endpoint
http GET http://127.0.0.1:8000/api/products/ \
  Authorization:"Bearer YOUR_TOKEN"
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure production database (PostgreSQL/MySQL)
- [ ] Set up environment variables
- [ ] Configure static files with WhiteNoise or CDN
- [ ] Set up media files storage (AWS S3, etc.)
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure CORS settings
- [ ] Set up logging and monitoring
- [ ] Run security checks: `python manage.py check --deploy`
- [ ] Set up automated backups
- [ ] Configure email settings for notifications

### Deploying to Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Add PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### Deploying to AWS/DigitalOcean

1. Set up server (Ubuntu 20.04+)
2. Install dependencies (Python, PostgreSQL, Nginx)
3. Configure Gunicorn
4. Set up Nginx reverse proxy
5. Configure SSL with Let's Encrypt
6. Set up systemd service
7. Configure firewall

Detailed deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/ecommerce_project.git
cd ecommerce_project
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
- Write clean, documented code
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation

4. **Commit your changes**
```bash
git add .
git commit -m "Add: Description of your feature"
```

5. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

6. **Create Pull Request**
- Go to the original repository
- Click "New Pull Request"
- Describe your changes
- Wait for review

### Coding Standards

- Follow PEP 8 style guide
- Write descriptive commit messages
- Add docstrings to functions and classes
- Write unit tests for new features
- Keep functions small and focused
- Use meaningful variable names

### Commit Message Format

```
Type: Brief description

Detailed description (optional)

Types: Add, Update, Fix, Remove, Refactor, Test, Docs
```

---

## 📄 License

This project is licensed under the SmartData Enterprices 

```
SmartData Enterprices License

Copyright (c) 2025 Sahil Golhar

```

---


⭐ Star this repo if you find it helpful!

</div>
