# xnat-email
Program to read users from xnat system and send them email

Features over native xnat email : 

- Allow for filtering of users that are not enabled , secured and verified
- sends individual emails to users 
- XNAT's native fails when talking to our SMTP system ( too many users ? )
- control of how frequent individual emails are send

Requirements
- A running version of the XNAT.ORG Server
- A SMTP server to receive emails ( no auth at this time supported ) 

Configuration

``` 
$ git clone git@github.com:gkowalski/xnat-email.git xnat-email
$ cd xnat-email
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
  Copy env_template to .env and edit to reflect your settings
```

Running 
- Edit the gen_email.py to reflect the email you want to send out and how frequently to send each email.
```angular2html
./gen_email.py
```
