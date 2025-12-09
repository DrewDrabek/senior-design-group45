import asyncio
from backend.app.database.sqlalc_dac import Sql_Alc_DAC
import boto3
from datetime import datetime, timedelta
import apscheduler


enpoint_orgs = ["org1"]

# Create the sqs client

'''
sample que message

{
    "org_id": "org1",
    "endpoint_id": "endpoint1"
}


'''

sqs_client = boto3.client('sqs', region_name='us-east-1')
dac = Sql_Alc_DAC("postgresql+asyncpg://drewdrabek@localhost:5432/postgres", echo=True)
queue_url = "replace this" # replce this with my actual queue url

# get all the endpoints for the orgs that exist

async def process_queue_messages():
    for org_id in enpoint_orgs:
        endpoints = await dac.get_endpoints_for_org(org_id)
        for endpoint in endpoints:
            endpoint_id = endpoint['endpoint_id']
            # Check if endpoint needs scanning
            needs_scanning = check_endpoint_last_scanned(endpoint)
            if not needs_scanning:
                continue  # Skip to next endpoint
            message_body = {
                "org_id": org_id,
                "endpoint_id": endpoint_id
            }
            # Send message to SQS queue
            response = sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=str(message_body)
            )
            print(f"Sent message for endpoint {endpoint_id} in org {org_id}: {response['MessageId']}")

def check_endpoint_last_scanned(endpoint) -> bool:

    # if returned true then we need to scan if false then we do not

    endpoint_information = dac.get_endpoint_by_id(endpoint['endpoint_id'])

    last_scanned_at = endpoint_information.get('last_scanned_at')

    last_scanned_at = endpoint.get('last_scanned_at')
    if last_scanned_at is None:
        return True  # Never scanned before
    elif datetime.utcnow() - last_scanned_at > timedelta(hours=24):
        # Check if last scanned more than 24 hours ago
        return True
    else:
        return False
    

async def main():
    # Initialize your DAC
    await dac.connect()
    
    # Create scheduler
    scheduler = apscheduler.schedulers.asyncio.AsyncIOScheduler()
    
    # Schedule your function to run daily at 2 AM
    scheduler.add_job(
        process_queue_messages,  # your existing function
        apscheduler.triggers.cron.CronTrigger(hour=2, minute=0),  # 2:00 AM daily
        id='daily_endpoint_scan'
    )
    
    # Start scheduler
    scheduler.start()
    
    # Keep the app running forever
    try:
        while True:
            await asyncio.sleep(3600)  # Sleep 1 hour, then check again
    except KeyboardInterrupt:
        scheduler.shutdown()
        await dac.disconnect()

if __name__ == "__main__":
    asyncio.run(main())