#!/bin/bash

# Чтение переменных окружения из .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Обновление списка пакетов и установка необходимых зависимостей
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-venv python3.10-dev default-libmysqlclient-dev build-essential

# Установка pip для Python 3.10
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.10

# Установка и активация virtualenv
python3.10 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt


# Предоставление прав пользователю MySQL
mysql -h"${DB_HOST}" -uroot -p"${DB_PASSWORD}" -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';"
mysql -h"${DB_HOST}" -uroot -p"${DB_PASSWORD}" -e "GRANT ALL PRIVILEGES ON *.* TO '${DB_USER}'@'%'; FLUSH PRIVILEGES;"

# Запуск тестов
python3 manage.py test