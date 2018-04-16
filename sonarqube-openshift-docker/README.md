# SonarQube on OpenShift
This repo contains all of the resources required to build an OpenShift-specific
Docker image of SonarQube.

It is inspired by the upstream SonarQube Docker image:
https://github.com/SonarSource/docker-sonarqube

# Docker Hub

The SonarQube image is available on Docker Hub at: https://hub.docker.com/r/openshiftdemos/sonarqube/

# Deploy on OpenShift
You can do use the provided templates with an embedded or postgresql database to deploy SonarQube on 
OpenShift:

SonarQube with Embedded H2 Database:

    oc new-app -f sonarqube-template.yaml --param=SONARQUBE_VERSION=6.7

SonarQube with PostgreSQL Database:

    oc new-app -f sonarqube-postgresql-template.yaml --param=SONARQUBE_VERSION=6.7

# 2018 April 15 - JDT

In order to get this container to work on my single-node origin cluster, I used the modified Dockerfile to set UID and GID to "1000060000".  I also had to expose the container to the host with port 9000:

oc patch svc openshift-sonarqube -p '{"spec":{"externalIPs":["x.x.x.x"]}}'

