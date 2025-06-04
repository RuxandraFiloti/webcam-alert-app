import smtplib
import imghdr  #metadata of images
from email.message import EmailMessage


#constants
PASSWORD = "niys ftsp rhno univ"
SENDER = "adaflori0207@gmail.com"
RECEIVER = "adaflori0207@gmail.com"



def send_email(image_path):
    print("send_email function started")  #this print is important for threads
    email_message = EmailMessage()
    email_message["Subject"] = "New Customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!") #body email

    with open(image_path, "rb") as file:  #rb - binary file
        content = file.read()
    
    #attach the image to email
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content)) 

    #send the email
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function ended") #DO NOT STOP THE PROGRAM IMMEDIATELY



if __name__ =="__main__":
    send_email(image_path="images/19.png")

