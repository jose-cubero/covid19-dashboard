# covid19-dashboard
Dashboard to visualize Covid-19 statistics

## Description
This web tool enables the visualization of various indicators for the COVID-19 pandemic
The data is taken from John Hopkins University (JHU) git repository: https://github.com/CSSEGISandData/COVID-19

## Requirements

Linux machine with [Docker](https://www.docker.com)

## Usage

Pull and run the latest image from Docker Hub:
```
docker run -d -p 8050:8050 joeblue/covid19-dashboard
```

**Or** build it locally

```
docker build -t covid-dash https://github.com/jose-cubero/covid19-dashboard.git
docker run -d -p 8050:8050 covid-dash:latest
```

Now you can load the dashboard in your favorite web-browser by visiting:
http://0.0.0.0:8050/

