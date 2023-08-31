from intentclassifier import *

Classifer = IntentClassifier()

Classifier.set_intentsfp("intents.json")
Classifier.set_vectorsfp("vectors.json")

Classifier.train_vectors()

Input = input("You: ")

classification = Classifier.classify(Input)

print(classification)
