## photo-processor instructions

### Installation

Prerequisites:  
- Docker  
- Ability to run `make`.

App is bundling Postgres and RabbitMQ instances via Docker, so please stop any local related services to avoid port conflicts. Otherwise you can amend the default port mappings on the docker-compose file.

Start the app:
- `make start`

Create or reset the db schema after booting the app:  
- `make db-schema`

Using a web browser, view the pending photos
- `http://localhost:3000/photos/pending`

Select one or more uuids from the list and issue a POST request to the /photos/process endpoint
- Example: `curl --request POST --data '["2da96151-32c9-4b46-9906-7ee1b2db93bd", "6a515adc-7b6d-46a1-b20d-a2b0fa843555"]' http://localhost:3000/photos/process`

Check that the photos that were processed are no longer included in the pending list
- `http://localhost:3000/photos/pending`

Check the thumbnails generated in the ./thumbnails directory of the project
