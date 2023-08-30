import json
import random
import base64
import re
import time

class ai:
    def __init__(self, dataset_file=None, dataset=None, is_compiled=False):
        if is_compiled:
            print("Loading model...")
        else:
            print("Loading dataset...")
            
            print("Training model...")
            for epoch in range(1, 6):
                print(f"Epoch {epoch}/5")
                time.sleep(0.3)

        if dataset:
            self.dataset = dataset
        elif dataset_file:
            with open(dataset_file, 'r') as f:
                self.dataset = json.load(f)
        else:
            raise ValueError("Either a dataset_file or a dataset must be provided.")

    @classmethod
    def compiled(cls, filename):
        with open(filename, 'rb') as f:
            encoded_data = f.read()
        decoded_data = json.loads(base64.b64decode(encoded_data).decode('utf-8'))
        return cls(dataset=decoded_data, is_compiled=True)

    def compile(self, filename):
        encoded_data = base64.b64encode(json.dumps(self.dataset).encode('utf-8'))
        with open(filename, 'wb') as f:
            f.write(encoded_data)
        print("Successfully compiled dataset into " + filename)

    def load_dataset(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    def find_best_match(self, input):
        # Remove punctuations from input
        input_clean = re.sub(r'[^\w\s]', '', input).lower()

        # Look for exact or substring matches
        for key in self.dataset.keys():
            for pattern in self.dataset[key]:
                # Remove punctuations from pattern
                pattern_clean = re.sub(r'[^\w\s]', '', pattern).lower()

                if pattern_clean in input_clean:
                    return key

        # Look for individual word matches
        input_words = input_clean.split()
        for key in self.dataset.keys():
            for pattern in self.dataset[key]:
                pattern_words = pattern.lower().split()
                if any(word in pattern_words for word in input_words):
                    return key

        return None

    def process_input(self, user_input):
        best_match_key = self.find_best_match(user_input)
        if best_match_key:
            response_key = f"{best_match_key}_responses"
            if response_key in self.dataset:
                return random.choice(self.dataset[response_key])  # Choose a random response
        return "I don't understand."
