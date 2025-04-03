# model.py - simplified version
import pickle
import re
import numpy as np

class SimpleSentimentClassifier:
    def __init__(self):
        # Define positive and negative word lists
        self.positive_words = ["good", "great", "excellent", "amazing", "love", "happy", "best", "fantastic", "wonderful", "awesome"]
        self.negative_words = ["bad", "terrible", "worst", "hate", "poor", "awful", "horrible", "disappointing", "avoid", "regret"]
        
    def fit(self, X, y=None):
        # Nothing to fit in this simple model
        return self
    
    def predict(self, texts):
        results = []
        for text in texts:
            # Convert to string if not already (handles potential non-string inputs)
            if not isinstance(text, str):
                text = str(text)
            
            text = text.lower()
            # Use word boundaries to find whole words
            positive_count = sum(1 for word in self.positive_words if re.search(r'\b' + word + r'\b', text))
            negative_count = sum(1 for word in self.negative_words if re.search(r'\b' + word + r'\b', text))
            
            if positive_count > negative_count:
                results.append(2)  # Positive
            elif negative_count > positive_count:
                results.append(0)  # Negative
            else:
                results.append(1)  # Neutral
                
        return np.array(results)
    
    def predict_proba(self, texts):
        # Returns probabilities for compatibility
        results = []
        for text in texts:
            # Convert to string if not already
            if not isinstance(text, str):
                text = str(text)
                
            text = text.lower()
            # Use word boundaries for better matching
            positive_count = sum(1 for word in self.positive_words if re.search(r'\b' + word + r'\b', text))
            negative_count = sum(1 for word in self.negative_words if re.search(r'\b' + word + r'\b', text))
            total = positive_count + negative_count
            
            if total == 0:
                results.append([0.33, 0.34, 0.33])  # Equal probabilities
            else:
                neg_prob = negative_count / (total + 1)
                pos_prob = positive_count / (total + 1)
                neut_prob = 1 - neg_prob - pos_prob
                results.append([neg_prob, neut_prob, pos_prob])
                
        return np.array(results)

# Check if this file is being run directly (not imported)
if __name__ == "__main__":
    # Create a simple model
    model = SimpleSentimentClassifier()
    
    # Test it on a few examples to verify it works
    test_texts = ["This is amazing and wonderful!", 
                  "I hate this terrible product", 
                  "The weather is nice today"]
    
    predictions = model.predict(test_texts)
    probabilities = model.predict_proba(test_texts)
    
    print("Test predictions:", predictions)
    print("Test probabilities:")
    for i, text in enumerate(test_texts):
        print(f"'{text}': {probabilities[i]}")
    
    # Save the model to a file
    with open('sentiment_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("\nSimple sentiment model trained and saved as 'sentiment_model.pkl'")