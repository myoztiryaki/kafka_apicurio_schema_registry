FROM openjdk:17.0.2-jdk-buster

RUN apt update
RUN apt install -y curl
RUN apt install -y python3 
RUN apt install -y python3-pip 
RUN apt install -y git 
RUN apt install -y libpq-dev

ENV KAFKA_VERSION 3.8.0
ENV SCALA_VERSION 2.12

RUN  mkdir /tmp/kafka && \
    curl "https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" \
    -o /tmp/kafka/kafka.tgz && \
    mkdir /kafka && cd /kafka && \
    tar -xvzf /tmp/kafka/kafka.tgz --strip 1

RUN mkdir -p /data/kafka

COPY start-kafka.sh  /usr/bin

RUN chmod +x  /usr/bin/start-kafka.sh

CMD ["start-kafka.sh"]
