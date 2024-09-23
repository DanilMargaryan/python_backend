Чтобы запустить проект, выполните следующие шаги:

1. **Клонируйте репозиторий:**

   ```bash
   git clone git@github.com:DanilMargaryan/python_backend.git
   ```

2. **Перейдите в директорию проекта:**

   ```bash
   cd python_backend
   ```

3. **Установите Poetry, если он у вас не установлен:**

   Следуйте официальной инструкции по установке Poetry: [Poetry Installation](https://python-poetry.org/docs/#installation)

4. **Установите зависимости проекта с помощью Poetry:**

   ```bash
   poetry install
   ```

5. **Активируйте виртуальное окружение Poetry:**

   ```bash
   poetry shell
   ```

6. **Запустите основной файл проекта:**

   ```bash
   python hw1/main.py
   ```

7. **Запустите тесты с помощью pytest:**

   ```bash
   pytest tests/test_homework_1.py
   ```