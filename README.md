**mcr_srv_pract** — учебный проект с микросервисной архитектурой для сервиса доставки еды.

## Структура проекта
```
mcr_srv_pract/
│
├── product_srv/     
│   ├── main.py       
│   ├── models.py     
│   └── Dockerfile    
│
├── delivery_srv/     
│   ├── main.py
│   ├── models.py
│   └── Dockerfile
│
├── order_srv/        
│   ├── main.py
│   ├── models.py
│   └── Dockerfile
│
├── docker-compose.yml   
└── README.md
```
**Доступ к сервисам**
    - Продукты: http://localhost:8001  
    - Доставка: http://localhost:8002  
    - Заказы: http://localhost:8003

## Краткое описание сервисов

- **product_srv:**  
  Управляет ассортиментом продуктов, их параметрами, ценами.

- **delivery_srv:**  
  Отвечает за обработку информации о доставке, маршрутизации, статусы курьеров.

- **order_srv:**  
  Обрабатывает оформление заказов, их статусы, взаимодействие с остальными сервисами.

## Организация кода внутри сервисов
В каждом сервисе используются стандартные файлы:
- `main.py` — точка входа приложения 
- `models.py` — модели данных 
- `Dockerfile` — инструкция для сборки контейнера.
- 
## Технологии

- Python 
- FastAPI 
- Docker, Docker Compose
- PostgreSQL

## Автор
- [EmiliaShh](https://github.com/EmiliaShh)