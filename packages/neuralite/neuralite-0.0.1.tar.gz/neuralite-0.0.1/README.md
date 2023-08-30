# Neuralite: A Lightweight  AI Framework 💡

Build, deploy, and scale your AI projects with Neuralite! Whether you're a seasoned AI developer or just dipping your toes into the world of artificial intelligence, Neuralite offers you a convenient and efficient way to implement AI features into your software.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Chatbot](#basic-chatbot)
3. [Compiling Your Model](#compiling-your-model)
4. [Loading a Compiled Model](#loading-a-compiled-model)
5. [License](#license)

## Getting Started
To get started, you only need to install Neuralite with PIP:
```bash
pip install Neuralite
```
## Basic Chatbot
```python
from neuralite.interpreter import ai

assistant = ai('dataset.json')
cycle_end = False

while not cycle_end:
    message = input("Enter a message: ")
    if message.lower() == "stop":
        cycle_end = True
    else:
        print(assistant.process_input(message))
```

## Compiling Your Model 📦
To make your dataset unreadable and to package it into a neat file.
```python
from neuralite.interpreter import ai

assistant = ai('dataset.json')
assistant.compile('model.nlite')
```

## Loading a Compiled Model 🔓
To make your dataset unreadable and to package it into a neat file.
```python
from neuralite.interpreter import ai

# To load a compiled model
assistant = ai.compiled('model.nlite')

cycle_end = False
while not cycle_end:
    message = input("Enter a message: ")
    if message.lower() == "stop":
        cycle_end = True
    else:
        print(assistant.process_input(message))
```
