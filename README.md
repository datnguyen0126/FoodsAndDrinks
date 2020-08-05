# Food and drink project

Project for education, using python django and vuejs

## Start python project

On project folder, create a .env file and modify it as env_example.

At the root folder, type this command and follow the link provided (check your current python is version 3.x or not):

```bash
python manage.py runserver
```

and run celery to excute task (if not windows os, be able to skip '-P eventlet')

```bash
celery -A FoodsAndDrinks worker -l info -P eventlet
```

don't forget to run rabbitmq together. See this tutorial

[how to install and run rabbitmq](https://www.rabbitmq.com/download.html)


## License
Feel free to use :)

