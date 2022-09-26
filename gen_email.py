#!/usr/bin/env python

import smtplib

import os
import pprint
import time
import xnat
from dotenv import load_dotenv


def main():

    load_dotenv()
    print ( f"connecting with : {os.environ['xnat_url']}, user={os.environ['xnat_user']}, password={os.environ['xnat_password']}")
    with  xnat.connect(os.environ['xnat_url'], user=os.environ['xnat_user'], password=os.environ['xnat_password'], verify=False) as connection:

        users = connection.get_json('/xapi/users')
        print(f"{users}")
        pp = pprint.PrettyPrinter(indent=4)
        counter = 0
        for user in users:
            print(user)
            if not user.startswith("&"):
                # Actually returns a dict
                json_data = connection.get_json(f'/xapi/users/{user}')

                email = json_data.get('email')
                fname = json_data.get('firstName')
                lname = json_data.get('lastName')
                enabled = json_data.get('enabled')
                secured = json_data.get('secured')
                verified = json_data.get('verified')
                if  email is not None and secured == True and verified == True and enabled == True:
                    counter += 1
                    print( json_data['email'])
                    #decoded = json.load(json_data)
                    pp.pprint(  json_data )
                    time.sleep(5)
                    gen_email(email, fname, lname)
        print(f"Valid users found :  {counter}")


def gen_email(to_email_address, fname , lname):
    """

    :param to_email_address:
    :param fname:
    :param lname:
    :return:
    """
    sent_from = os.environ['smtp_from']
    subject = 'Image Deidentificaton Service Center : Scheduled downtime'
    body = f"""Dear {fname} {lname} , 
     Please be aware of the following scheduled downtime: 

     This Thursday 9/29/2022 from 4:00 to 4:30 pm . 

     We will be performing a update of the xnat server software and the system will be down.
     Another Email will follow when the system is up. Please plan accordingly. 

     Thanks for your patience. 
     
    Your IDSC Team """
    email_text = f"""Subject: {subject}

    {body}  """
    try:
        smtp_server = smtplib.SMTP(os.environ['smtp_server'])
        smtp_server.ehlo()
        smtp_server.sendmail(sent_from, to_email_address, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)


if __name__ == '__main__':
    main()

