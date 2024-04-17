FROM python:3.7-slim    
RUN pip install flask
RUN pip install flask-mysql
RUN mkdir templates
RUN mkdir controlles
COPY app.py /app.py
COPY templates/*  /templates/
COPY controllers/*  /controllers/
RUN chmod -R a+rwx templates
RUN chmod -R a+rwx controllers
CMD ["python","app.py"]
