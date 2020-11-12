import boto3
from pycognito.aws_srp import AWSSRP

cognito = boto3.client('cognito-identity', 'eu-west-1')
response = cognito.get_credentials_for_identity(
    IdentityId="eu-west-1_SamNfoWtf")

client = boto3.client('cognito-idp', 'eu-west-1')
aws = AWSSRP(username='khole_47@hotmail.co.uk', password='romhYq-facbyk-tehzi2', pool_id='eu-west-1_SamNfoWtf',
             client_id='3rl4i0ajrmtdm8sbre54p9dvd9', client=client)
test = aws.authenticate_user()

response = client.get_credentials_for_identity(
    IdentityId='3rl4i0ajrmtdm8sbre54p9dvd9',
    Logins={
        'cognito-idp.eu-west-1.amazonaws.com/eu-west-1_SamNfoWtf': test['AuthenticationResult']['IdToken']
    }
)

response = client.list_devices(
    AccessToken=test['AuthenticationResult']['IdToken'],
)

print(response)
