# our base image
FROM tseenliu/ubuntu:vim

# matainer
MAINTAINER zerostyle0327@gmail.com

# Install python2.7 and pip
RUN apt-get install -y python-pip

# work dir
WORKDIR /usr/src/app

# install Python modules needed by the Python app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy files required for the app to run
COPY app.py .
COPY templates/index.html templates/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "app.py"]
