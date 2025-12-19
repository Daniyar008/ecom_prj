#!/usr/bin/env python3
import os
import sys


def main():
    # Проверяем аргументы
    if len(sys.argv) < 3:
        print(
            "Использование: python script.py <папка_для_сканирования> <файл_для_сохранения>"
        )
        print('Пример: python script.py "F:\\Deploy proj\\ecom_prj" "output.txt"')
        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = sys.argv[2]

    # Проверяем существование папки
    if not os.path.exists(input_folder):
        print(f"❌ Ошибка: Папка не найдена: {input_folder}")
        print(f"   Проверьте путь и попробуйте снова.")
        sys.exit(1)

    if not os.path.isdir(input_folder):
        print(f"❌ Ошибка: Это не папка: {input_folder}")
        sys.exit(1)

    print(f"📁 Сканирую: {input_folder}")
    print(f"💾 Сохраняю в: {output_file}")

    try:
        # Создаем директорию для выходного файла, если нужно
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Открываем файл для записи
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Структура папки: {os.path.abspath(input_folder)}\n")
            f.write("=" * 60 + "\n\n")

            # Рекурсивная функция для обхода
            def scan_dir(current_path, indent_level=0):
                indent = "    " * indent_level

                try:
                    items = os.listdir(current_path)
                except PermissionError:
                    f.write(f"{indent}[НЕТ ДОСТУПА]\n")
                    return

                # Сортируем: сначала папки, потом файлы
                items.sort(
                    key=lambda x: (
                        not os.path.isdir(os.path.join(current_path, x)),
                        x.lower(),
                    )
                )

                for item in items:
                    item_path = os.path.join(current_path, item)

                    if os.path.isdir(item_path):
                        f.write(f"{indent}{item}/\n")
                        scan_dir(item_path, indent_level + 1)
                    else:
                        f.write(f"{indent}{item}\n")

            # Начинаем сканирование
            scan_dir(input_folder)

        print(f"✅ Готово! Файл сохранен: {output_file}")
        print(f"📊 Размер файла: {os.path.getsize(output_file)} байт")

    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
