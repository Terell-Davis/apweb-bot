FROM python:3.14-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "./bot.py"]