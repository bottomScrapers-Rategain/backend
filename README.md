# backend
On startup run command

sudo python -m spacy download en_core_web_md


Run app.py within User folder

This repository details the merging and fetching of user sessions

GraphDb folder manages generic graph operations like insertion/deletion of edge, node and aggregating values 
across a connected component

Elastic search is to store user data in the backend.

In user service, key value pairs can be updated, similar sessions are merged.

When return a value for a user, the values are aggregated across the connected component containing the user.

We have referenced paper - https://dl.acm.org/doi/abs/10.1145/2740908.2742750#:~:text=2-,ABSTRACT,for%20pairs%20of%20anonymous%20visitors