#!/user/bin/env python

import smtplib
import xnat, os, json, pprint, time
from dotenv import load_dotenv

def main():

    load_dotenv()
    with  xnat.connect(os.environ['xnat_url'], user=os.environ['xnat_user'], password=os.environ['xnat_password']) as connection:

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
                    #time.sleep(10)
                    #gen_email(email, fname, lname)
        print(f"Valid users found :  {counter}")


def gen_email(to_email_address, fname , lname):
    """

    :param to_email_address:
    :param fname:
    :param lname:
    :return:
    """
    sent_from = os.environ['smtp_from']
    subject = 'XNAT Server scheduled downtime'
    body = f"""Dear {fname} {lname} , 
    Please note that the xnat server will be down the entirety of next friday Oct 15th 2021 ( 8:00am - 5:00pm ) 
    for a major hardware and software upgrade of the system to better serve you.
    Please contact the Image De-identification Team at {os.environ['smtp_from']} if this is an issue for you and we'll 
    work out a temporary delivery mechanism if needed for this day.
     
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

