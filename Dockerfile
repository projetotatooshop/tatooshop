FROM python:3.7-slim    
RUN pip install flask
RUN pip install flask-mysql
RUN mkdir templates
RUN mkdir controlles
RUN mkdir static
COPY app.py /app.py
COPY templates/*  /templates/
COPY controllers/*  /controllers/
COPY static/*  /static/
RUN chmod -R a+rwx templates
RUN chmod -R a+rwx controllers
RUN chmod -R a+rwx static
CMD ["python","app.py"]
