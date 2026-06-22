import json
import os

DB_FILE = "series_db.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("⚠️ Помилка читання файлу даних. Створено новий список.")
        return []

def save_data(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError:
        print("⚠️ Помилка запису у файл!")

def get_valid_int(prompt, min_val=0, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"Число не може бути меншим за {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Число не може бути більшим за {max_val}.")
                continue
            return val
        except ValueError:
            print("❌ Помилка! Будь ласка, введіть коректне ціле число.")

def get_valid_status():
    statuses = {1: "Заплановано", 2: "В процесі", 3: "Переглянуто", 4: "Відкладено"}
    print("\nОберіть статус:")
    for k, v in statuses.items():
        print(f"  {k} - {v}")
    choice = get_valid_int("Ваш вибір: ", 1, 4)
    return statuses[choice]

def add_series(data):
    print("\n--- Додавання нового серіалу ---")
    title = input("Введіть назву серіалу: ").strip()
    if not title:
        print("❌ Назва не може бути порожньою!")
        return
    
    seasons = get_valid_int("Кількість переглянутих сезонів: ")
    episodes = get_valid_int("Кількість переглянутих серій: ")
    status = get_valid_status()
    rating = get_valid_int("Введіть оцінку (від 1 до 10, або 0 якщо без оцінки): ", 0, 10)
    
    series = {
        "title": title,
        "watched_seasons": seasons,
        "watched_episodes": episodes,
        "status": status,
        "rating": rating if rating != 0 else None
    }
    
    data.append(series)
    save_data(data)
    print(f"✅ Серіал '{title}' успішно додано!")

def show_series(data, filtered_data=None):
    target_data = filtered_data if filtered_data is not None else data
    if not target_data:
        print("\nСписок порожній.")
        return

    print("\n" + "="*75)
    print(f"{'Назва':<25} | {'Сезони':<8} | {'Серії':<6} | {'Статус':<15} | {'Оцінка':<6}")
    print("="*75)
    for s in target_data:
        rating_str = str(s['rating']) if s['rating'] is not None else "-"
        print(f"{s['title']:<25} | {s['watched_seasons']:<8} | {s['watched_episodes']:<6} | {s['status']:<15} | {rating_str:<6}")
    print("="*75)

def filter_by_status(data):
    if not data:
        print("\nБаза даних порожня. Немає що фільтрувати.")
        return
    status = get_valid_status()
    filtered = [s for s in data if s['status'] == status]
    print(f"\nФільтр за статусом: '{status}'")
    show_series(data, filtered)

def calculate_average_rating(data):
    ratings = [s['rating'] for s in data if s['rating'] is not None]
    if not ratings:
        print("\n📊 Немає оцінених серіалів для підрахунку середнього балу.")
        return
    
    avg_rating = sum(ratings) / len(ratings)
    print(f"\n📊 Середня оцінка ваших серіалів: {avg_rating:.2f} / 10 (всього оцінено: {len(ratings)})")

def main():
    data = load_data()
    while True:
        print("\n=== МЕНЕДЖЕР КАТАЛОГУ СЕРІАЛІВ ===")
        print("1. Переглянути всі серіали")
        print("2. Додати новий серіал")
        print("3. Фільтрувати за статусом")
        print("4. Показати середню оцінку")
        print("5. Вийти з програми")
        
        choice = input("Оберіть дію (1-5): ").strip()
        
        if choice == "1":
            show_series(data)
        elif choice == "2":
            add_series(data)
        elif choice == "3":
            filter_by_status(data)
        elif choice == "4":
            calculate_average_rating(data)
        elif choice == "5":
            print("👋 До побачення! Дані збережено.")
            break
        else:
            print("❌ Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()