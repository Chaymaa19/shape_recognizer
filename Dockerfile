FROM ubuntu:20.04
RUN apt-get update
RUN apt install -y python3 python3-pip
WORKDIR /shape_recognizer
COPY ./ /shape_recognizer
RUN pip install -r requirements.txt
CMD ["bash"]