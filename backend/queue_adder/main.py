import asyncio
import json
import os
from datetime import datetime
from app.database.sqlalc_dac import Sql_Alc_DAC
from boto3 import client as boto3_client

# setting the client globally to reuse the connection
sqs_client = boto3_client('sqs', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

# Setting the db connection string - defaults for testing
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://drewdrabek@localhost:5432/postgres"
)


dac = Sql_Alc_DAC(DATABASE_URL, echo=True)

# Function to test the database connection to make sure that we can connect to it
async def test_database_connection():
    """Test the database connection on startup."""
    try:
        await dac.connect()
        print("Database connection established successfully")
        return True
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return False

# function to send to the SQS queue
async def send_to_queue(org_id: str, endpoint_id: str):
    """Send a message to the scanning queue."""
    message = {
        # had to change to string so that it can be added as a json object
        "org_id": str(org_id),
        "endpoint_id": str(endpoint_id),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        queue_url = os.environ['QUEUE_URL']
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        print(f"Queued to SQS: {json.dumps(message)} - MessageId: {response['MessageId']}")
        return message
    except KeyError:
        print("Error: QUEUE_URL environment variable not set")
        raise
    except Exception as e:
        print(f"Error sending to SQS: {e}")
        raise

# This is going to go through the endpoints and then add to the queue those that need to be scanned
async def process_endpoints():
    """Check endpoints and add scan jobs to queue for those not scanned in 24 hours."""
    try:

        endpoints = await dac.get_endpoints_needing_scan()

        print(f"Found {len(endpoints)} endpoints needing scan")
        # This is just for logging purposes
        queued_count = 0
        skipped_count = 0
        # Goes through of the endpoints that is returned from the database and adds to the queue if it has not been scanned in 24 hours
        for endpoint in endpoints:
            try:
                await send_to_queue(
                    org_id=endpoint['org_id'],
                    endpoint_id=endpoint['endpoint_id']
                )
                queued_count += 1
                print(f"Queued: {endpoint['name']} (endpoint_id: {endpoint['endpoint_id']})")
            except Exception as e:
                print(f"Error queueing endpoint {endpoint['endpoint_id']}: {e}")
                skipped_count += 1

        print(f"Summary - Queued: {queued_count}, Skipped: {skipped_count}")
        return queued_count

    except Exception as e:
        print(f"Error in process_endpoints: {e}")
        return 0


async def main():
    print("Queue Adder Service starting...")
    
    # Test database connection first
    db_connected = await test_database_connection()
    if not db_connected:
        print("Cannot start service without database connection. Exiting.")
        return
    
    print("Checking for endpoints that need scanning every 2 minutes...")
    print("Queueing endpoints that haven't been scanned in the last 24 hours")

    try:
        while True:
            try:
                timestamp = datetime.utcnow().isoformat()
                print(f"\n[{timestamp}] Checking for endpoints to scan...")

                count = await process_endpoints()
                print(f"Processed and queued {count} endpoints")

            except Exception as e:
                print(f"Error in main loop: {e}")

            # Wait 2 minutes before next check (120 seconds)
            print("Waiting 2 minutes until next check...")
            await asyncio.sleep(120)
    finally:
        # Clean up database connection when the app is stopped to save resources
        await dac.disconnect()
        print("Database connection closed")


if __name__ == "__main__":
    asyncio.run(main())