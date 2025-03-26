<a name="Установка и запуск"><h2>Установка и запуск:</h2></a>

Установите зависимости с помощью следующей команды:
```
pip install -r requirements.txt
```

\
Запуск всех тестов:
```
pytest --alluredir=allure-results
```

\
Команда для просмотра allure отчёта:
```
allure serve allure-results
```
