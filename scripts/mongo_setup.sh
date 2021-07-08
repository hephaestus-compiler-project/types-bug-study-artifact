#! /bin/bash

mongoimport --db db --collection bugs --file /bugs.json --jsonArray
