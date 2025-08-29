#!/bin/sh
set -e

# Wait for the emulator to be ready
echo "Waiting for Pub/Sub emulator to be ready..."
until curl -s "http://pub-sub-emulator:8085/v1/projects/test/schemas" > /dev/null; do
  echo "Pub/Sub emulator not ready yet. Waiting..."
  sleep 5
done

echo "Pub/Sub emulator is ready. Creating topics..."

# Set environment variables for the emulator
export PUBSUB_EMULATOR_HOST="pub-sub-emulator:8085"
export PUBSUB_PROJECT_ID="test"

# Create topics
topics="labour.planned labour.begun labour.completed labour.update-posted notification.requested notification.created notification.status-updated contraction.started contraction.ended subscriber.requested subscriber.approved contact-message.created"

for topic in $topics; do
  # Create topic using curl to the emulator REST API
  echo "Creating topic: $topic"
  curl -X PUT "http://pub-sub-emulator:8085/v1/projects/test/topics/$topic" \
       -H "Content-Type: application/json" \
       -d "{}" \
       -s
  echo " - Topic $topic created or already exists."

  echo "Creating dead-letter topic: $topic.dlq"
  curl -X PUT "http://pub-sub-emulator:8085/v1/projects/test/topics/$topic.dlq" \
       -H "Content-Type: application/json" \
       -d "{}" \
       -s
  echo " - Topic $topic.dlq created or already exists."
  
  # Create subscription with the same name as topic
  subscription_name="${topic}.sub"
  echo "Creating subscription: $subscription_name"
  curl -X PUT "http://pub-sub-emulator:8085/v1/projects/test/subscriptions/$subscription_name" \
       -H "Content-Type: application/json" \
       -d "{
         \"topic\": \"projects/test/topics/$topic\",
         \"retryPolicy\": {
            \"minimumBackoff\": \"1s\",
            \"maximumBackoff\": \"60s\"
          },
          \"deadLetterPolicy\": {
            \"deadLetterTopic\": \"projects/test/topics/$topic.dlq\",
            \"maxDeliveryAttempts\": 10   
          },
         \"ackDeadlineSeconds\": 10
       }" \
       -s
  echo " - Subscription $subscription_name created or already exists."
done

echo "All topics and subscriptions created!"
