# FastAPI Todo & User Management API

Bu proje, **FastAPI** kullanılarak geliştirilmiş bir **Todo ve Kullanıcı Yönetim API'si**dir.
API, kullanıcı oluşturma, giriş, token tabanlı kimlik doğrulama, todo ekleme/güncelleme/silme ve listeleme işlevlerini içerir.

---

## 📦 Teknolojiler

* Python 3.11
* FastAPI
* SQLAlchemy
* Pydantic
* Passlib (şifreleme)
* JWT (JSON Web Token)
* SQLite

---

## ⚙️ Kurulum

1. **Projeyi klonlayın**

```bash
https://github.com/kayracihanbaskan/FastAPI-TodoApp.git
cd FastAPI-TodoApp
```

2. **Sanal ortam oluşturun ve aktifleştirin**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

3. **Gerekli paketleri yükleyin**

```bash
pip install -r requirements.txt
```

4. **Veritabanı bağlantısını ayarlayın**

* `database.py` dosyasında veritabanı URL’sini güncelleyin:

```python
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
```

5. **Veritabanını başlatın ve tabloları oluşturun**

```python
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)
```

---

## 🚀 API Başlatma

```bash
uvicorn main:app --reload
```

* API varsayılan olarak `http://127.0.0.1:8000` adresinde çalışır
* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## 🔑 Authentication

* JWT ile **access token** ve **refresh token** kullanılır
* Login endpoint: `POST /auth/user/login`

```json
{
  "username": "kullanici_adi",
  "password": "sifre"
}
```

* Token tipleri: `access` (20 dakika), `refresh` (7 gün)

---

## 👤 Kullanıcı Endpointleri

| Endpoint                      | Method | Açıklama                                             |
| ----------------------------- | ------ | ---------------------------------------------------- |
| `/auth/user/create/`          | POST   | Yeni kullanıcı oluşturur                             |
| `/auth/user/login`            | POST   | Kullanıcı giriş yapar, access ve refresh token döner |
| `/auth/user/all`              | GET    | Tüm kullanıcıları listeler                           |
| `/auth/user/{user_id}`        | GET    | ID’ye göre kullanıcı getirir                         |
| `/auth/user/delete/{user_id}` | DELETE | ID’ye göre kullanıcı siler                           |
| `/auth/user/update/{user_id}` | PATCH  | ID’ye göre kullanıcı günceller                       |

---

## ✅ Todo Endpointleri

| Endpoint                       | Method | Açıklama                  |
| ------------------------------ | ------ | ------------------------- |
| `/todos/todo/get-all`          | GET    | Tüm todo’ları listeler    |
| `/todos/todo/{todo_id}`        | GET    | ID’ye göre todo getirir   |
| `/todos/todo/create`           | POST   | Yeni todo oluşturur       |
| `/todos/todo/delete/{todo_id}` | DELETE | ID’ye göre todo siler     |
| `/todos/todo/update/{id}`      | PATCH  | ID’ye göre todo günceller |

---

## 🔒 Güvenlik

* Şifreler **bcrypt** ile hashlenir
* JWT kullanılarak API endpointlerine yetkilendirme yapılır
* Access token ile endpointlere erişim sağlanır

---

## 📖 Örnek Kullanım (Python)

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Login
resp = requests.post(f"{BASE_URL}/auth/user/login", data={"username":"test","password":"123"})
tokens = resp.json()

# Access token ile todo oluşturma
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
todo_data = {"title":"Örnek Todo", "description":"Deneme"}
resp = requests.post(f"{BASE_URL}/todos/todo/create", json=todo_data, headers=headers)
print(resp.json())
```


