# Описание | Уровень | Категория

## Информация

> Текст, который будет приложен к заданию
>
> Если нужно - указываем сразу строку подключения (nc или http или что-то еще)
> http://<ip>:3355

## Деплой

Указываем команду необходимую для запуска задачи на сервере

```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Архив из директории [public/](public/) и IP:PORT сервера

## Описание

Краткое описание сути задачи от автора

## Решение

Подробное решение от автора

[Эксплоит](solve/solve.py)

## Флаг

`ExampleFlag`
