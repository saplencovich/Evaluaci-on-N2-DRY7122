FROM python:3.8.2
RUN pip install --upgrade pip
RUN pip install flask
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY  sample_app.py /home/myapp/
EXPOSE 3000
CMD python3 /home/myapp/sample_app.py
