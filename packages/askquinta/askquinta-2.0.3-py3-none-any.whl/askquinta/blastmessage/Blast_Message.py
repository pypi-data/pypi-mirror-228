import os
import requests
import base64
import pickle
import html, slack
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import quote

class About_Blast_Message:
    def __init__(self, creds_email = None, token_telegram_bot = None, token_slack_bot = None):
        
        """
        Initialize the About_Blast_Message class.

        Args:
            creds_email (str): The path to the file containing credentials in pickle format.
                By default, the creds_email will be obtained from the environment variable 'blast_message_creds_email_file'.
            token_telegram_bot (str, optional): Token Telegram Bot
                By default, the token_telegram_bot will be obtained from the environment variable 'blast_message_token_telegram_bot'.
            token_slack_bot (str, optional): Token Slack Bot
                By default, the token_slack_bot will be obtained from the environment variable 'blast_message_token_slack_bot'.
        """
        
        self.creds_email = creds_email or os.getenv('blast_message_creds_email_file')
        self.creds_telegram =  token_telegram_bot or os.getenv('blast_message_token_telegram_bot')
        self.creds_slack = token_slack_bot or os.getenv('blast_message_token_slack_bot')
                  
    def send_message_to_email(self, to, subject, message, cc = None, file_path = None) -> dict:
        """
        Sends an email message.

        This method sends an email message using the Gmail API.

        Args:
            to (str): The recipient's email address.
            subject (str): The subject of the email.
            message (str): The body of the email.
            cc (str, optional): The email address to be included in the CC field. Default is None 
            file_path (str, optional): Path to attached file. Default is None

        Returns:
            dict: The response message from the Gmail API after sending the email.

        Example:
            bot = About_Blast_Message()
            bot.send_message_to_email(
                to='recipient@example.com',
                subject='Hello',
                message='This is a test email.',
                cc='cc@example.com'
            )
        """
        ## Config E-mail
        path_to_pickle = self.creds_email
        
        ## Get the service object from the loaded credentials
        with open(path_to_pickle, 'rb') as token:
            creds = pickle.load(token)
        service = build('gmail', 'v1', credentials=creds)

        if file_path:
            final_message = MIMEMultipart()
        else:
            final_message = MIMEText(message)
            
        final_message['to'] = to
        final_message['subject'] = subject
        if cc:
            final_message['cc'] = cc

        if file_path:
            final_message.attach(MIMEText(message, 'plain'))
    
            attachment = MIMEBase('application', 'octet-stream')
            with open(file_path, 'rb') as file:
                attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f"attachment; filename= {file_path}"
            )
            final_message.attach(attachment)
        
        raw_message = base64.urlsafe_b64encode(final_message.as_bytes()).decode('utf-8')
        email = {'raw': raw_message}

        # Send the email
        try:
            message = service.users().messages().send(userId='me', body=email).execute()
            print('Email sent successfully to.')
            return message
        except HttpError as e:
            print('An error occurred while sending the email:', str(e))

    def send_message_to_telegram(self, to, message):
        """
        Sends a message to a specified recipient using the Telegram Bot API.

        This function constructs a URL with the provided message and recipient information
        and sends an HTTP GET request to the Telegram Bot API for sending messages.

        Args:
            self (About_Blast_Message): An instance of the About_Blast_Message class.
            to (str): The target chat or user ID to which the message will be sent.
                1. click t.me/kucingduduk_bot -> click start
                2. find 'https://t.me/RawDataBot' -> find your chat_id
                3. to = your_chat_id
            message (str): The message text to be sent.

        Returns:
            requests.Response: The response object from the Telegram API request.

        Raises:
            Exception: If there is an error while sending the message via the Telegram API,
                       an exception is caught, and an error message is printed.
        
        

        Example:
            bot = About_Blast_Message()
            response = bot.send_message_to_telegram(to='CHAT_OR_USER_ID', message='Hello from your bot!')
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print("Failed to send message.")
        
        
        """
        token = self.creds_telegram
        for i in "_*[":
            message = message.replace(i,'\{}'.format(i)) # Replace underscore with HTML entity
        
        message = quote(message)
                        
        send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + to + '&parse_mode=Markdown&text=' + message
        try:
            response = requests.get(send_text)
            return response
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")
            pass
            
    def send_message_to_slack(self, to, message):
        '''
        Sends a message to a specified channel in Slack using the provided token.

        Parameters:
        to (str): The channel or member ID where the message will be sent.
        message (str): The message content to be sent.

        Returns:
        dict: A dictionary containing information about the Slack API response.
            - 'ok' (bool): Indicates whether the message sending was successful.
            - 'ts' (str): The timestamp of the sent message, if successful.

        Usage:
        1. Obtain an OAuth bot token:
            a. Go to https://api.slack.com/
            b. Click on 'Create New App' -> 'From Scratch'.
            c. Provide a bot name and select the desired workspace.
            d. In 'Add Features and Functionality settings', choose 'Bots'.
            e. Proceed to 'Review Scopes to Add'.
            f. Under 'Scopes', find 'Bot Token Scopes', and select 'Add an OAuth Scope'.
            g. Choose the relevant bot functionality scope, e.g., 'chat:write.public' for messaging.
            h. Click 'Install to Workspace' and grant the necessary permissions.

        2. Launch the bot:
            a. Create or open the desired channels in your Slack workspace.
            b. Add the bot to the channels where you want it to send messages.
            c. You're ready to send messages using the function!

        Example:
        ```python
        bot = About_Blast_Message()
        channel_id = '#general'  # Replace with the desired channel or member ID
        message_content = 'Hello, this is a test message!'
        response = bot.send_message_to_slack(channel_id, message_content)
        print("Message sent successfully:", response['ok'])
        print("Message timestamp:", response['ts'])
        ```

        Note:
        - This function uses the `slack.WebClient` from the `slack` library. Make sure to install the library
          using `pip install slack-sdk` if you haven't already.

        - Ensure that the bot has been added to the target channels before attempting to send messages.
        '''
        client = slack.WebClient(self.creds_slack)
        response = client.chat_postMessage(channel=to, text=message)
        return response
 
