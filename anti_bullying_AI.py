import requests


def classify(text):
    """
    This function will pass your text to the machine learning model
    and return the top result with the highest confidence
    """
    key = "6e455150-600d-11eb-87da-c312ddc79b98786a7691-f275-4654-a4c8-25669eb7bb4b"
    url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/classify"
    response = requests.get(url, params={"data": text})
    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


repeating = True

while True:
    message = input("Enter your message (X to exit):")
    if message.upper() == "X":
        repeating = False
    # CHANGE THIS to something you want your machine learning model to classify
    demo = classify(message)

    label = demo["class_name"]
    confidence = int(demo["confidence"])
    # CHANGE THIS to do something different with the result
    print("Result: '%s' with %d%% confidence" % (label, confidence))
    if ((label == "Hurtful") and (confidence > 60)) or ((label == "Nice") and (confidence < 60)):
        print("\nAre you sure you want to post this?")
    else:
        print("\nMessage Accepted.")
