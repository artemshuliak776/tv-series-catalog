import json
import os

# Константи для статусів
STATUSES = {
    "1": "Дивлюсь",
    "2": "Пройдено/Переглянуто",
    "3": "Відкладено"
}
FILE_NAME = "series_data.json"

def load_data():
    """Завантажує дані з файлу JSON. Якщо файлу немає, повертає порожній список."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, PermissionError):
        print("[Помилка] Не вдалося зчитати файл даних. Створено новий каталог.")
        return []

def save_data(data):
    """Зберігає дані у файл JSON."""
    try:
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[Помилка] Не вдалося зберегти дані: {e}")

def get_int_input(prompt, min_val=None, max_val=None):
    """Безпечне зчитування цілого числа з валідацією."""
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Помилка: значення не може бути меншим за {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Помилка: значення не може бути більшим за {max_val}.")
                continue
            return val
        except ValueError:
            print("Некоректний ввід! Будь ласка, введіть ціле число.")

def get_status_input():
    """Діалог вибору статусу серіалу."""
    print("\nОберіть статус серіалу:")
    for key, value in STATUSES.items():
        print(f"  {key}. {value}")
    while True:
        choice = input("Ваш вибір (1-3): ").strip()
        if choice in STATUSES:
            return STATUSES[choice]
        print("Некоректний вибір. Спробуйте ще раз.")

# --- ФУНКЦІОНАЛЬНІСТЬ ВАРІАНТУ ---

def add_series(data):
    """Функція 1: Додавання серіалу"""
    print("\n=== ДОДАВАННЯ НОВОГО СЕРІАЛУ ===")
    name = input("Введіть назву серіалу: ").strip()
    while not name:
        print("Назва не може бути порожньою!")
        name = input("Введіть назву серіалу: ").strip()
        
    seasons = get_int_input("Кількість переглянутих сезонів: ", min_val=0)
    episodes = get_int_input("Кількість переглянутих серій: ", min_val=0)
    status = get_status_input()
    score = get_int_input("Ваша оцінка (від 1 до 10): ", min_val=1, max_val=10)
    
    new_series = {
        "title": name,
        "seasons": seasons,
        "episodes": episodes,
        "status": status,
        "score": score
    }
    
    data.append(new_series)
    save_data(data)
    print(f"✔ Серіал '{name}' успішно додано до каталогу!")

def print_table(series_list):
    """Допоміжна функція для гарного виведення списку у вигляді таблиці."""
    if not series_list:
        print("Список порожній.")
        return
        
    print("\n" + "="*85)
    print(f"{'№':<3} | {'Назва серіалу':<30} | {'Сезони/Серії':<12} | {'Статус':<20} | {'Оцінка':<6}")
    print("="*85)
    for idx, item in enumerate(series_list, 1):
        progress = f"S{item['seasons']} / E{item['episodes']}"
        print(f"{idx:<3} | {item['title'][:30]:<30} | {progress:<12} | {item['status']:<20} | {item['score']:<6}")
    print("="*85)

def filter_by_status(data):
    """Функція 2: Фільтрація за статусом"""
    print("\n=== ФІЛЬТРАЦІЯ ЗА СТАТУСОМ ===")
    status_to_filter = get_status_input()
    
    filtered = [item for item in data if item['status'] == status_to_filter]
    
    print(f"\nРезультати фільтрації за статусом '{status_to_filter}':")
    print_table(filtered)

def calculate_average_score(data):
    """Функція 3: Середня оцінка"""
    print("\n=== СЕРЕДНЯ ОЦІНКА КАТАЛОГУ ===")
    if not data:
        print("Каталог порожній. Немає оцінок для розрахунку.")
        return
        
    total_score = sum(item['score'] for item in data)
    avg_score = total_score / len(data)
    
    print(f"Загальна кількість серіалів в базі: {len(data)}")
    print(f"📊 Середня оцінка вашого каталогу: {avg_score:.2f} / 10")

def view_all_series(data):
    """Функція 4: Перегляд усіх серіалів"""
    print("\n=== УСІ СЕРІАЛИ В КАТАЛОЗІ ===")
    print_table(data)


# --- ГОЛОВНЕ МЕНЮ ---

def main():
    # Завантажуємо актуальні дані з JSON при старті
    catalog = load_data()
    
    while True:
        print("\n--- МЕНЕДЖЕР КАТАЛОГУ СЕРІАЛІВ ---")
        print("1. Переглянути всі серіали")
        print("2. Додати новий серіал")
        print("3. Фільтрувати за статусом")
        print("4. Порахувати середню оцінку")
        print("5. Вихід")
        
        choice = input("Оберіть дію (1-5): ").strip()
        
        if choice == "1":
            view_all_series(catalog)
        elif choice == "2":
            add_series(catalog)
        elif choice == "3":
            filter_by_status(catalog)
        elif choice == "4":
            calculate_average_score(catalog)
        elif choice == "5":
            print("\nДякуємо за використання утиліти! Дані збережено. Бувай!")
            break
        else:
            print("Некоректний пункт меню. Оберіть число від 1 до 5.")

if __name__ == "__main__":
    main()
    import json

test_data = [
    {
        "title": "Пуститися берега (Breaking Bad)",
        "seasons": 5,
        "episodes": 62,
        "status": "Пройдено/Переглянуто",
        "score": 10
    },
    {
        "title": "Дивні дива (Stranger Things)",
        "seasons": 4,
        "episodes": 34,
        "status": "Дивлюсь",
        "score": 9
    },
    {
        "title": "Відьмак (The Witcher)",
        "seasons": 3,
        "episodes": 24,
        "status": "Відкладено",
        "score": 6
    },
    {
        "title": "Шерлок (Sherlock)",
        "seasons": 4,
        "episodes": 13,
        "status": "Пройдено/Переглянуто",
        "score": 10
    },
    {
        "title": "Мандалорець",
        "seasons": 3,
        "episodes": 24,
        "status": "Дивлюсь",
        "score": 8
    },
    {
        "title": "Хлопаки (The Boys)",
        "seasons": 4,
        "episodes": 32,
        "status": "Відкладено",
        "score": 9
    }
]

FILE_NAME = "series_data.json"

try:
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)
    print("==================================================")
    print(f"✔ Файл '{FILE_NAME}' !")
    print("==================================================")
except Exception as e:
    print(f"Помилка: {e}")
