import imaplib
import email

# Connect to the IMAP server
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
imap_server.login('horogszegi.palko@gmail.com', 'bzdm jufm eehs ltda')

# Select the mailbox (e.g., INBOX)
imap_server.select('inbox')

# Search for emails
result, email_ids = imap_server.search(None, 'FROM "do-not-reply@directmail2.binance.com" SUBJECT "[Binance] Your ID Document has Expired - 2023-10-02 00:04:38 (UTC)"')

if result == 'OK':
    # Get the latest email ID
    latest_email_id = email_ids[0].split()[-1]
    
    # Fetch the email content
    result, email_data = imap_server.fetch(latest_email_id, '(RFC822)')
    
    if result == 'OK':
        # Parse the email content
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        
        # Extract the text from the email body
        email_text = email_message.get_payload()
        
        # Process the email text as needed
        print(email_text)

# Close the IMAP connection
imap_server.logout()
