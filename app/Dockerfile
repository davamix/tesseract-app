FROM python:3.8.2

# Python 3.8.2 is based on Debian Buster.
# The default version of tesseract-ocr package is 4.0.0 and has some problems with the locales. 
# --> https://github.com/sirfz/tesserocr/issues/165

# Those problems are solved in the version 4.1.x. In order to install this version we need to 
# add an extra repository.
# --> https://github.com/tesseract-ocr/tesseract/wiki
# --> https://notesalexp.org/tesseract-ocr/

RUN echo "deb https://notesalexp.org/tesseract-ocr/buster/ buster main" | tee -a /etc/apt/sources.list

RUN wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add - && \
    apt-get update

RUN apt-get update && \
    apt-get install -y apt-transport-https && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config poppler-utils && \
    rm -rf /var/lib/apt/list/*

WORKDIR /usr/src/tesseract-app

RUN pip install --upgrade pip

ADD ./requirements.txt ./

RUN pip install -r requirements.txt

ADD . .

CMD ["python", "./src/main.py"]
