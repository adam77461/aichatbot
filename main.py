import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import wikipedia
prebuiltCommands = ["search"]
# printing the result
# print(result)
# Define some initial training data
f = open('memory.txt', 'rb')
training_data = pickle.load(f)
f.close()

# Define a function to preprocess the text data
def preprocess_text(text):
    return text.lower().strip()

# Define a function to train the chatbot
def train_chatbot(training_data):
    # Prepare the data for training
    inputs = []
    outputs = []
    for input_text, output_text in training_data:
        inputs.append(preprocess_text(input_text))
        outputs.append(output_text)

    # Use scikit-learn to vectorize the input text
    vectorizer = CountVectorizer()
    input_vectors = vectorizer.fit_transform(inputs)

    # Train a Naive Bayes classifier on the input vectors and output text
    classifier = MultinomialNB()
    classifier.fit(input_vectors, outputs)
    with open('memory.txt', 'wb') as f:
        pickle.dump(training_data, f)
        f.close()
    return vectorizer, classifier

# Define a function to generate a response
def generate_response(input_text, vectorizer, classifier):
    # Vectorize the input text
    input_vector = vectorizer.transform([preprocess_text(input_text)])

    # Use the classifier to predict the output text
    output_text = classifier.predict(input_vector)[0]
    return output_text

# Train the chatbot
vectorizer, classifier = train_chatbot(training_data)
# Use the chatbot to generate responses to user input
while True:
    input_text = input("You: ")

    # Check if the input text is new
    if preprocess_text(input_text) not in [preprocess_text(data[0]) for data in training_data]:
        # Prompt the user for a new response
        if input_text.split(" ")[0] in prebuiltCommands:
            # input_textList = split(input_text) 
            try:
                # to make it smarter it use wikipedia sentences so it doesn't print whole page
                result = wikipedia.summary(str(input_text), sentences = 2)
                print("Chatbot: "+result)
            except Exception as e:
                print("Chatbot: i was unable to retrieve any data my apologies")
        else:
            new_response = input("I'm not sure how to respond to that. Please provide a response: ")
            # Add the new input and corresponding response to the training data
            training_data.append((input_text, new_response))
            # Retrain the chatbot with the updated training data
            vectorizer, classifier = train_chatbot(training_data)
            print("Chatbot: Thanks for letting me know. I'll remember that for next time.")

    else:
        # Generate a response to the user input
        output_text = generate_response(input_text, vectorizer, classifier)
        print("Chatbot:", output_text)
