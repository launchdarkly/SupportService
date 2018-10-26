FROM circleci/openjdk:8-node-browsers

WORKDIR /usr/src/webdriver

ADD src /usr/src/webdriver/src
COPY hosts.txt . 
COPY pom.xml . 
RUN mvn dependency:go-offline

RUN sudo chown -R circleci:circleci /usr/src/webdriver
RUN mvn compile assembly:single 

EXPOSE 9515