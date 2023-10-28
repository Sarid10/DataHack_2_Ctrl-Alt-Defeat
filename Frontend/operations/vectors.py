import boto3

def getVector(text):

    comprehend = boto3.client('comprehend')
    response = comprehend.detect_entities(Text=text, LanguageCode='en')
    # print(f"response = {response}")
    if response['Entities'] == []:
        embedding = 0
    else:
        embedding = response["Entities"][0]["Score"]
    return embedding

# print(getVector("Anay Ahluwalia has 20 years of experience in Corporate Law, Consumer Protection Law, and Labor Law. He has a Client Feedback of 5.0 out of 5.0. His Jurisdiction is Supreme Court. He charges 420.6850078605348 USD per hour. He takes 117.69593880898871 Avg Days for Disposal. He speaks: Telugu, Hindi and Hindi. He practices at Saini PLC, and is based in Hyderabad. She provides pro bono services to the community. Her Client Demographics is Large Corporations."))
# print(getVector("20 Corporate Consumer Protection Labor 5.0 m 420.6850078605348 117.69593880898871 Telugu Hindi Saini PLC Hyderabad Large Corporations False"))
# 0.39465588331222534
# print(getVector("21 Corporate Consumer Protection Labor 5.0 m 420.6850078605348 117.69593880898871 Telugu Hindi Saini PLC Hyderabad Large Corporations False"))
# 0.8611189723014832
# print(getVector("45 Corporate Consumer Protection Labor 5.0 m 420.6850078605348 117.69593880898871 Telugu Hindi Saini PLC Hyderabad Large Corporations False"))
# 0.5133768320083618
# a=['29', 'Medical Immigration Constitutional', '2', 'f', '153', '106', 'Hindi Malayalam', 'Bhatia', 'Bangalore', 'Small Business', 'False']
a=['0', '0', '0', '0', '0', '0', '0', '0', 'Mumbai', '0', '0']
v = [getVector(i) for i in a]
print(v)