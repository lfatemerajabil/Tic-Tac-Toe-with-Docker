# Tic-Tac-Toe with Docker

You can play tic-tac-toe in your localhost:8080 with docker.
The game board will look like the below image.

<img width="349" alt="Screenshot 2024-08-10 at 13 29 03" src="https://github.com/user-attachments/assets/135f9b2d-0ebd-4bc7-bc90-26830aec0700">


## Run the following commands

step 1: log in to your docker

```
docker login
```

## Method 1: using docker

step 2: build your docker image

```
docker build -t <your_image_name> .
```

step 3: run your image and make a container

```
docker run -d -p 8080:8080 <your_image_name>
```

step 4: got to http://localhost:8080/

## Method 2: using docker-compose

step2: run docker-compose file

```
docker-compose up
```

step 3: got to http://localhost:8080/
