# mlops.py
import pickle
import requests
import json
import os
import time
from sklearn.metrics import accuracy_score

def test_model_accuracy(model_path):
    """Test the model accuracy on a test dataset"""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Test data
    test_data = [
        "I absolutely love this product",
        "This is the worst thing I've ever bought",
        "It's okay but not great",
        "Amazing service, highly recommend",
        "Completely useless and a waste of money"
    ]
    # 2: positive, 0: negative, 1: neutral
    test_labels = [2, 0, 1, 2, 0]
    
    # Make predictions
    predictions = model.predict(test_data)
    
    # Calculate metrics
    accuracy = accuracy_score(test_labels, predictions)
    
    return accuracy

def test_api_performance(url="http://localhost:5000/predict"):
    """Test the API performance"""
    test_cases = [
        {"text": "I love this product", "expected": "positive"},
        {"text": "This is terrible", "expected": "negative"},
        {"text": "It's okay", "expected": "neutral"}
    ]
    
    results = []
    response_times = []
    
    for test in test_cases:
        start_time = time.time()
        response = requests.post(url, json={"text": test["text"]})
        end_time = time.time()
        
        response_times.append(end_time - start_time)
        
        if response.status_code == 200:
            data = response.json()
            results.append(data["sentiment"] == test["expected"])
        else:
            results.append(False)
    
    return {
        "success_rate": sum(results) / len(results) * 100,
        "avg_response_time": sum(response_times) / len(response_times)
    }

def register_model(model_path, version, performance_metrics):
    """Simulated function to register model in a model registry"""
    # In a real-world scenario, this would push to MLflow, Azure ML, etc.
    registry_dir = "model_registry"
    
    if not os.path.exists(registry_dir):
        os.makedirs(registry_dir)
    
    # Create metadata file
    metadata = {
        "version": version,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "accuracy": performance_metrics.get("accuracy", 0),
        "api_success_rate": performance_metrics.get("success_rate", 0),
        "api_response_time": performance_metrics.get("avg_response_time", 0)
    }
    
    with open(f"{registry_dir}/model_v{version}_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Copy the model file to the registry
    with open(model_path, "rb") as src, open(f"{registry_dir}/model_v{version}.pkl", "wb") as dst:
        dst.write(src.read())
    
    return f"{registry_dir}/model_v{version}.pkl"

if __name__ == "__main__":
    # Test current model
    model_path = "sentiment_model.pkl"
    accuracy = test_model_accuracy(model_path)
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    
    # Test API if it's running
    try:
        api_performance = test_api_performance()
        print(f"API success rate: {api_performance['success_rate']:.2f}%")
        print(f"API average response time: {api_performance['avg_response_time'] * 1000:.2f}ms")
    except Exception as e:
        print(f"API is not available for testing: {e}")
        api_performance = {}
    
    # Register the model
    version = "1.0.0"  # In real scenario, would be determined dynamically
    performance_metrics = {
        "accuracy": accuracy,
        **api_performance
    }
    
    registered_path = register_model(model_path, version, performance_metrics)
    print(f"Model registered at: {registered_path}")