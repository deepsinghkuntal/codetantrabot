from twilio.rest import Client

account_sid = "ACd621bbcae9f2c8e4aab3378eb674506a"
auth_token = 'd00a7dca49cdaac9a8cac9d56d351a29'





def send_sms():
    twilio_number = '+12087389649'
    target_number = '+917300807892'

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body = "Boss I have joind your class",
        from_= twilio_number,
        to = target_number
    )
    print(message.body)

send_sms()