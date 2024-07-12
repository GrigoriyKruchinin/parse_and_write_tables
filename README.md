# HTML Table Extractor and Transformer
Этот проект предназначен для автоматического извлечения таблиц из HTML-файлов, их трансформации в соответствии с заданными правилами технического задания и записи в формате DOCX.

## Установка проекта через requirements.txt

1. Клонируйте репозиторий:

```
git clone https://github.com/GrigoriyKruchinin/parse_and_write_tables.git
```
2. Перейдите в каталог проекта:

```
cd parse_and_write_tables
```

3. Создайте виртуальное окружение:

```
python -m venv .venv
```

4. Активируйте виртуальное окружение:

```
source .venv/bin/activate
```

5. Установите зависимости:

```
pip install -r requirements.txt
```


## Установка проекта через Poetry

Так же вы можете воспользоваться альтернативным и более удобным способом установки зависимостей.
Убедитесь, что у вас установлен Poetry. Если нет, установите его, следуя инструкциям на официальном сайте.

1. Клонируйте репозиторий:

```
git clone https://github.com/GrigoriyKruchinin/parse_and_write_tables.git
```
2. Перейдите в каталог проекта:

```
cd parse_and_write_tables
```

3. Активируйте виртуальное окружение с помощью Poetry:

```
poetry shell
```

4. Установите зависимости с помощью Poetry:

```
poetry install
```

## Запуск основного приложения
Для запуска основного приложения выполните следующую команду:

```
make start
```

Эта команда выполнит основную функцию проекта, обрабатывая HTML-файлы, извлекая таблицы, трансформируя их и записывая результаты в DOCX файлы.

Перейдите в созданную папку output_data и ознакомтесь с ее содержимым. 

## Благодарность и контакты

Буду рад обратной связи!

- Автор: Grigoriy Kruchinin
- [GitHub](https://github.com/GrigoriyKruchinin)
- [Email](mailto:gkruchinin75@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/grigoriy-kruchinin/)