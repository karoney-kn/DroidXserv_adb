import subprocess
import re
from datetime import datetime
import sys
def convert_timestamp(timestamp):
    try:
        dt = datetime.fromtimestamp(int(timestamp) / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "N/A"

def parse_sms_output(raw_output):
    messages = []
    rows = raw_output.strip().split("Row:")

    for row in rows:
        if not row.strip():
            continue

        # Extract fields using regex
        address = re.search(r"address=(.*?),", row)
        sub_id = re.search(r"sub_id=(.*?),", row)
        date = re.search(r"date=(\d+)", row)
        date_sent = re.search(r"date_sent=(\d+)", row)
        body = re.search(r'body=(.+?)(?=\s+\w+=|\s*$)', row)

        sms = {
            "address": address.group(1).strip() if address else "Unknown",
            "sub_id": sub_id.group(1).strip() if sub_id else "N/A",
            "date": convert_timestamp(date.group(1)) if date else "N/A",
            "date_sent": convert_timestamp(date_sent.group(1)) if date_sent else "N/A",
            "body": body.group(1).strip() if body else ""
        }
        messages.append(sms)

    return messages


def save_to_file(messages, filename):
    with open(filename, "w", encoding="utf-8") as f:

        for i, sms in enumerate(messages, start=1):

            content=f"""
            Message #{i}
            {'-'*40}
            Sub ID:      {sms['sub_id']}
            Address:     {sms['address']}
            Date:        {sms['date']}
            Date Sent:   {sms['date_sent']}
            Body:        {sms['body']}
            """
            
            cleaned_content = '\n'.join(line.lstrip() for line in content.splitlines())
            f.write(cleaned_content)


def main():

    output_file = "nzxt_sms.txt"
    
    try:

        print("Fetching SMS data from device...")
        result = subprocess.run(['adb', 'shell', 'content', 'query', '--uri', 'content://sms/'],capture_output=True,text=True,check=True)
        raw_output = result.stdout
        
        if not raw_output.strip():
            print("No SMS data found or unable to query SMS content.")
            sys.exit(1)
        
        # Parse the output
        print("Parsing SMS data...")
        sms_messages = parse_sms_output(raw_output)
        
        if not sms_messages:
            print("No SMS messages could be parsed.")
            sys.exit(1)
        
        # Write to file
        print(f"Writing {len(sms_messages)} messages to {output_file}...")
        save_to_file(sms_messages, output_file)
        print(f"\n✅ Success! Filtered SMS data saved to {output_file}")
        print(f"Total messages processed: {len(sms_messages)}")
        

    except:
        print(f"An error occurred: {e}")
        print("Make sure:")
        print("  1. ADB is installed and in your PATH")
        print("  2. A device is connected (run 'adb devices')")
        print("  3. Your device has USB debugging enabled")
        sys.exit(1)

if __name__ == "__main__":
    main()