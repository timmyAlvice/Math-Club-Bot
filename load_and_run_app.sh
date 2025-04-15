#!/bin/bash

set -e

echo "Авторизация в Docker Hub..."
docker login || { echo "Ошибка авторизации! Проверьте логин и пароль."; exit 1; }

echo "Загрузка Docker-образа из Docker Hub..."
docker pull timmyalvice8/math-club-app:mvp || { echo "Ошибка загрузки образа! Проверьте имя образа."; exit 1; }

echo "Запуск контейнера из загруженного образа..."
docker run -d --name math_club_app_container -p 8080:80 timmyalvice8/math-club-app:mvp || { echo "Ошибка запуска контейнера!"; exit 1; }

echo "Контейнер успешно запущен!"
echo "Список запущенных контейнеров:"
docker ps
