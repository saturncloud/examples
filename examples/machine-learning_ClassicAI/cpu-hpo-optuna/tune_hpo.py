import time
import joblib
import ray
from ray import tune
from ray.tune.search import ConcurrencyLimiter
from ray.tune.search.optuna import OptunaSearch
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# 1. Define Objective (The "Black Box" function)
def objective(config):
    data = load_iris()
    X, y = data.data, data.target
    
    # Initialize model with current trial's hyperparameters
    clf = RandomForestClassifier(
        n_estimators=int(config["n_estimators"]),
        max_depth=int(config["max_depth"]),
        min_samples_split=float(config["min_samples_split"]),
        random_state=42
    )
    
    # Evaluate performance using Cross-Validation
    scores = cross_val_score(clf, X, y, cv=3)
    accuracy = scores.mean()
    
    # Report metric to Ray Tune
    tune.report({"accuracy": accuracy})

def run_hpo():
    print("🧠 Initializing Ray...")
    ray.init(configure_logging=False)

    # 2. Define Search Space
    search_space = {
        "n_estimators": tune.randint(10, 200),
        "max_depth": tune.randint(2, 20),
        "min_samples_split": tune.uniform(0.1, 1.0)
    }

    # 3. Setup Optuna Search Algorithm
    algo = OptunaSearch()
    algo = ConcurrencyLimiter(algo, max_concurrent=4) 

    print("🚀 Starting Tuning Job...")
    tuner = tune.Tuner(
        objective,
        tune_config=tune.TuneConfig(
            metric="accuracy",
            mode="max",
            search_alg=algo,
            num_samples=20,
        ),
        param_space=search_space,
    )

    results = tuner.fit()
    
    # 4. Process Best Result
    best_result = results.get_best_result("accuracy", "max")
    best_config = best_result.config
    
    print("\n" + "="*50)
    print(f"🏆 Best Accuracy: {best_result.metrics['accuracy']:.4f}")
    print(f"🔧 Best Config:   {best_config}")
    print("="*50)

    # 5. Retrain & Save Best Model
    print("💾 Retraining final model with best parameters...")
    data = load_iris()
    X, y = data.data, data.target
    
    final_model = RandomForestClassifier(
        n_estimators=int(best_config["n_estimators"]),
        max_depth=int(best_config["max_depth"]),
        min_samples_split=float(best_config["min_samples_split"]),
        random_state=42
    )
    final_model.fit(X, y)
    
    joblib.dump(final_model, "best_model.pkl")
    print("✅ Model saved to 'best_model.pkl'")

if __name__ == "__main__":
    run_hpo()