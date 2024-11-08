# PIVO_BACK

PIVO_BACK — это серверное приложение, являющееся частью экосистемы, созданной для мобильного приложения, которое приглашает всех окунуться в прекрасный мир светлого и нефильтрованного пива. Это проект, направленный на то, чтобы объединить любителей пива, предоставив им доступ к информации о лучших сортах, местах дегустации и многом другом..

## Содержание

- [PIVO\_BACK](#pivo_back)
  - [Содержание](#содержание)
  - [Описание](#описание)
  - [Требования](#требования)
  - [Установка](#установка)


---

## Описание

PIVO_BACK — это серверная часть проекта, написанная с использованием **FastAPI** и **SQLAlchemy**. Сервис поддерживает работу с базой данных, хранящей информацию о местах, пиве и других связанных сущностях. Конфигурация включает в себя использование **Nginx** для обратного прокси и **Docker** для простоты развертывания.

## Требования

- **Python 3.10+**

Для деплоя:
- **Docker** 
- **Docker Compose** 

## Установка

### Локальная установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/pivo_back.git
   cd pivo_back
   pip install -r requirements.txt
    ```
2. Сконфигурируйте приложение, создав .env файл с необходимыми переменными окружения.
Программа ожидает:
- SECRET_KEY
- EMAIL_SMTP
- PASSWORD_SMTP
3. Миграции 
```
alembic revision --autogenerate -m "описание миграции"
```
Если выпадает с ошибкой удалите свою текущую базу. 
```
rm r database.db
```
4. Примените миграции
```
alembic upgrade head
```
5. Запуск
```
python -m fastapi run
```
6. API спецификация будет доступна по ссылке
```
http://127.0.0.1:8000/docs
```

### Установка с Docker

Если хотите развернуть приложение с докером, то необходимо:

1. Сконфигурируйте приложение, создав .env файл с необходимыми переменными окружения.
Программа ожидает:
- SECRET_KEY
- EMAIL_SMTP
- PASSWORD_SMTP

2. Запустите докер контейнер через bash файл:
   ```bash
   deploy.sh
    ```

PS. [API](https://api.secondmansite.ru/docs) доступно \
PPS. [Презентация пдф](https://drive.google.com/file/d/1J_Ub9y_yVkvY0QaWuQ0YlvBvPc5lvjnV/view?usp=sharing) \
PPS. [Презентация пптх](https://docs.google.com/presentation/d/19hyUFwd_cZDxeCFgi-tXrFrI4cxzA0FW/edit?usp=sharing&ouid=108248758496360302231&rtpof=true&sd=true)
