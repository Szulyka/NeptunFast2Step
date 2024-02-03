import subprocess
import sys
import time
import quopri
import email


def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)


# Install dependencies if not already installed
try:
    import imaplib
    import pyperclip
except ImportError:
    print("Missing dependencies, installing now...")
    install_dependencies()

# this program connect to your e-mail account, gets the content of latest Neptun e-mail every 4 seconds and copies the security 6-digit code to the clipboard

# could be other e-mail client
imapServer = imaplib.IMAP4_SSL('imap.gmail.com')

# your e-mail adress, and password
# for the password, you need to make an app password through Google -> profile settings -> security -> app passwords
# this is needed to surpass two-step authentication at Google
# do not share that code with anyone, it is a security risk
imapServer.login('horogszegi.palko@gmail.com', 'bzdm jufm eehs ltda')
# example: -------'smith.adam@gmail.com', '4 times 4 digit app password'

latestEmailId = ""
while True:
    imapServer.select('inbox')
    # example: ------------------------------------------------------"noreply@neptun.elte.hu"        "Neptun"       <- don't add utf-8 chars, also subset of words of the subject is enough
    result, emailIds = imapServer.search(None, 'FROM "noreply@neptun.elte.hu" SUBJECT "Neptun"')
    if result == 'OK':
        # this lets the code and the clipboard "rest" until a new Neptun e-mail comes
        if emailIds[0].split()[-1] != latestEmailId:
            # Get the latest e-mail ID
            latestEmailId = emailIds[0].split()[-1]

            # Fetch the e-mail content
            result, emailData = imapServer.fetch(latestEmailId, '(RFC822)')

            # Parse the e-mail content
            rawEmail = emailData[0][1]

            emailMessage = email.message_from_bytes(rawEmail)
            # Extract the text from the e-mail body
            emailText = emailMessage.get_payload()
            decodedEmailText = quopri.decodestring(emailText).decode('utf-8')
            # whole e-mail
            print("EMAIL CONTENT")
            print(decodedEmailText)

            digitsOfCode = []
            # we go through char by char in the email body, after finding digits, we ignore the first three digits and dash and there is the 6-digit code we need
            for i in range(len(decodedEmailText)):
                if decodedEmailText[i].isdigit():
                    digitsOfCode.append(decodedEmailText[i + 4:i + 10])
                    break

            digitsOfCode = ''.join(digitsOfCode)
            print(digitsOfCode)
            # let's put it onto clipboard
            pyperclip.copy(digitsOfCode)
            print("Code to be pasted: ", digitsOfCode)
        else:
            print("Waiting for new code")
            time.sleep(1)
    else:
        print("No email found")


# TODO: standalone app that calls this app and automatically click e-mail button, pastes the code, pushes enter
