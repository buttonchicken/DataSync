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

Q. How to further integrate this with Salesforce?
A. The exposed API's of salesforce can easily be written as functions and be called aysnchronously using celery.
   They will function in the same way as Stripe's API's are functioning right now. We just need to declare them
   inside the tasks.py and call them whenever an event is triggered inside the database. So the plan broadly is:
    1. Make functions out of the exposed salesforce API's.
    2. Push them in the queue whenever a CRUD operation is triggered in any other database.
    3. Let celery worker execute them asynchronously.

Q. How can the above integrations with your product's customer catalog be extended to support other systems within your product?
A. The product's customer catalog can be futher used to generate invoices in the invoice catalog with the necessary details being fetched 
   from both the stripe or my local databse. Any of them can act as a foreign key to the invoice catalog module. Further the necessary details in the customer catalog can be used for calculations to provide insights and analytics to various other modules.
