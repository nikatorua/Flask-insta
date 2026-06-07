# FlaskSocial

Instagram-ის გამარტივებული ვებ-აპლიკაცია, შექმნილი Flask Framework-ისა და SQLAlchemy ORM-ის გამოყენებით.

---

## გამოყენებული ტექნოლოგიები

| ტექნოლოგია | მიზნობრიობა |
|---|---|
| Flask | ვებ-ფრეიმვორკი |
| SQLAlchemy | ORM (Object-Relational Mapping) |
| SQLite | მონაცემთა ბაზა (სურათები BLOB-ად ინახება) |
| Flask-Login | სესიების მართვა / ავთენტიფიკაცია |
| Flask-WTF | ფორმები, ფაილების ატვირთვა და CSRF დაცვა |
| Bootstrap 5 | UI ფრეიმვორკი |
| Font Awesome 6 | ხატულები |

---

## მონაცემთა ბაზის სქემა

**User** — **Post** კავშირი: One-to-Many (ერთი მომხმარებელი → ბევრი პოსტი)

```
User                  Post              Like          Comment
────────────────      ─────────────     ─────────     ─────────
id (PK)               id (PK)           id (PK)       id (PK)
username              title             user_id (FK)  content
email                 description       post_id (FK)  created_at
password_hash         image_data        *UniqueConstraint user_id (FK)
bio                   image_mimetype                  post_id (FK)
profile_pic_data      created_at
profile_pic_mimetype  user_id (FK)
created_at
```

> სურათები (პოსტის ფოტო და პროფილის ფოტო) ინახება პირდაპირ SQLite-ში `LargeBinary` სვეტად.  
> სერვირება ხდება `/post/<id>/image` და `/user/<id>/avatar` მარშრუტებით.

---

## პროექტის სტრუქტურა

```
Flask-insta/
├── app.py                  <- Flask app factory
├── extensions.py           <- db, login_manager, csrf (circular import-ის გვერდის ავლა)
├── models.py               <- User, Post, Like, Comment მოდელები
├── forms.py                <- WTForms + FileField ფორმები
├── requirements.txt
├── routes/
│   ├── auth.py             <- /register, /login, /logout
│   ├── main.py             <- / (ფიდი), /search (ცარიელზე → ფიდი)
│   ├── posts.py            <- CRUD + like + comment + /post/<id>/image
│   └── users.py            <- /users, /user/<id>, /profile/edit, /user/<id>/avatar
├── templates/
│   ├── base.html           <- ნავბარი, Flash შეტყობინებები
│   ├── index.html          <- პოსტების ფიდი + pagination
│   ├── search.html         <- ძებნის შედეგები
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── posts/
│   │   ├── create.html     <- drag-and-drop ატვირთვა
│   │   ├── edit.html       <- drag-and-drop ატვირთვა (წინა სურათი ჩანს)
│   │   └── post.html       <- დეტალური ნახვა + კომენტარები + "უკან" ღილაკი
│   └── users/
│       ├── list.html
│       ├── profile.html
│       └── edit_profile.html <- avatar ატვირთვა კლიკით
├── static/
│   └── style.css           <- კასტომური dark theme
└── instance/
    └── flasksocial.db      <- SQLite ბაზა (გაშვებისას ავტომატურად იქმნება)
```

---

## გაშვების ინსტრუქცია

### 1. პროექტის საქაღალდეში გადასვლა

```bash
cd Flask-insta
```

### 2. ვირტუალური გარემოს შექმნა

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. დამოკიდებულებების დაყენება

```bash
pip install -r requirements.txt
```

### 4. გაშვება

```bash
python app.py
```

### 5. ბრაუზერში გახსნა

```
http://127.0.0.1:5000
```

> **შენიშვნა:** SQLite ბაზა (`instance/flasksocial.db`) პირველი გაშვებისას ავტომატურად იქმნება.

---

## ძირითადი ფუნქციონალი

- **რეგისტრაცია და ავთენტიფიკაცია** — ანგარიშის შექმნა, შესვლა, გამოსვლა
- **პოსტების CRUD** — შექმნა, ნახვა, რედაქტირება, წაშლა
- **სურათის ატვირთვა** — მოწყობილობიდან, drag-and-drop მხარდაჭერით; ინახება SQLite BLOB-ად
- **პოსტების ფიდი** — ყველა პოსტი თარიღის მიხედვით, 9 პოსტი გვერდზე (Pagination)
- **One-to-Many** — `user_id` Foreign Key პოსტებში
- **get_or_404()** — გამოიყენება ყველა Post და User-ის მოძიებისას
- **მოწონება (Like)** — ლაიქის დამატება/მოხსნა
- **კომენტარები** — პოსტებზე კომენტირება
- **პროფილის გვერდი** — ბიო, ფოტო ატვირთვა, პოსტების grid ნახვა
- **ძებნა** — სათაური/აღწერით
- **"უკან" ღილაკი** — პოსტის ნახვიდან დაბრუნება browser history-ის გამოყენებით

---

## მოკლე დემო სცენარი

1. გახსენი `http://127.0.0.1:5000` — გადამისამართდება `/login`-ზე

<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/1c193cc3-d2c2-4758-b526-d5c0245dd229" />

3. **რეგისტრაცია:** შექმენი ანგარიში

<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/73a7b2ff-dc16-4caf-940f-9c4cce12b5f9" />

5. **ახალი პოსტი:** დააჭირე `+` ნავბარში → ატვირთე სურათი (drag-and-drop ან კლიკი)

<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/13c7ebf4-d892-474a-acd4-fb0d40311e70" />

7. **ლაიქი / კომენტარი:** გახსენი ნებისმიერი პოსტი

<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/1b7ccd5d-408f-4925-884e-42752654bf37" />

9. **პროფილი:** ავატარზე კლიკი ნავბარში → "პროფილი" → ფოტოს ატვირთვა

<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/bb859bdd-f521-4358-9026-7265df23628e" />

11. **ძებნა:** ნავბარის ველი

<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/758a4f24-834a-4444-b556-7f19a8f9dd2e" />
