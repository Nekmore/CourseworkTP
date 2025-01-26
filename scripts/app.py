import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Подключение к базе данных MySQL
db = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="0000",  
    database="auto_service"
)
cursor = db.cursor()

# Функции для работы с базой данных

def add_master(first_name, last_name, specialization, experience_years, phone_number):
    try:
        query = """
        INSERT INTO masters (first_name, last_name, specialization, experience_years, phone_number) 
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, specialization, experience_years, phone_number)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Успех", f"Мастер {first_name} {last_name} добавлен.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка добавления мастера: {err}")
    


def update_master(master_id, first_name, last_name, specialization, experience_years, phone_number):
    try:
        query = """
        UPDATE masters 
        SET first_name=%s, last_name=%s, specialization=%s, experience_years=%s, phone_number=%s 
        WHERE id=%s
        """
        values = (first_name, last_name, specialization, experience_years, phone_number, master_id)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Успех", "Данные мастера обновлены.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка обновления мастера: {err}")


def delete_master(master_id):
    try:
        query = "DELETE FROM masters WHERE id=%s"
        cursor.execute(query, (master_id,))
        db.commit()
        messagebox.showinfo("Успех", "Мастер удален.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка удаления мастера: {err}")


def add_car(registration_number, brand, model):
    try:
        query = """
        INSERT INTO cars (registration_number, brand, model) 
        VALUES (%s, %s, %s)
        """
        values = (registration_number, brand, model)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Успех", f"Автомобиль {brand} {model} добавлен.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка добавления автомобиля: {err}")


def update_car(car_id, registration_number, brand, model):
    try:
        query = """
        UPDATE cars 
        SET registration_number=%s, brand=%s, model=%s 
        WHERE car_id=%s
        """
        values = (registration_number, brand, model, car_id)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Успех", "Данные автомобиля обновлены.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка обновления автомобиля: {err}")
    


def delete_car(car_id):
    try:
        query = "DELETE FROM cars WHERE car_id=%s"
        cursor.execute(query, (car_id,))
        db.commit()
        messagebox.showinfo("Успех", "Автомобиль удален.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка удаления автомобиля: {err}")


def add_work(car_id, master_id, problem_description, work_description, hours_worked, hourly_rate):
    try:
        query = """
        INSERT INTO works (car_id, master_id, problem_description, work_description, hours_worked, hourly_rate) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (car_id, master_id, problem_description, work_description, hours_worked, hourly_rate)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Успех", "Работа успешно добавлена.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка добавления работы: {err}")


def update_work(work_id, car_id, master_id, problem_description, work_description, hours_worked, hourly_rate):
    try:
        query = """
        UPDATE works 
        SET car_id=%s, master_id=%s, problem_description=%s, work_description=%s, hours_worked=%s, hourly_rate=%s 
        WHERE work_id=%s
        """
        values = (car_id, master_id, problem_description, work_description, hours_worked, hourly_rate, work_id)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Успех", "Данные работы обновлены.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка обновления работы: {err}")


def delete_work(work_id):
    try:
        query = "DELETE FROM works WHERE work_id=%s"
        cursor.execute(query, (work_id,))
        db.commit()
        messagebox.showinfo("Успех", "Работа удалена.")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка удаления работы: {err}")


def generate_report(registration_number):
    try:
        cursor.execute("SELECT id FROM cars WHERE registration_number=%s", (registration_number,))
        car = cursor.fetchone()
        if not car:
            messagebox.showerror("Ошибка", "Автомобиль с таким регистрационным номером не найден.")
            return
        car_id = car[0]

        cursor.execute("""
        SELECT works.problem_description, works.work_description, 
               works.hours_worked * works.hourly_rate AS earnings,
               CONCAT(masters.first_name, ' ', masters.last_name) AS master_name
        FROM works
        JOIN masters ON works.master_id = masters.id
        WHERE works.car_id=%s
        """, (car_id,))
        works = cursor.fetchall()

        total_earnings = 0
        report_text = f"Отчет по автомобилю {registration_number}:\n\n"

        for work in works:
            problem_description, work_description, earnings, master_name = work
            total_earnings += earnings
            report_text += f"- Мастер: {master_name}, Проблема: {problem_description}, Решение: {work_description}, Заработок: {earnings} руб.\n"

        report_text += f"\nОбщая сумма заработка: {total_earnings} руб."
        messagebox.showinfo("Отчет", report_text)
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка генерации отчета: {err}")


# Функции обновления интерфейса
def update_masters_view():
    """Обновление списка мастеров."""
    for row in tree_masters.get_children():
        tree_masters.delete(row)
    cursor.execute("SELECT * FROM masters")
    masters = cursor.fetchall()
    for master in masters:
        tree_masters.insert("", "end", values=(master[0], master[1], master[2], master[3], master[4], master[5]))


def update_cars_view():
    """Обновление списка автомобилей."""
    for row in tree_cars.get_children():
        tree_cars.delete(row)
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    for car in cars:
        tree_cars.insert("", "end", values=(car[0], car[1], car[2], car[3]))


def update_works_view():
    """Обновление списка выполненных работ."""
    for row in tree_works.get_children():
        tree_works.delete(row)
    cursor.execute("""
        SELECT works.id, cars.registration_number, CONCAT(masters.first_name, ' ', masters.last_name),
               works.problem_description, works.work_description, works.hours_worked, works.hourly_rate,
               works.hours_worked * works.hourly_rate AS total_cost
        FROM works
        JOIN cars ON works.car_id = cars.id
        JOIN masters ON works.master_id = masters.id
    """)
    works = cursor.fetchall()
    for work in works:
        tree_works.insert("", "end", values=work)

# Создание графического интерфейса
root = tk.Tk()
root.title("Система управления автосервисом")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Вкладка добавления данных
frame_add = ttk.Frame(notebook)
notebook.add(frame_add, text="Добавить данные")

# Вкладка отчета
frame_report = ttk.Frame(notebook)
notebook.add(frame_report, text="Отчет")

# Вкладка просмотра мастеров
frame_masters = ttk.Frame(notebook)
notebook.add(frame_masters, text="Мастера")

# Вкладка просмотра автомобилей
frame_cars = ttk.Frame(notebook)
notebook.add(frame_cars, text="Автомобили")

# Вкладка просмотра работ
frame_works = ttk.Frame(notebook)
notebook.add(frame_works, text="Работы")

def on_add_master_button_click():
    # Получаем значения из полей ввода
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    middle_name = entry_middle_name.get()
    grade = entry_grade.get()
    specialization = entry_specialization.get()

    # Вызываем функцию add_master с полученными значениями
    add_master(first_name, last_name, middle_name, grade, specialization)
    update_masters_view()

frame_add_master = ttk.Labelframe(frame_add, text="Добавить мастера")
frame_add_master.pack(fill="x", padx=10, pady=5)

tk.Label(frame_add_master, text="Имя:").grid(row=0, column=0)
entry_first_name = ttk.Entry(frame_add_master)
entry_first_name.grid(row=0, column=1)

tk.Label(frame_add_master, text="Фамилия:").grid(row=1, column=0)
entry_last_name = ttk.Entry(frame_add_master)
entry_last_name.grid(row=1, column=1)

tk.Label(frame_add_master, text="Специализация:").grid(row=2, column=0)
entry_middle_name = ttk.Entry(frame_add_master)
entry_middle_name.grid(row=2, column=1)

tk.Label(frame_add_master, text="Разряд:").grid(row=3, column=0)
entry_grade = ttk.Entry(frame_add_master)
entry_grade.grid(row=3, column=1)

tk.Label(frame_add_master, text="Номер телефона:").grid(row=4, column=0)
entry_specialization = ttk.Entry(frame_add_master)
entry_specialization.grid(row=4, column=1)

btn_add_master = ttk.Button(frame_add_master, text="Добавить", command=on_add_master_button_click)
btn_add_master.grid(row=5, columnspan=2, pady=5)

# Добавление автомобиля

frame_add_car = ttk.Labelframe(frame_add, text="Добавить автомобиль")
frame_add_car.pack(fill="x", padx=10, pady=5)

tk.Label(frame_add_car, text="Регистрационный номер:").grid(row=0, column=0)
entry_brand = ttk.Entry(frame_add_car)
entry_brand.grid(row=0, column=1)

tk.Label(frame_add_car, text="Марка:").grid(row=1, column=0)
entry_year = ttk.Entry(frame_add_car)
entry_year.grid(row=1, column=1)

tk.Label(frame_add_car, text="Модель:").grid(row=2, column=0)
entry_registration_number = ttk.Entry(frame_add_car)
entry_registration_number.grid(row=2, column=1)

btn_add_car = ttk.Button(frame_add_car, text="Добавить", command=add_car)
btn_add_car.grid(row=3, columnspan=2, pady=5)

# Добавление работы

frame_add_work = ttk.Labelframe(frame_add, text="Добавить выполненную работу")
frame_add_work.pack(fill="x", padx=10, pady=5)

tk.Label(frame_add_work, text="Регистрационный номер машины:").grid(row=0, column=0)
entry_work_car_reg = ttk.Entry(frame_add_work)
entry_work_car_reg.grid(row=0, column=1)

tk.Label(frame_add_work, text="Мастер:").grid(row=1, column=0)
entry_work_master_id = ttk.Entry(frame_add_work)
entry_work_master_id.grid(row=1, column=1)

tk.Label(frame_add_work, text="Описание проблемы:").grid(row=2, column=0)
entry_work_hours = ttk.Entry(frame_add_work)
entry_work_hours.grid(row=2, column=1)

tk.Label(frame_add_work, text="Описание работы:").grid(row=3, column=0)
entry_work_rate = ttk.Entry(frame_add_work)
entry_work_rate.grid(row=3, column=1)

tk.Label(frame_add_work, text="Часы работы:").grid(row=4, column=0)
entry_work_problem = ttk.Entry(frame_add_work)
entry_work_problem.grid(row=4, column=1)

tk.Label(frame_add_work, text="Ставка в час:").grid(row=5, column=0)
entry_work_description = ttk.Entry(frame_add_work)
entry_work_description.grid(row=5, column=1)

btn_add_work = ttk.Button(frame_add_work, text="Добавить работу", command=add_work)
btn_add_work.grid(row=6, columnspan=2, pady=5)


# Элементы для просмотра мастеров
frame_masters_view = ttk.Frame(frame_masters)
frame_masters_view.pack(fill="both", expand=True, padx=10, pady=5)

def on_update_master_button_click():
    # Получаем значения из полей ввода
    master_id = entry_master_id.get()
    first_name = entry_edit_first_name.get()
    last_name = entry_edit_last_name.get()
    specialization = entry_edit_specialization.get()
    grade = entry_edit_grade.get()
    number = entry_edit_number.get()
    print(master_id)
    # Вызываем функцию update_master с полученными значениями
    update_master(master_id, first_name, last_name, specialization, grade, number)
    update_masters_view()

def on_delete_master_button_click():
    # Получаем значения из полей ввода
    master_id = entry_master_id.get()

    # Вызываем функцию delete_master с полученными значениями
    delete_master(master_id)
    update_masters_view()

scrollbar_masters = ttk.Scrollbar(frame_masters_view, orient="vertical")
tree_masters = ttk.Treeview(frame_masters_view, columns=("ID", "Имя", "Фамилия", "Специализация", "Разряд", "Номер телефона"), show="headings", yscrollcommand=scrollbar_masters.set)
scrollbar_masters.config(command=tree_masters.yview)
scrollbar_masters.pack(side="right", fill="y")

tree_masters.heading("ID", text="ID")
tree_masters.heading("Имя", text="Имя")
tree_masters.heading("Фамилия", text="Фамилия")
tree_masters.heading("Специализация", text="Специализация")
tree_masters.heading("Разряд", text="Разряд")
tree_masters.heading("Номер телефона", text="Номер телефона")
tree_masters.pack(fill="both", expand=True)

frame_edit_master = ttk.Labelframe(frame_masters, text="Изменение/Удаление мастера")
frame_edit_master.pack(fill="x", padx=10, pady=5)

tk.Label(frame_edit_master, text="ID мастера:").grid(row=0, column=0)
entry_master_id = ttk.Entry(frame_edit_master)
entry_master_id.grid(row=0, column=1)

tk.Label(frame_edit_master, text="Имя:").grid(row=1, column=0)
entry_edit_first_name = ttk.Entry(frame_edit_master)
entry_edit_first_name.grid(row=1, column=1)

tk.Label(frame_edit_master, text="Фамилия:").grid(row=2, column=0)
entry_edit_last_name = ttk.Entry(frame_edit_master)
entry_edit_last_name.grid(row=2, column=1)

tk.Label(frame_edit_master, text="Специализация:").grid(row=3, column=0)
entry_edit_specialization = ttk.Entry(frame_edit_master)
entry_edit_specialization.grid(row=3, column=1)

tk.Label(frame_edit_master, text="Разряд:").grid(row=4, column=0)
entry_edit_grade = ttk.Entry(frame_edit_master)
entry_edit_grade.grid(row=4, column=1)

tk.Label(frame_edit_master, text="Номер телефона:").grid(row=5, column=0)
entry_edit_number = ttk.Entry(frame_edit_master)
entry_edit_number.grid(row=5, column=1)

btn_update_master = ttk.Button(frame_edit_master, text="Изменить", command=on_update_master_button_click)
btn_update_master.grid(row=6, column=0, pady=5)

btn_delete_master = ttk.Button(frame_edit_master, text="Удалить", command=on_delete_master_button_click)
btn_delete_master.grid(row=6, column=1, pady=5)

# Элементы для просмотра автомобилей
tree_cars = ttk.Treeview(frame_cars, columns=("ID", "Регистрационный номер", "Марка", "Модель"), show="headings")
tree_cars.heading("ID", text="ID")
tree_cars.heading("Регистрационный номер", text="Регистрационный номер")
tree_cars.heading("Марка", text="Марка")
tree_cars.heading("Модель", text="Модель")
tree_cars.pack(fill="both", expand=True)

frame_edit_car = ttk.Labelframe(frame_cars, text="Изменение/Удаление автомобиля")
frame_edit_car.pack(fill="x", padx=10, pady=5)

tk.Label(frame_edit_car, text="ID автомобиля:").grid(row=0, column=0)
entry_car_id = ttk.Entry(frame_edit_car)
entry_car_id.grid(row=0, column=1)

tk.Label(frame_edit_car, text="Регистрационный номер:").grid(row=1, column=0)
entry_car_brand = ttk.Entry(frame_edit_car)
entry_car_brand.grid(row=1, column=1)

tk.Label(frame_edit_car, text="Марка:").grid(row=2, column=0)
entry_car_year = ttk.Entry(frame_edit_car)
entry_car_year.grid(row=2, column=1)

tk.Label(frame_edit_car, text="Модель:").grid(row=3, column=0)
entry_car_number = ttk.Entry(frame_edit_car)
entry_car_number.grid(row=3, column=1)

btn_update_car = ttk.Button(frame_edit_car, text="Изменить", command=update_car)
btn_update_car.grid(row=4, column=0, pady=5)

btn_delete_car = ttk.Button(frame_edit_car, text="Удалить", command=delete_car)
btn_delete_car.grid(row=4, column=1, pady=5)

# Элементы для просмотра работ
frame_works_view = ttk.Frame(frame_works)
frame_works_view.pack(fill="both", expand=True, padx=10, pady=5)

scrollbar_works = ttk.Scrollbar(frame_works_view, orient="vertical")
tree_works = ttk.Treeview(frame_works_view, columns=("Id работы", "Номер машины", "Мастер", "Описание проблемы", "Описание работы", "Часы", "Ставка"), show="headings", yscrollcommand=scrollbar_works.set)
scrollbar_works.config(command=tree_works.yview)
scrollbar_works.pack(side="right", fill="y")

tree_works.heading("Id работы", text="Id работы")
tree_works.heading("Номер машины", text="Номер машины")
tree_works.heading("Мастер", text="Мастер")
tree_works.heading("Описание проблемы", text="Описание проблемы")
tree_works.heading("Описание работы", text="Описание работы")
tree_works.heading("Часы", text="Часы")
tree_works.heading("Ставка", text="Ставка")
tree_works.pack(fill="both", expand=True)

# Элементы для просмотра работ с возможностью изменения и удаления
frame_edit_work = ttk.Labelframe(frame_works, text="Изменение/Удаление работы")
frame_edit_work.pack(fill="x", padx=10, pady=5)

# Поля для ввода данных о работе
tk.Label(frame_edit_work, text="ID работы:").grid(row=0, column=0)
entry_work_id = ttk.Entry(frame_edit_work)
entry_work_id.grid(row=0, column=1)

# Поля для изменения данных

# Машина
tk.Label(frame_edit_work, text="Машина:").grid(row=1, column=0)
entry_work_car = ttk.Entry(frame_edit_work)
entry_work_car.grid(row=1, column=1)

# Мастер
tk.Label(frame_edit_work, text="Мастер:").grid(row=2, column=0)
entry_work_master = ttk.Entry(frame_edit_work)
entry_work_master.grid(row=2, column=1)

# Описание проблемы
tk.Label(frame_edit_work, text="Описание проблемы:").grid(row=3, column=0)
entry_work_problem = ttk.Entry(frame_edit_work)
entry_work_problem.grid(row=3, column=1)

# Описание работы
tk.Label(frame_edit_work, text="Описание работы:").grid(row=4, column=0)
entry_work_description = ttk.Entry(frame_edit_work)
entry_work_description.grid(row=4, column=1)

# Часы работы
tk.Label(frame_edit_work, text="Часы:").grid(row=5, column=0)
entry_work_hours = ttk.Entry(frame_edit_work)
entry_work_hours.grid(row=5, column=1)

# Ставка
tk.Label(frame_edit_work, text="Ставка:").grid(row=6, column=0)
entry_work_rate = ttk.Entry(frame_edit_work)
entry_work_rate.grid(row=6, column=1)

# Функции для обработки изменений и удаления
def submit_update_work():
    update_work(
        entry_work_id.get(),
        entry_work_car.get(),
        entry_work_master.get(),
        entry_work_problem.get(),
        entry_work_description.get(),
        entry_work_hours.get(),
        entry_work_rate.get()
    )
    update_works_view()

def submit_delete_work():
    delete_work(entry_work_id.get())
    update_works_view()

# Кнопки для изменения и удаления работы
btn_update_work = ttk.Button(frame_edit_work, text="Изменить", command=submit_update_work)
btn_update_work.grid(row=7, column=0, pady=5)

btn_delete_work = ttk.Button(frame_edit_work, text="Удалить", command=submit_delete_work)
btn_delete_work.grid(row=7, column=1, pady=5)

# Элементы для формирования отчета
frame_generate_report = ttk.Labelframe(frame_report, text="Создать отчет по автомобилю")
frame_generate_report.pack(fill="x", padx=10, pady=5)

tk.Label(frame_generate_report, text="Регистрационный номер:").grid(row=0, column=0, padx=5, pady=5)
entry_report_car_number = ttk.Entry(frame_generate_report)
entry_report_car_number.grid(row=0, column=1, padx=5, pady=5)

def submit_report():
    generate_report(entry_report_car_number.get())

btn_generate_report = ttk.Button(frame_generate_report, text="Создать отчет", command=submit_report)
btn_generate_report.grid(row=1, columnspan=2, pady=10)


# Начальная загрузка данных
update_masters_view()
update_cars_view()
update_works_view()

root.mainloop()
