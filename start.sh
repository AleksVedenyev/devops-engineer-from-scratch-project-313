#!/usr/bin/env bash

# Запускаем Nginx (он будет слушать порт 80, так как это дефолт для Render)
nginx & 

# Сбрасываем переменную PORT для этого процесса, чтобы Uvicorn не лез на порт 80
unset PORT

# Теперь Uvicorn послушно запустится на порту 8080
exec uv run uvicorn main:app --host 0.0.0.0 --port 8080