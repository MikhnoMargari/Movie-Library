import json
import tkinter as tk
from tkinter import ttk, messagebox

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.data = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля для ввода информации о фильме
        ttk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.title_entry = ttk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.genre_entry = ttk.Entry(self.root)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.year_entry = ttk.Entry(self.root)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.rating_entry = ttk.Entry(self.root)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления фильма
        add_button = ttk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения фильмов
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

        # Фильтры
        ttk.Label(self.root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        self.genre_filter = ttk.Entry(self.root)
        self.genre_filter.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.root, text="Фильтр по году:").grid(row=6, column=2, padx=5, pady=5, sticky='e')
        self.year_filter = ttk.Entry(self.root)
        self.year_filter.grid(row=6, column=3, padx=5, pady=5, sticky='w')

        # Кнопки фильтрации
        filter_button = ttk.Button(self.root, text="Применить фильтр", command=self.apply_filter)
        filter_button.grid(row=7, column=0, padx=5, pady=10)

        reset_button = ttk.Button(self.root, text="Сбросить фильтр", command=self.load_data)
        reset_button.grid(row=7, column=1, padx=5, pady=10)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        # Валидация
        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            year_int = int(year)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом.")
            return

        try:
            rating_float = float(rating)
            if not (0 <= rating_float <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
            return

        # Добавление в таблицу
        self.tree.insert('', 'end', values=(title, genre, year_int, rating_float))
        # Добавление в список данных
        self.data.append({"Название": title, "Жанр": genre, "Год": year_int, "Рейтинг": rating_float})
        self.save_data()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def load_data(self):
        # Очистить таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Загрузить из файла
        try:
            with open('movies.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []

        # Отобразить данные
        for movie in self.data:
            self.tree.insert('', 'end', values=(movie["Название"], movie["Жанр"], movie["Год"], movie["Рейтинг"]))

    def save_data(self):
        with open('movies.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def apply_filter(self):
        genre_filter = self.genre_filter.get().lower().strip()
        year_filter = self.year_filter.get().strip()

        filtered = self.data

        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["Жанр"].lower()]

        if year_filter:
            try:
                y = int(year_filter)
                filtered = [m for m in filtered if m["Год"] == y]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтра должен быть числом.")
                return

        # Обновление таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in filtered:
            self.tree.insert('', 'end', values=(movie["Название"], movie["Жанр"], movie["Год"], movie["Рейтинг"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()