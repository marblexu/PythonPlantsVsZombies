FROM python:3

RUN apt update -y 

LABEL Name=pythonplantsvszombies Version=0.0.1

RUN pip install pygame

WORKDIR /app/

RUN echo "Working Directory: /app/  "


RUN echo "Cloning the Marblexu's Repository"

RUN git clone https://github.com/marblexu/PythonPlantsVsZombies /app/

RUN echo "Almost done"

CMD python main.py >> /dev/null

RUN echo "Enjoy Playing!!!"
