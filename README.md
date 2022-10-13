# Социальная сеть Be Social

## Социальная сеть для обмена сообщениями и фотографиями.
## Стек
<ul>- Python</ul>
<ul>- Django</ul>
<ul>- HTML</ul>
<ul>- JavaScript</ul>

## Описание

![изображение](https://user-images.githubusercontent.com/86165052/195691628-8c55d60b-c415-48f9-88c7-57c3b3b6bc63.png)

Сервис предназначен для обмена сообщениями и фотографиями. В приложении реализована аутентификация и возмоность создавать новых пользователей.

![изображение](https://user-images.githubusercontent.com/86165052/195691949-f747d1d6-d443-4f57-af4a-baf374bdc9ce.png)

На странице "Настройки аккаунта" можно загрузить фото профиля, добавить описание о себе и указать родной город.

![изображение](https://user-images.githubusercontent.com/86165052/195692126-5977b727-2af5-4833-a909-25d521c4cf6d.png)

На главное странице есть лента новостей, которая отображает только посты других пользователей, на которых мы подписаны. Также, есть отдельный раздел с рекомендациями новых пользователей.

![изображение](https://user-images.githubusercontent.com/86165052/195692329-a946b2fd-ab9d-4411-9132-f0bae5a34ce1.png)

Реализован поиск пользователей по имени, есть возможность ставить и убирать лайки, скачивать изображения.

![изображение](https://user-images.githubusercontent.com/86165052/195692427-87e69e84-1973-425d-9a51-d128489c4ffd.png)

На странице пользователя есть счетчик постов и подписчиков и кнопка "Читать", чтобы посты этого пользователя отображались в ленте.

![изображение](https://user-images.githubusercontent.com/86165052/195692530-1cf6e0c1-ce0b-45df-b866-53ebafeeab4f.png)

## Разворачивание на машине разработчика

* Клонируем [be-social](https://github.com/Nenavsegda/be-social).
* Переходим в директорию be-social и собираем образ проекта:

  ```bash
  docker build -t be-social -f docker/Dockerfile .
  ```

* Переходим в директорию docker и запускаем созданный образ:

  ```bash
  docker run --rm -p 8000:8000 be-social
  ```
  
* В браузере переходим по адресу http://127.0.0.1:8000/
