# covid19-dashboard
Dashboard to visualize Covid-19 statistics

## Description
This web tool enables the visualization of various indicators for the COVID-19 pandemic
The data is taken from John Hopkins University (JHU) git repository: https://github.com/CSSEGISandData/COVID-19

## Requirements

Linux machine with [Docker](https://www.docker.com)

## Installation and Usage

Build the docker image
```
docker build -t covid-dash https://github.com/jose-cubero/covid19-dashboard.git
```

Run it
```
docker run -d -p 8050:8050 covid-dash:latest
```

Now you can load the dashboard in your favorite web-browser by visiting:
http://0.0.0.0:8050/

## Removal

Stop and remove the container:
```
docker rm 
Remove the image
```
