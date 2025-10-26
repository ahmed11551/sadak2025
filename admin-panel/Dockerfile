FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы
COPY . .

# Устанавливаем зависимости
RUN npm install --legacy-peer-deps

# Открываем порт
EXPOSE 3000

# Команда запуска
CMD ["npm", "start"]

