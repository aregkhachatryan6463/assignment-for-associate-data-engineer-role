from flask import Flask, request, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "db"),
            database=os.getenv("POSTGRES_DB", "user_metrics_db"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.DatabaseError as e:
        app.logger.error(f"Database connection error: {e}")
        raise


def execute_query(query, params=None, commit=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if commit:
            conn.commit()
        return cursor
    except psycopg2.IntegrityError as e:
        app.logger.error(f"Database integrity error: {e}")
        conn.rollback()
        raise
    except psycopg2.DatabaseError as e:
        app.logger.error(f"Database error: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def validate_data(data):
    validators = {
        'user_id': lambda x: x is not None,
        'session_id': lambda x: x is not None,
        'talked_time': lambda x: isinstance(x, (int, float)) and x >= 0,
        'microphone_used': lambda x: isinstance(x, bool),
        'speaker_used': lambda x: isinstance(x, bool),
        'voice_sentiment': lambda x: isinstance(x, (int, float)) and 0 <= x <= 1
    }

    for field, validate in validators.items():
        if field not in data or not validate(data[field]):
            return False, f"Invalid or missing value for field: {field}"

    return True, None


@app.route('/ingest', methods=['POST'])
def ingest_data():
    data = request.json

    is_valid, error_message = validate_data(data)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    try:
        query = """
            INSERT INTO user_metrics (user_id, session_id, talked_time,
            microphone_used, speaker_used, voice_sentiment)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('user_id'),
            data.get('session_id'),
            data.get('talked_time'),
            data.get('microphone_used'),
            data.get('speaker_used'),
            data.get('voice_sentiment')
        )
        execute_query(query, params, commit=True)
        return jsonify({"status": "success"}), 201

    except psycopg2.IntegrityError:
        return jsonify({"status": "error", "message": "Integrity error occurred. Please check your data."}), 400

    except psycopg2.DatabaseError:
        return jsonify({"status": "error", "message": "A database error occurred."}), 500

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
