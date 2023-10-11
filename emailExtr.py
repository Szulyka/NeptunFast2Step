import imaplib
import email
import time
import pyperclip 

#this program connect to your e-mail account, gets the content latest Neptun e-mail every 4 seconds and copies the security 6-digit code to the clipboard

while True:
    #could be other e-mail client
    imapServer = imaplib.IMAP4_SSL('imap.gmail.com')

    #your e-mail adress, and password
    #for the password, you need to make an app password through google -> profile settings -> security -> app passwords 
    #this is needed to surpass two-step authentication at Google
    #do not share that code with anyone, it is a security risk
    imapServer.login('e-mail', 'password')
    #example: -------'smith.adam@gmail.com', '4 times 4 digit app password'

    imapServer.select('inbox')
    #example: ---------------------------------------"noreply@neptun.elte.hu"         "Neptun"       <- don't add utf-8 chars, also subset of words of the subject is enough
    result, emailIds = imapServer.search(None, 'FROM "noreply@neptun.elte.hu" SUBJECT "Neptun"')

    if result == 'OK':
        # Get the latest e-mail ID
        latestEmailId = emailIds[0].split()[-1]
        print(latestEmailId)
        # Fetch the e-mail content
        result, emailData = imapServer.fetch(latestEmailId, '(RFC822)')
        
        # Parse the e-mail content
        rawEmail = emailData[0][1]
        emailMessage = email.message_from_bytes(rawEmail)
        
        # Extract the text from the e-mail body
        emailText = emailMessage.get_payload()
     
        #ascii -> utf-8 causes some corruption to the text
        emailText = emailText.replace('=', '')
        
        numList = []
        for i in range(len(emailText)):
            #not sure why this is how it works 
            if i > 30 and emailText[i].isdigit() and len(numList) < 22:
                numList.append(emailText[i])
                
        #numList is the whole code, Neptun already includes the first three digits, so codeWithoutFirstThree is what we need
        numList = numList[13:]
        codeWithoutFirstThree = numList[3:]
        codeWithoutFirstThree = ('').join(codeWithoutFirstThree)
        #let's put it onto clipboard
        pyperclip.copy(codeWithoutFirstThree)
        print("Code to be pasted: ", codeWithoutFirstThree)
        
        #whole e-mail
        print(emailText)
    else:
        print("No email found")
        
    #logout in every iteration, probably there is a better way. This ensures that you will get the latest e-mail every iteration
    imapServer.logout()
            
    time.sleep(1)

#TODO: standalone app that calls this app and automatically click e-mail button, pastes the code, pushes enter