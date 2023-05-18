# DataSync
A django based project which syncs your local database with that of stripe with each API call made to either of them using celery task queue.

Link to API Documentation - https://docs.google.com/document/d/13BBRdo5hFQpRiKVkWh1xOGqyN6uyv7pwhd8gRZUTLgE/edit?usp=sharing

Steps to run the project:
1. Create and activate virtualenvironment
2. Install the necessay dependencies from requirements.txt using the command "pip3 install -r requirements.txt"
3. Make sure you have rabbitmq server up and running at localhost:5672, if some other url/port then add the url and port as
   CELERY_BROKER_URL = url 
   in the settings.py file inside DataSync folder.
3. Run migrations using these 2 commands:
    a. "python3 manage.py makemigrations"
    b. "python3 manage.py migrate"
4. Run celery in a seperate terminal using the command "celery -A DataSync worker --concurrency=3 -l info"
5. Run flower in a seperate terminal using the command "celery -A DataSync flower --loglevel=info".

Your project will now be up and running at http://127.0.0.1:8000
Your flower dashboard can be seen at http://localhost:5555/dashboard
