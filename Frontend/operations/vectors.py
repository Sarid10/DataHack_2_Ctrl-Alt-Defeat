import boto3

def getVector(text):

    comprehend = boto3.client('comprehend')
    response = comprehend.detect_entities(Text=text, LanguageCode='en')
    embedding = response["Entities"][0]["Score"]
    return embedding

# print(getVector("Anay Ahluwalia has 20 years of experience in Corporate Law, Consumer Protection Law, and Labor Law. He has a Client Feedback of 5.0 out of 5.0. His Jurisdiction is Supreme Court. He charges 420.6850078605348 USD per hour. He takes 117.69593880898871 Avg Days for Disposal. He speaks: Telugu, Hindi and Hindi. He practices at Saini PLC, and is based in Hyderabad. She provides pro bono services to the community. Her Client Demographics is Large Corporations."))
# print(getVector("Arnav Dubey has 29 years of experience in Intellectual Property Law, Criminal Law, and Tax Law. He has a Client Feedback of 2.0 out of 5.0. His Jurisdiction is Specialized Court. He charges 435.66306274876007 USD per hour. He takes 119.00039621571536 Avg Days for Disposal. He speaks: Urdu, Kannada and Tamil. He practices at Sarna-Contractor, and is based in Delhi. She does not provide pro bono services to the community. Her Client Demographics is Small Businesses."))