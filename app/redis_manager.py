import redis
import os

redis_url = os.environ.get("REDIS_URL")

if redis_url:
    redis_client = redis.from_url(redis_url, decode_responses=True)
else:
    redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

if __name__ == "__main__":
    try:
        # 1. Check connection
        if redis_client.ping():
            print("Successfully connected to Redis.")
        else:
            print("Could not connect to Redis.")

        # 2. Test data storage and retrieval
        print("\nTesting storage and retrieval...")
        redis_client.set("test_key", "Hello, Redis!")
        value = redis_client.get("test_key")
        print(f"Retrieved value for 'test_key': {value}")

        if value == "Hello, Redis!":
            print("Data storage and retrieval works correctly.")
        else:
            print("There was a problem with data storage or retrieval.")

        # Clean up the test key
        redis_client.delete("test_key")
        print("\nTest key 'test_key' deleted.")

    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}")
