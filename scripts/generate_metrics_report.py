"""
Complete example demonstrating metrics collection and report generation
Run this script to generate sample metrics and create a PowerPoint report
"""

import sys
import numpy as np
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from performance_metrics import (
    MetricsCollector,
    MetricsVisualizer,
    PowerPointReportGenerator
)


def generate_sample_healthcare_metrics():
    """Generate sample metrics for healthcare image classification"""
    
    print("=" * 80)
    print("GENERATING SAMPLE METRICS FOR QUANTUM FLOW - HEALTHCARE AI")
    print("=" * 80 + "\n")
    
    # Initialize collector
    collector = MetricsCollector("Quantum Flow - Healthcare AI System")
    
    # === ACCURACY METRICS ===
    print("📊 Recording Accuracy Metrics...")
    
    # Baseline Model
    collector.record_accuracy(
        model_name="ResNet50 Baseline",
        accuracy=0.8520,
        precision=0.8410,
        recall=0.8630,
        f1_score=0.8520,
        confusion_matrix={"TP": 86, "FP": 15, "TN": 92, "FN": 8}
    )
    
    # Classical CNN with advanced features
    collector.record_accuracy(
        model_name="Advanced CNN v2",
        accuracy=0.8810,
        precision=0.8750,
        recall=0.8890,
        f1_score=0.8820,
        confusion_matrix={"TP": 89, "FP": 12, "TN": 95, "FN": 5}
    )
    
    # Quantum Enhanced Model
    collector.record_accuracy(
        model_name="Quantum Enhanced CNN (AE-QIP)",
        accuracy=0.9210,
        precision=0.9180,
        recall=0.9240,
        f1_score=0.9210,
        confusion_matrix={"TP": 92, "FP": 8, "TN": 99, "FN": 2}
    )
    
    # === LATENCY METRICS ===
    print("⚡ Recording Latency Metrics...")
    
    # Simulate multiple API calls for each operation
    operations = {
        "Image Upload (Cloudinary)": (45, 8),      # Mean, std dev
        "Feature Extraction": (120, 15),
        "Model Inference": (85, 10),
        "Vector Search (Pinecone)": (35, 5),
        "Image Processing": (55, 8),
    }
    
    for op_name, (mean, std) in operations.items():
        for _ in range(15):
            latency = np.random.normal(mean, std)
            latency = max(latency, 1)  # Ensure positive
            throughput = 1000 / latency if latency > 0 else 0
            collector.record_latency(op_name, latency, throughput)
    
    # === EFFICIENCY METRICS ===
    print("💾 Recording Efficiency Metrics...")
    
    efficiency_data = {
        "Image Upload": (156.5, 32.1, 55.2, 0.0),  # memory, cpu, gpu, model_size
        "Feature Extraction": (512.3, 75.4, 85.2, 256.0),
        "Model Inference": (384.2, 68.5, 92.1, 128.0),
        "Vector Search": (256.8, 42.3, 45.1, 0.0),
        "Preprocessing": (128.5, 45.2, 62.1, 0.0),
    }
    
    for op_name, (mem, cpu, gpu, model_size) in efficiency_data.items():
        collector.record_efficiency(
            operation=op_name,
            memory_mb=mem,
            cpu_percent=cpu,
            gpu_percent=gpu,
            model_size_mb=model_size if model_size > 0 else None
        )
    
    # === PRINT SUMMARY ===
    collector.print_summary()
    
    # === SAVE METRICS ===
    print("\n💾 Saving metrics to JSON...")
    collector.save_metrics("metrics_data.json")
    
    return collector


def generate_sample_multimodal_metrics():
    """Generate sample metrics for multi-domain (healthcare, satellite, surveillance)"""
    
    print("\n" + "=" * 80)
    print("GENERATING MULTI-DOMAIN METRICS")
    print("=" * 80 + "\n")
    
    collector = MetricsCollector("Quantum Flow - Multi-Domain AI System")
    
    # Healthcare metrics
    collectors = {}
    domains = [
        ("Healthcare Classification", 0.921, 0.918, 0.924, 0.921),
        ("Satellite Image Analysis", 0.845, 0.832, 0.858, 0.845),
        ("Surveillance Detection", 0.876, 0.871, 0.881, 0.876),
    ]
    
    for domain_name, acc, prec, rec, f1 in domains:
        collector.record_accuracy(
            model_name=domain_name,
            accuracy=acc,
            precision=prec,
            recall=rec,
            f1_score=f1
        )
    
    # API latencies
    api_endpoints = [
        "POST /upload",
        "GET /search",
        "POST /classify",
        "GET /analytics",
        "POST /extract-features",
    ]
    
    for endpoint in api_endpoints:
        for _ in range(10):
            latency = np.random.normal(65, 12)
            latency = max(latency, 5)
            collector.record_latency(endpoint, latency, 1000/latency)
    
    # System efficiency
    collector.record_efficiency(
        operation="Full Pipeline",
        memory_mb=1024.5,
        cpu_percent=55.3,
        gpu_percent=78.5,
        model_size_mb=640.0
    )
    
    collector.print_summary()
    collector.save_metrics("multimodal_metrics.json")
    
    return collector


def create_visualization_and_report(collector: MetricsCollector, 
                                   output_name: str = "Performance_Report.pptx"):
    """Generate visualizations and PowerPoint report"""
    
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS AND POWERPOINT REPORT")
    print("=" * 80 + "\n")
    
    # Create visualizer
    visualizer = MetricsVisualizer(collector)
    
    print("📈 Creating charts...")
    visualizer.create_accuracy_comparison_chart()
    visualizer.create_latency_chart()
    visualizer.create_throughput_chart()
    visualizer.create_efficiency_chart()
    
    print("💾 Saving charts as PNG...")
    visualizer.save_all_figures("metrics_charts")
    
    # Generate PowerPoint report
    print("📊 Generating PowerPoint report...")
    report_gen = PowerPointReportGenerator(collector, visualizer)
    report_file = report_gen.generate_report(output_name)
    
    print(f"\n✅ Report generated: {report_file}")
    return report_file


def main():
    """Main execution"""
    
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  QUANTUM FLOW - PERFORMANCE METRICS COLLECTION & REPORTING SYSTEM  ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Step 1: Generate healthcare metrics
    healthcare_collector = generate_sample_healthcare_metrics()
    
    # Step 2: Generate multimodal metrics
    multimodal_collector = generate_sample_multimodal_metrics()
    
    # Step 3: Create visualization and reports
    print("\n" + "=" * 80)
    print("GENERATING HEALTHCARE REPORT")
    print("=" * 80)
    create_visualization_and_report(
        healthcare_collector, 
        "Healthcare_Performance_Report.pptx"
    )
    
    print("\n" + "=" * 80)
    print("GENERATING MULTIMODAL REPORT")
    print("=" * 80)
    create_visualization_and_report(
        multimodal_collector,
        "MultiDomain_Performance_Report.pptx"
    )
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ METRICS GENERATION COMPLETE!")
    print("=" * 80)
    print("\n📁 Generated Files:")
    print("  ✓ metrics_data.json - Healthcare metrics data")
    print("  ✓ multimodal_metrics.json - Multi-domain metrics data")
    print("  ✓ metrics_charts/ - Directory with performance charts (PNG)")
    print("  ✓ Healthcare_Performance_Report.pptx - Healthcare presentation")
    print("  ✓ MultiDomain_Performance_Report.pptx - Multi-domain presentation")
    print("\n📊 Charts included in presentation:")
    print("  1. Accuracy Comparison - Model performance metrics")
    print("  2. Latency Performance - Response times across endpoints")
    print("  3. Throughput Analysis - Processing capacity per operation")
    print("  4. Efficiency Metrics - Memory, CPU, GPU usage breakdown")
    print("  5. Summary Statistics - Key performance indicators")
    print("\n💡 Next Steps:")
    print("  1. Review the PowerPoint reports for your presentation")
    print("  2. Integrate MetricsCollector into your FastAPI backend")
    print("  3. Use @track_api_latency decorator on your endpoints")
    print("  4. Schedule periodic metric collection and report generation")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    # Import here to avoid issues if module not available
    from performance_metrics import MetricsVisualizer
    main()
