# Dokumentasi Praktik Authentication, Permission, Pagination, dan Filter
# Pertemuan ke 7

Project ini adalah API sederhana untuk sistem POS/restoran yang dibuat dengan Django dan Django REST Framework. Fokus dokumentasi ini adalah menjelaskan bagaimana project menerapkan:

- `Authentication`
- `Permission`
- `Pagination`
- `Filter`

Source code utama ada di folder [pos](./pos), sedangkan endpoint API berada di [pos/api](./pos/api).

## Teknologi

- Django `5.2.13`
- Django REST Framework `3.17.1`
- django-filter `25.2`
- SQLite

## Menjalankan Project

```bash
cd pos
pip install -r requiment.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Base URL lokal:

```text
http://127.0.0.1:8000
```

Panel admin:

```text
http://127.0.0.1:8000/super-admin/
```

## Ringkasan Endpoint

| Endpoint | Method | Akses | Keterangan |
| --- | --- | --- | --- |
| `/api/register` | `POST` | Public | Registrasi user baru |
| `/api/login` | `POST` | Public | Login dan mendapatkan token |
| `/api/menu-resto` | `GET` | Authenticated | Melihat data menu |
| `/api/menu-resto-filter/` | `GET` | Authenticated | Melihat data menu dengan filter, ordering, dan pagination |
| `/api/table_resto` | `GET`, `POST` | Authenticated | List dan tambah meja restoran |
| `/api/table_resto/<id>` | `GET`, `PUT`, `DELETE` | Authenticated | Detail, ubah, dan hapus meja restoran |

## Authentication

Authentication global dikonfigurasi di [pos/pos/settings.py](/d:/ti4pa/pos/pos/settings.py) melalui `REST_FRAMEWORK`:

```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
]
```

Artinya project ini mendukung tiga cara autentikasi:

1. `TokenAuthentication`
2. `BasicAuthentication`
3. `SessionAuthentication`

Untuk konsumsi API, cara yang paling nyaman adalah `TokenAuthentication`.

### Alur Authentication

1. User melakukan registrasi lewat endpoint `/api/register`
2. User login lewat endpoint `/api/login`
3. Server mengembalikan token
4. Token dikirim pada header request berikutnya

Header yang digunakan:

```http
Authorization: Token <token_anda>
```

### Contoh Register

Request:

```http
POST /api/register
Content-Type: application/json
```

```json
{
  "username": "waitress1",
  "email": "waitress1@example.com",
  "password1": "Password123!",
  "password2": "Password123!",
  "is_active": true,
  "first_name": "Siti",
  "last_name": "Aulia"
}
```

Catatan:

- `password1` dan `password2` harus sama
- Password divalidasi dengan validator bawaan Django
- Endpoint ini bersifat public karena memakai `AllowAny`

### Contoh Login

Request:

```http
POST /api/login
Content-Type: application/json
```

```json
{
  "username": "waitress1",
  "password": "Password123!"
}
```

Contoh response:

```json
{
  "status": 200,
  "message": "Selamat anda berhasil masuk....",
  "data": {
    "token": "1a2b3c4d5e6f",
    "id": 1,
    "first_name": "Siti",
    "last_name": "Aulia",
    "email": "waitress1@example.com",
    "is_active": true
  }
}
```

### Contoh Akses Endpoint Setelah Login

```bash
curl http://127.0.0.1:8000/api/menu-resto ^
  -H "Authorization: Token 1a2b3c4d5e6f"
```

## Permission

Permission global juga diatur di [pos/pos/settings.py](/d:/ti4pa/pos/pos/settings.py):

```python
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
]
```

Maknanya:

- Secara default semua endpoint API hanya bisa diakses user yang sudah login
- Jika request tidak membawa autentikasi yang valid, maka akses akan ditolak

### Endpoint Public

Endpoint berikut secara eksplisit diizinkan untuk semua user:

- `/api/register`
- `/api/login`

Keduanya memakai `permission_classes = [AllowAny]` di [pos/api/views.py](/d:/ti4pa/pos/api/views.py).

### Endpoint Protected

Endpoint berikut membutuhkan user yang terautentikasi:

- `/api/menu-resto`
- `/api/menu-resto-filter/`
- `/api/table_resto`
- `/api/table_resto/<id>`

Jika token tidak dikirim atau salah, response umumnya berupa `401 Unauthorized`.

## Pagination

Fitur pagination dipakai pada endpoint:

```text
/api/menu-resto-filter/
```

View ini menggunakan `CustomPagination` dari [pos/api/paginators.py](/d:/ti4pa/pos/api/paginators.py), yang mewarisi `LimitOffsetPagination`.

Konfigurasi aktif:

```python
default_limit = 10
limit_query_param = 'limit'
offset_query_param = 'offset'
max_limit = 50
```

Maknanya:

- Jika `limit` tidak dikirim, default data per request adalah `10`
- Parameter jumlah data memakai `limit`
- Posisi awal data memakai `offset`
- Nilai `limit` maksimal adalah `50`

### Contoh Pagination

Ambil 5 data pertama:

```text
GET /api/menu-resto-filter/?limit=5&offset=0
```

Ambil 5 data berikutnya:

```text
GET /api/menu-resto-filter/?limit=5&offset=5
```

Contoh bentuk response pagination DRF:

```json
{
  "count": 20,
  "next": "http://127.0.0.1:8000/api/menu-resto-filter/?limit=5&offset=5",
  "previous": null,
  "results": [
    {
      "id": 1,
      "code": "M001",
      "name": "Nasi Goreng",
      "price": "25000.00"
    }
  ]
}
```

## Filter

Fitur filter juga diterapkan pada endpoint:

```text
/api/menu-resto-filter/
```

Implementasinya ada di [pos/api/views.py](/d:/ti4pa/pos/api/views.py):

```python
filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
filterset_fields = ['category__name']
ordering_fields = ['created_on']
```

Artinya endpoint mendukung:

- Filter berdasarkan nama kategori menu
- Ordering berdasarkan field `created_on`

### Filter Berdasarkan Kategori

Contoh:

```text
GET /api/menu-resto-filter/?category__name=Minuman
```

Contoh di atas hanya menampilkan menu dengan kategori `Minuman`.

### Ordering Data

Urutkan dari yang paling lama:

```text
GET /api/menu-resto-filter/?ordering=created_on
```

Urutkan dari yang paling baru:

```text
GET /api/menu-resto-filter/?ordering=-created_on
```

### Kombinasi Filter + Ordering + Pagination

Contoh request yang lengkap:

```text
GET /api/menu-resto-filter/?category__name=Makanan&ordering=-created_on&limit=5&offset=0
```

Fungsi request tersebut:

- Menampilkan hanya menu kategori `Makanan`
- Data diurutkan dari yang terbaru
- Jumlah data per response `5`
- Mulai dari data ke-`0`

## Praktik yang Terjadi di Project Ini

Jika diringkas, pola kerjanya adalah sebagai berikut:

1. User daftar melalui `/api/register`
2. User login melalui `/api/login`
3. Token dari login dipakai untuk mengakses endpoint yang diproteksi
4. Endpoint `/api/menu-resto-filter/` memanfaatkan authentication, permission, pagination, dan filter sekaligus

Endpoint `/api/menu-resto-filter/` adalah contoh terbaik untuk demonstrasi empat konsep tersebut dalam satu alur.

## Contoh Uji Coba Lengkap

### 1. Login

```bash
curl -X POST http://127.0.0.1:8000/api/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"waitress1\",\"password\":\"Password123!\"}"
```

### 2. Gunakan Token untuk Filter dan Pagination

```bash
curl "http://127.0.0.1:8000/api/menu-resto-filter/?category__name=Minuman&ordering=-created_on&limit=3&offset=0" ^
  -H "Authorization: Token 1a2b3c4d5e6f"
```

## File yang Paling Relevan

- [pos/pos/settings.py](/d:/ti4pa/pos/pos/settings.py): konfigurasi global DRF
- [pos/api/views.py](/d:/ti4pa/pos/api/views.py): endpoint API, permission, filter, ordering
- [pos/api/paginators.py](/d:/ti4pa/pos/api/paginators.py): custom pagination
- [pos/api/serializers.py](/d:/ti4pa/pos/api/serializers.py): validasi register dan login
- [pos/pos_app/models.py](/d:/ti4pa/pos/pos_app/models.py): model `MenuResto`, `Category`, `StatusModel`, `TableResto`

## Kesimpulan

Project ini sudah menunjukkan praktik dasar Django REST Framework untuk:

- Mengautentikasi user dengan token, basic auth, dan session auth
- Membatasi akses endpoint dengan permission
- Membagi data besar dengan pagination `limit-offset`
- Menyaring dan mengurutkan data melalui query parameter

Untuk pembelajaran `authentication`, `permission`, `pagination`, dan `filter`, endpoint `/api/menu-resto-filter/` adalah titik praktik utama pada project ini.
