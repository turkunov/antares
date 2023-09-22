# Team Antares 
#### @turkunov (Backend/ML/DS), @kyyoto (ML/DS), @Aspir01 (Frontend/React)

Microservice for TG news' deduplication and classification. This was a hackathon with 10.000$ prizepool that we've participated in and managed to get to finals.

**Our repo's architecture**:

**|_backend**: backend with model's inference
<br /> 
‎ ‎ |_research: our research of DL and traditional ML classification models
<br /> 
‎ ‎‎ ‎ |_utils: ML-related utilities (trainer and optimizer)
<br /> 
‎ ‎ |_utils: utilities for dataset preprocessing (deduplication, embeddings etc..)
<br /> 
**|_frontend**: UI for interacting with the model
<br /> 
**|_data**: training data


**Servers can be deployed via docker container**:
`docker compose up` 

**Following servers'll be accessible after container's deployment**:
* `http://localhost:8080/docs`: API documentation (including ML model's inference endpoints)
* `http://localhost:3030/`: UI for interacting with the model