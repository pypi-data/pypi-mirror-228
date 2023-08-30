# Neuralite: A Streamlined Python Framework for Rapidly Building and Deploying Machine Learning-Based Conversational Agents 💡

Build, deploy, and scale your AI projects with Neuralite! Whether you're a seasoned AI developer or just starting out, Neuralite offers a simple and efficient way to implement AI features into your software.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Chatbot](#basic-chatbot)
3. [Compiling Your Model](#compiling-your-model)
4. [Loading a Compiled Model](#loading-a-compiled-model)
5. [Sample Datasets](#sample-datasets)
   - [Conversational Dataset](#conversational-dataset)
   - [Medical Advice Dataset](#medical-advice-dataset)
   - [Educational Dataset](#educational-dataset)

## Getting Started
To get started, install Neuralite with pip:
```bash
pip install Neuralite
```

## Basic Chatbot
Creating a basic chatbot is simple:
```python
from neuralite.interpreter import ai # Imports framework

assistant = ai('dataset.json') # Loads dataset

cycle_end = False # Starts the AI cycle

while not cycle_end: # Main cycle
    message = input("Enter a message: ") # Prompts user with message
    if message.lower() == "stop": # Exit with 'stop'
        cycle_end = True # Ends cycle
    else:
        print(assistant.process_input(message)) # Prints the response
```

# Compiling Your Model 📦
To make your dataset unreadable, load faster, and to package it into a neat file.

```python
from neuralite.interpreter import ai # Imports framework

assistant = ai('dataset.json') # Loads dataset

assistant.compile('model.nlite') # Packages dataset to 'model.nlite'
```

# Loading a Compiled Model 🔓
To load a precompiled model.

```python
from neuralite.interpreter import ai # Imports framework

assistant = ai.compiled('model.nlite') # Loads the compiled model

cycle_end = False # Starts the AI cycle

while not cycle_end: # Main cycle
    message = input("Enter a message: ") # Prompts user with message
    if message.lower() == "stop": # Exit with 'stop'
        cycle_end = True # Ends cycle
    else:
        print(assistant.process_input(message)) # Prints the response
```

## Sample Datasets
Here are some sample datasets for different use-cases.

### Conversational Dataset
```json
{
  "greeting": ["Hi", "Hello", "Hey there"],
  "greeting_responses": ["Hello!", "Hi, how can I help?", "Hey! What's up?"],
  "farewell": ["Goodbye", "See you", "Ciao"],
  "farewell_responses": ["Goodbye!", "See you soon!", "Take care!"],
  "how_are_you": ["How are you?", "How's it going?", "What's up?"],
  "how_are_you_responses": ["I'm good, thank you!", "I'm doing well. How about you?", "Not much, what about you?"],
  "compliment": ["You're great!", "You're amazing!", "You're awesome!"],
  "compliment_responses": ["Thank you! You're pretty awesome too.", "Thanks! You're great as well!", "Thanks! That means a lot."],
  "name": ["What's your name?", "Who are you?", "Tell me your name."],
  "name_responses": ["I'm Neuralite, your AI assistant.", "Call me Neuralite.", "I'm Neuralite! Nice to meet you."],
  "jokes": ["Tell me a joke.", "Do you know any jokes?", "Make me laugh."],
  "jokes_responses": ["Why did the scarecrow win an award? Because he was outstanding in his field!", "I told my computer I needed a break. Now it won't stop sending me Kit-Kats.", "Why did the math book look sad? Because it had too many problems."]
}
```

### Medical Advice Dataset
```json
{
  "general_health": ["How can I stay healthy?", "Tell me some health tips"],
  "general_health_responses": ["Eat a balanced diet, exercise regularly, and get enough sleep.", "Maintaining a healthy lifestyle is essential for long-term health."],
  "first_aid": ["What should I do for a cut?", "How do I treat burns?"],
  "first_aid_responses": ["For minor cuts, clean with water and apply antiseptic.", "For minor burns, cool the area under cold running water and apply a burn ointment."],
  "headache": ["How to treat a headache?", "What's good for migraines?"],
  "headache_responses": ["For mild headaches, over-the-counter pain relievers and rest are recommended.", "For migraines, consult a healthcare provider for prescription medications."],
  "allergies": ["How to manage allergies?", "Tell me about antihistamines"],
  "allergies_responses": ["Antihistamines can help relieve allergy symptoms.", "For chronic allergies, consider lifestyle changes and consult a healthcare provider."],
  "exercise": ["What are the benefits of exercise?", "Tell me about aerobic exercises"],
  "exercise_responses": ["Exercise improves mental and physical health.", "Aerobic exercises like running and swimming are good for cardiovascular health."]
}
```

### Conversational Dataset
```json
{
  "general_science": ["Tell me about science", "What is science?"],
  "general_science_responses": ["Science is the study of the natural world.", "Science helps us understand how things work."],
  "literature": ["Who wrote 'Romeo and Juliet'?", "Tell me about 'Moby Dick'"],
  "literature_responses": ["'Romeo and Juliet' was written by William Shakespeare.", "'Moby Dick' is a novel by Herman Melville about Captain Ahab's obsession with a white whale."],
  "history": ["Tell me about the French Revolution", "Who was Martin Luther King Jr.?"],
  "history_responses": ["The French Revolution was a period of social and political upheaval in France from 1789 to 1799.", "Martin Luther King Jr. was an American civil rights leader who fought for racial equality."],
  "chemistry": ["What is the periodic table?", "Tell me about chemical bonds"],
  "chemistry_responses": ["The periodic table organizes chemical elements based on their properties.", "Chemical bonds are forces that hold atoms together in a molecule."],
  "biology": ["What is DNA?", "Tell me about evolution"],
  "biology_responses": ["DNA is the genetic material that carries information about an organism.", "Evolution is the process of change in species over generations."]
}
```

