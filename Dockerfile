FROM python:2

RUN pip install cherrypy
RUN pip install sqlalchemy

ADD sale.db /
ADD sales_service.py /

CMD [ "python", "./sales_service.py" ]