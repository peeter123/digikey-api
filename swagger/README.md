# Modified swagger files

This folder contains modified swagger files for the Digikey API. Only swagger files 
that require modifications should be placed in here.

## Explanation

When using the API generator `generate-v3-api/generate_client_swagger.py`, by default
it will download the swagger API definitions from Digikey. This is useful because the
API should be generated from the latest swagger files. However, we found that the 
swagger file for the Marketplace Orders API (Orders.json) was not in fact up-to-date
(as of 2022-09-20) and was missing authentication parameters from all operations.
For this reason, we have added a `swagger` folder to the repo and added the 
`Orders.json` file to it, with the modifications that were necessary for it to generate
a functional API.

The API generator was modified such that it would now check to see if a swagger file
exists in the `swagger` folder, before downloading it from Digikey. If the swagger
file exists in the `swagger` folder, the API generator will use it instead. All other
swagger files are downloaded from Digikey.

