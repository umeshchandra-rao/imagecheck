"""
Integration helper for metrics collection into FastAPI backend
Shows how to track API performance, model inference, and resource usage
"""

import time
import psutil
from functools import wraps
from typing import Callable, Any
import asyncio
import sys
from pathlib import Path

# Add scripts directory to path if needed
_current_dir = Path(__file__).parent
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

from performance_metrics import MetricsCollector


# Global metrics collector instance
metrics_collector = MetricsCollector("Quantum Flow - Multi-Domain AI")


def track_api_latency(operation_name: str = None) -> Callable:
    """
    Decorator to track API endpoint latency
    
    Usage:
        @app.post("/upload")
        @track_api_latency("image_upload")
        async def upload_image(file: UploadFile):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            op_name = operation_name or func.__name__
            start_time = time.perf_counter()
            
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                throughput = 1000 / latency_ms  # items per second
                metrics_collector.record_latency(op_name, latency_ms, throughput)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            op_name = operation_name or func.__name__
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                throughput = 1000 / latency_ms
                metrics_collector.record_latency(op_name, latency_ms, throughput)
        
        # Return async or sync wrapper depending on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def track_model_inference(model_name: str, accuracy: float = None, 
                         precision: float = None, recall: float = None, 
                         f1_score: float = None):
    """
    Record model inference metrics
    
    Usage:
        predictions = model.predict(image)
        track_model_inference(
            "ResNet50",
            accuracy=0.85,
            precision=0.82,
            recall=0.88,
            f1_score=0.85
        )
    """
    metrics_collector.record_accuracy(
        model_name=model_name,
        accuracy=accuracy or 0.0,
        precision=precision or 0.0,
        recall=recall or 0.0,
        f1_score=f1_score or 0.0
    )


def track_resource_usage(operation_name: str, model_size_mb: float = None) -> Callable:
    """
    Decorator to track CPU, memory, and GPU usage
    
    Usage:
        @track_resource_usage("feature_extraction", model_size_mb=128.5)
        def extract_features(image):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            process = psutil.Process()
            
            # Record before execution
            mem_before = process.memory_info().rss / 1024 / 1024  # MB
            cpu_percent_start = process.cpu_percent(interval=0.1)
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # Record after execution
                mem_after = process.memory_info().rss / 1024 / 1024
                cpu_percent_end = process.cpu_percent(interval=0.1)
                memory_used = mem_after - mem_before
                
                metrics_collector.record_efficiency(
                    operation=operation_name,
                    memory_mb=memory_used,
                    cpu_percent=(cpu_percent_start + cpu_percent_end) / 2,
                    gpu_percent=None,  # Would need GPU monitoring library
                    model_size_mb=model_size_mb
                )
        
        return wrapper
    
    return decorator


class MetricsMiddleware:
    """
    FastAPI middleware for tracking all API requests
    
    Usage in FastAPI app:
        app.add_middleware(MetricsMiddleware)
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        path = scope.get("path", "")
        method = scope.get("method", "")
        
        start_time = time.perf_counter()
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                elapsed = (time.perf_counter() - start_time) * 1000
                operation = f"{method} {path}"
                metrics_collector.record_latency(operation, elapsed)
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)


# === FastAPI Integration Example ===

# Here's how to use this in your backend_server.py:
"""
from fastapi import FastAPI
from metrics_integration import (
    metrics_collector, 
    track_api_latency, 
    track_model_inference,
    track_resource_usage,
    MetricsMiddleware
)

app = FastAPI()

# Add metrics middleware
app.add_middleware(MetricsMiddleware)


# Example 1: Track upload endpoint
@app.post("/api/upload")
@track_api_latency("cloudinary_upload")
async def upload_to_cloudinary(file: UploadFile):
    # Upload logic here
    pass


# Example 2: Track search endpoint  
@app.get("/api/search")
@track_api_latency("vector_search")
async def search_images(query: str):
    # Search logic here
    pass


# Example 3: Track model inference
@app.post("/api/classify")
@track_api_latency("model_inference")
async def classify_image(file: UploadFile):
    # Classification logic
    accuracy = 0.892
    precision = 0.885
    recall = 0.899
    f1 = 0.892
    
    track_model_inference(
        "Quantum Enhanced CNN",
        accuracy, precision, recall, f1
    )
    
    return {"result": "...", "confidence": accuracy}


# Example 4: Track feature extraction
@app.post("/api/extract-features")
@track_resource_usage("feature_extraction", model_size_mb=256)
async def extract_features(file: UploadFile):
    # Feature extraction logic
    pass


# Example 5: Generate metrics report
@app.get("/api/metrics/report")
async def get_metrics_report():
    metrics_collector.print_summary()
    return metrics_collector.get_accuracy_summary()


# Example 6: Export PowerPoint report
@app.get("/api/metrics/export")
async def export_report():
    from performance_metrics import PowerPointReportGenerator, MetricsVisualizer
    
    visualizer = MetricsVisualizer(metrics_collector)
    reporter = PowerPointReportGenerator(metrics_collector, visualizer)
    report_file = reporter.generate_report()
    
    return {"report": report_file}
"""


# === Data Collection Helper Functions ===

def calculate_model_metrics(predictions, ground_truth):
    """
    Calculate accuracy, precision, recall, F1 from predictions
    
    Args:
        predictions: Model predictions (list or array)
        ground_truth: True labels (list or array)
    
    Returns:
        Dict with accuracy, precision, recall, f1_score
    """
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score
    )
    
    try:
        acc = accuracy_score(ground_truth, predictions)
        prec = precision_score(ground_truth, predictions, average='weighted', zero_division=0)
        rec = recall_score(ground_truth, predictions, average='weighted', zero_division=0)
        f1 = f1_score(ground_truth, predictions, average='weighted', zero_division=0)
        
        return {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1
        }
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None


def get_gpu_stats():
    """
    Get GPU usage stats (requires nvidia-ml-py)
    Install: pip install nvidia-ml-py
    """
    try:
        from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        res = nvmlDeviceGetUtilizationRates(handle)
        return res.gpu  # GPU usage percentage
    except:
        return None


def benchmark_function(func, num_runs: int = 10, *args, **kwargs):
    """
    Run benchmark on a function and collect latency stats
    
    Usage:
        stats = benchmark_function(model.predict, 100, image=test_image)
        print(stats)
    """
    import numpy as np
    
    latencies = []
    
    for _ in range(num_runs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)  # Convert to ms
    
    return {
        "mean": np.mean(latencies),
        "median": np.median(latencies),
        "min": np.min(latencies),
        "max": np.max(latencies),
        "std": np.std(latencies),
        "p95": np.percentile(latencies, 95),
        "p99": np.percentile(latencies, 99),
        "samples": num_runs
    }


# Example of benchmarking usage
if __name__ == "__main__":
    print("Metrics Integration Module Loaded Successfully!")
    print("\nAvailable functions:")
    print("  - track_api_latency(operation_name)")
    print("  - track_model_inference(model_name, accuracy, precision, recall, f1_score)")
    print("  - track_resource_usage(operation_name, model_size_mb)")
    print("  - MetricsMiddleware - Automatic API tracking")
    print("  - calculate_model_metrics(predictions, ground_truth)")
    print("  - benchmark_function(func, num_runs, *args, **kwargs)")
    print("  - get_gpu_stats()")
