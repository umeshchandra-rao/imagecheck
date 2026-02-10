"""
Quick test to verify metrics imports work correctly
Run this to test before starting the backend
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing imports...")

try:
    print("1. Testing scripts.metrics_integration import...")
    from scripts.metrics_integration import metrics_collector, track_api_latency, track_model_inference
    print("   ✅ metrics_integration imported successfully")
    
    print("\n2. Testing scripts.performance_metrics import...")
    from scripts.performance_metrics import MetricsCollector, MetricsVisualizer, PowerPointReportGenerator
    print("   ✅ performance_metrics imported successfully")
    
    print("\n3. Testing metrics_collector...")
    print(f"   Project: {metrics_collector.project_name}")
    print("   ✅ metrics_collector works")
    
    print("\n4. Testing decorator...")
    @track_api_latency("test_operation")
    def test_func():
        return "test"
    
    result = test_func()
    print(f"   Result: {result}")
    print("   ✅ @track_api_latency decorator works")
    
    print("\n" + "="*60)
    print("✅ ALL IMPORTS WORKING! Backend should start successfully.")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
