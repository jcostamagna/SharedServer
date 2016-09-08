FROM ubuntu

RUN apt-get -y update && apt-get install -y nodejs && apt-get install -y npm

RUN apt-get install nodejs-legacy

RUN npm install -g live-server

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Bundle app source
COPY . /usr/src/app

EXPOSE 8080
CMD [ "live-server", "--open=index.html" ]

