FROM node:20-alpine

# Рабочая директория
WORKDIR /app

# Копируем только зависимости (для кеша)
COPY frontend/package.json frontend/package-lock.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем остальной код
COPY frontend .

# Открываем порт Vite
EXPOSE 5173

# Важно для Docker (иначе HMR может не работать)
ENV CHOKIDAR_USEPOLLING=true

# Запуск dev сервера
CMD ["npm", "run", "dev", "--", "--host"]
