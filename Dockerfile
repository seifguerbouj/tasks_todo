FROM python:3.9



COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Add the rest of your application files
COPY . .

# Specify the command to run your application
CMD ["uvicorn", "app.main:app","--reload", "--host","0.0.0.0","--port", "3000"]
