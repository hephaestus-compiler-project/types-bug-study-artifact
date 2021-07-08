FROM mongo

COPY ./data/bug-collection.json /bugs.json
COPY ./scripts/mongo_setup.sh /docker-entrypoint-initdb.d/
