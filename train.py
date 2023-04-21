import os
import pickle
print("training ai")
training_data = [("Hello", "Hi there!"),("Hi", "Hello!"),("How are you?", "I'm doing well, thanks! How about you?"),("I'm fine", "Glad to hear it! How can I help you today?"),("Bye", "Goodbye!"),("Thanks", "You're welcome!"),("What's your name?", "My name is Chatbot.")
]
def trainData():
	with open('memory.txt', 'wb') as f:
		pickle.dump(training_data, f)
	print("file crated")
check1 = os.path.exists("memory.txt")
if check1 == True:
	print("the file already exist do wipe and startover y/n")
	check1 = input(":")
	if check1.lower() == "y" or check1 == "yes":
		trainData()
else:
	trainData()

