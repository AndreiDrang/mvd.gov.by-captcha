# `mvd.gov.by` math captcha solver

![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/andreidrang/mvd.gov.by-captcha-back?style=flat-square)
![](https://img.shields.io/badge/Dockerhub-link-blue?style=flat-square)

Сервис предназначен для автоматизации решения математической капчи на сайте [mvd.gov.by](https://mvd.gov.by/ru/electronicAppealLogin).
На вход сервис получает данные `SVG` изображения, в ответ выдает либо это изображение в текстовом виде, либо уже решенное выражение. 

Для получения примера капчи:
`GET` запрос на `https://mvd.gov.by/api/captcha/main`.

### Запуск
1. Для запуска нужен установленный в системе `docker` & `docker-compose`.
2. `make pull`. Выкачает образ с докер-хаба. Для билдинга локально - `make build`.
3. `make start`. Или же, для локального запуска - `make local`. Стандартно сервис запускается на `127.0.0.1:5000`.

### API

#### /math-captcha
##### /recognition

Метод преобразовывает переданные SVG данные в текстовый вид и возвращает полученное выражение.

1. *Method* - `POST, PUT`;
1. *Content-Type* - `application/json`;
1. *Payload*:
```json
{
	"data":"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"150\" height=\"50\" viewBox=\"0,0,150,50\"> .......  </svg>"
}
```
1. *Response*:
    1. Success response:
        
        *Status code* - `200`
        ```json
        {
            "data": "3 + 5",
            "result": "ok"
        }
        ```
    1. Fail responses:
    
        *204* - wrong content type;

        *500* - captcha recognition error.
        
##### /solve

Метод преобразовывает переданные SVG данные в текстовый вид и затем решает математическую капчу, возвращая готовый результат.

1. *Method* - `POST, PUT`;
1. *Content-Type* - `application/json`;
1. *Payload*:
```json
{
	"data":"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"150\" height=\"50\" viewBox=\"0,0,150,50\"> .......  </svg>"
}
```
1. *Response*:
    1. Success response:
        
        *Status code* - `200`
        ```json
        {
            "data": 8,
            "result": "ok"
        }
        ```
    1. Fail responses:
    
        *204* - wrong content type;

        *500* - captcha recognition error.
        
        
