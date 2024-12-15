from datetime import datetime
from functools import reduce

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        self.history = []
        self.created_at = datetime.now()

# Списки пользователей и книг
users = [
    User("Пользователь", "1234567890", "Пользователь"),
    User("Админ", "0987654321", "Админ"),
]

books = [
    {"title": "Маленький принц", "author": "Антуан де Сент-Экзюпери", "genre": "Сказка"},
    {"title": "Война и мир", "author": "Лев Толстой", "genre": "Роман-Эппопея"},
    {"title": "1984", "author": "Джордж Оруэлл", "genre": "Антиутопия"},
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Фантастика"},
    {"title": "Дубровский", "author": "Александр Пушкин", "genre": "Роман"},
    {"title": "Девочка со спичками", "author": "Ханс Кристиан Андерсен", "genre": "Сказка"},
    {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "genre": "Психологический роман"},
    {"title": "Убийства на улице Морг", "author": "Эдгар Аллан По", "genre": "Детектив"}
]

current_user = None 

def authorize_user():
    global current_user
    username = input("Логин: ")
    password = input("Пароль: ")

    for user in users:
        if user.username == username and user.password == password:
            current_user = user
            print(f"Выполнен вход, {current_user.username} ({current_user.role})!")
            return True
    print("Неверный логин или пароль.")
    return False 

def main_menu():
    while True:
        print("\nГлавное меню:")
        print("1. Просмотреть книги")
        print("2. Фильтрация книг")
        print("3. Сортировка книг")
        if current_user.role == "Админ":
            print("4. Добавить книгу")
            print("5. Удалить книгу")
            print("6. Обновить данные книги")
            print("7. Просмотреть пользователей")
            print("8. Выход")
        else:
            print("4. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                view_books()
            elif choice == "2":
                filter_books()
            elif choice == "3":
                sort_books()
            elif choice == "4" and current_user.role == "Админ":
                add_book()
            elif choice == "5" and current_user.role == "Админ":
                remove_book()
            elif choice == "6" and current_user.role == "Админ":
                update_book()
            elif choice == "7" and current_user.role == "Админ":
                view_users()
            elif choice == "8" and current_user.role == "Админ":
                break
            elif choice == "4" and current_user.role == "Пользователь":
                break
            else:
                print("Некорректный выбор. Попробуйте снова.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

def view_books():
    print("\nДоступные книги:")
    # Используем map для форматирования вывода
    formatted_books = map(lambda book: f"- {book['title']} ({book['author']}, {book['genre']})", books)
    print("\n".join(formatted_books))

def add_book():
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    genre = input("Введите жанр книги: ")

    books.append({"title": title, "author": author, "genre": genre})
    print("Книга успешно добавлена!")

def remove_book():
    title = input("Введите название книги для удаления: ")
    book_to_remove = next((book for book in books if book['title'].lower() == title.lower()), None)

    if book_to_remove:
        books.remove(book_to_remove)
        print("Книга успешно удалена!")
    else:
        print("Книга не найдена.")

def update_book():
    title = input("Введите название книги для обновления: ")
    book_to_update = next((book for book in books if book['title'].lower() == title.lower()), None)

    if book_to_update:
        new_title = input("Введите новое название книги (или нажмите Enter для сохранения): ")
        new_author = input("Введите нового автора книги (или нажмите Enter для сохранения): ")
        new_genre = input("Введите новый жанр книги (или нажмите Enter для сохранения): ")

        if new_title:
            book_to_update['title'] = new_title
        if new_author:
            book_to_update['author'] = new_author
        if new_genre:
            book_to_update['genre'] = new_genre

        print("Данные книги успешно обновлены!")
    else:
        print("Книга не найдена.")

def filter_books():
    criteria = input("Введите критерии фильтрации (title, author, genre): ").lower()
    if criteria not in ['title', 'author', 'genre']:
        print("Некорректный критерий. Попробуйте снова.")
        return

    value = input(f"Введите значение для фильтрации по '{criteria}': ").lower()

    filtered_books = list(filter(lambda book: book[criteria].lower() == value, books))

    if filtered_books:
        print("\nОтфильтрованные книги:")
        # Используем map для форматирования вывода
        formatted_books = map(lambda book: f"- {book['title']} ({book['author']}, {book['genre']})", filtered_books)
        print("\n".join(formatted_books))
    else:
        print("Книги не найдены по заданным критериям.")

def sort_books():
    criteria = input("Введите критерий сортировки (title, author, genre): ").lower()

    if criteria in ['title', 'author', 'genre']:
        sorted_books = sorted(books, key=lambda x: x[criteria].lower())
        print("\nОтсортированные книги:")
        # Используем map для форматирования вывода
        formatted_books = map(lambda book: f"- {book['title']} ({book['author']}, {book['genre']})", sorted_books)
        print("\n".join(formatted_books))
    else:
        print("Некорректный критерий сортировки.")

def view_users():
    print("\nСписок пользователей:")
    # Используем zip для создания пар (имя пользователя, роль)
    user_info = zip([user.username for user in users], [user.role for user in users])
    for username, role in user_info:
        print(f"- {username} (Роль: {role})")

if __name__ == "__main__":
    if authorize_user():
        main_menu()