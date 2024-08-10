# Assignment for Associate Data Engineer role
This project implements a data ingestion pipeline for user metrics using Flask and PostgreSQL, all orchestrated with Docker.

## Setup
1. Clone the repository:
```shell
   git clone <repository-url>
   cd data-ingestion-pipeline
```
2. Create an external docker network
```shell
docker network create krisp-assignment
```
3. Build and run the containers:
```shell
 docker-compose up -d
```
4. Test the API: 
You can send a POST request to the /ingest endpoint.
```shell
curl -X POST -H "Content-Type: application/json" -d '{
    "user_id": "user123",
    "session_id": "session456",
    "talked_time": 120.5,
    "microphone_used": true,
    "speaker_used": true,
    "voice_sentiment": 0.75
}' http://localhost:5001/ingest
```

## Database Schema

The user_metrics table stores the following fields:
- id: Auto-incrementing primary key
- user_id: Unique identifier for the user
- session_id: Unique identifier for the session
- talked_time: Amount of time the user talked (in seconds)
- microphone_used: Boolean indicating if the microphone was used
- speaker_used: Boolean indicating if the speaker was used
- voice_sentiment: Sentiment score of the user's voice (float)
- timestamp: Timestamp of the data entry



