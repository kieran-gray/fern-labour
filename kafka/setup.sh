#!bin/sh
echo -e 'Creating kafka topics'

kafka-topics.sh --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} --create --if-not-exists --topic ${KAFKA_TOPIC_PREFIX}.labour.begun --replication-factor 1 --partitions 1
kafka-topics.sh --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} --create --if-not-exists --topic ${KAFKA_TOPIC_PREFIX}.labour.completed --replication-factor 1 --partitions 1
kafka-topics.sh --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} --create --if-not-exists --topic ${KAFKA_TOPIC_PREFIX}.contraction.started --replication-factor 1 --partitions 1
kafka-topics.sh --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} --create --if-not-exists --topic ${KAFKA_TOPIC_PREFIX}.contraction.ended --replication-factor 1 --partitions 1
kafka-topics.sh --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} --create --if-not-exists --topic ${KAFKA_TOPIC_PREFIX}.labour.update-posted --replication-factor 1 --partitions 1
kafka-topics.sh --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} --create --if-not-exists --topic ${KAFKA_TOPIC_PREFIX}.notification.requested --replication-factor 1 --partitions 1
kafka-topics.sh --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} --create --if-not-exists --topic ${KAFKA_TOPIC_PREFIX}.notification.status-updated --replication-factor 1 --partitions 1

echo -e 'Successfully created the following topics:'
kafka-topics.sh --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} --list