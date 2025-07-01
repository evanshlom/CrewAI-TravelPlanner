#!/usr/bin/env python3
from langsmith import Client
from langsmith.evaluation import evaluate
from src.main import run
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any

def load_dataset(path: str):
    with open(path, 'r') as f:
        return json.load(f)

def predict(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Run crew and return response for evaluation."""
    response = run(inputs["query"])
    return {"response": str(response)}

def semantic_similarity(run, example) -> dict:
    """Evaluate semantic similarity using LangSmith's built-in evaluator."""
    from langchain.evaluation import load_evaluator
    from langchain_anthropic import ChatAnthropic
    
    evaluator = load_evaluator(
        "labeled_score_string",
        llm=ChatAnthropic(model="claude-3-haiku-20240307"),
        normalize_by=1.0
    )
    
    result = evaluator.evaluate_strings(
        prediction=run.outputs.get("response", ""),
        reference=example.outputs.get("response", ""),
        input=example.inputs.get("query", "")
    )
    
    return {"key": "semantic_similarity", "score": result["score"]}

def main():
    load_dotenv()
    
    if not os.getenv("LANGSMITH_API_KEY"):
        print("Error: LANGSMITH_API_KEY not found")
        return
    
    client = Client()
    
    # Load validation data
    examples = load_dataset("data/validation_dataset.json")
    
    # Create dataset
    dataset_name = "allegiant-travel-validation"
    
    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
    except:
        dataset = client.create_dataset(dataset_name=dataset_name)
        
    # Add examples
    for ex in examples:
        client.create_example(
            inputs={"query": ex["input"]},
            outputs={"response": ex["expected_output"]},
            dataset_id=dataset.id
        )
    
    # Run evaluation
    results = evaluate(
        predict,
        data=dataset_name,
        evaluators=[semantic_similarity],
        experiment_prefix="allegiant-crew"
    )
    
    print(f"\nEvaluation complete! View at: https://smith.langchain.com")

if __name__ == "__main__":
    main()