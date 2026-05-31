"""
Real-Time Enterprise Data Processing & Automation Pipeline
============================================================
Corporate Use Case: Simulated real-time data pipeline using
threading, deque (streaming buffer), heapq (priority processing),
and anomaly detection.
"""

import threading
import time
import random
import heapq
from collections import deque, Counter, defaultdict
from datetime import datetime

random.seed(42)


# ============================================================
# DATA STREAM SIMULATOR
# ============================================================

class SensorDataStream:
    """Simulates real-time sensor data stream."""

    SENSORS = ["TEMP-01", "TEMP-02", "PRESSURE-01", "HUMIDITY-01", "VIBRATION-01"]
    NORMAL_RANGES = {
        "TEMP": (20, 35),
        "PRESSURE": (100, 110),
        "HUMIDITY": (40, 60),
        "VIBRATION": (0, 5),
    }

    def __init__(self, num_readings=50):
        self.num_readings = num_readings
        self.readings = []

    def generate(self):
        """Generate sensor readings."""
        for i in range(self.num_readings):
            sensor = random.choice(self.SENSORS)
            sensor_type = sensor.split("-")[0]
            low, high = self.NORMAL_RANGES[sensor_type]

            # 15% chance of anomaly
            if random.random() < 0.15:
                value = round(random.uniform(high * 1.2, high * 1.8), 2)
            else:
                value = round(random.uniform(low, high), 2)

            reading = {
                "id": i + 1,
                "sensor": sensor,
                "type": sensor_type,
                "value": value,
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:12],
            }
            self.readings.append(reading)
        return self.readings


# ============================================================
# STREAMING BUFFER (DEQUE)
# ============================================================

class StreamBuffer:
    """Rolling buffer using deque for streaming data."""

    def __init__(self, maxlen=10):
        self.buffer = deque(maxlen=maxlen)
        self.lock = threading.Lock()

    def push(self, item):
        with self.lock:
            self.buffer.append(item)

    def get_all(self):
        with self.lock:
            return list(self.buffer)

    @property
    def moving_average(self):
        with self.lock:
            if not self.buffer:
                return 0
            return sum(r["value"] for r in self.buffer) / len(self.buffer)


# ============================================================
# PRIORITY PROCESSOR (HEAPQ)
# ============================================================

class PriorityProcessor:
    """Process readings by priority using heapq."""

    PRIORITY_MAP = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}

    def __init__(self):
        self.queue = []
        self.processed = []
        self.counter = 0  # Tie-breaker for heapq

    def classify_priority(self, reading):
        """Classify reading priority based on anomaly severity."""
        sensor_type = reading["type"]
        value = reading["value"]
        ranges = SensorDataStream.NORMAL_RANGES[sensor_type]

        if value > ranges[1] * 1.5:
            return "CRITICAL"
        elif value > ranges[1] * 1.2:
            return "HIGH"
        elif value > ranges[1]:
            return "MEDIUM"
        return "LOW"

    def enqueue(self, reading):
        """Add reading to priority queue."""
        priority_label = self.classify_priority(reading)
        priority_num = self.PRIORITY_MAP[priority_label]
        self.counter += 1
        heapq.heappush(self.queue, (priority_num, self.counter, reading, priority_label))

    def process_next(self):
        """Process highest priority reading."""
        if self.queue:
            priority, _, reading, label = heapq.heappop(self.queue)
            self.processed.append({"reading": reading, "priority": label})
            return reading, label
        return None, None


# ============================================================
# ANOMALY DETECTOR
# ============================================================

class AnomalyDetector:
    """Detect anomalies in sensor readings."""

    def __init__(self):
        self.anomalies = []
        self.sensor_counts = defaultdict(int)

    def check(self, reading):
        """Check if reading is anomalous."""
        sensor_type = reading["type"]
        value = reading["value"]
        low, high = SensorDataStream.NORMAL_RANGES[sensor_type]

        if value > high or value < low:
            severity = "CRITICAL" if value > high * 1.5 else "WARNING"
            anomaly = {
                "sensor": reading["sensor"],
                "value": value,
                "expected": f"{low}-{high}",
                "severity": severity,
            }
            self.anomalies.append(anomaly)
            self.sensor_counts[reading["sensor"]] += 1
            return anomaly
        return None


# ============================================================
# PIPELINE ORCHESTRATOR
# ============================================================

class DataPipeline:
    """Orchestrate the entire data processing pipeline."""

    def __init__(self):
        self.stream = SensorDataStream(num_readings=50)
        self.buffer = StreamBuffer(maxlen=10)
        self.processor = PriorityProcessor()
        self.detector = AnomalyDetector()
        self.stats = {"total": 0, "processed": 0, "anomalies": 0}

    def ingest(self, readings):
        """Stage 1: Ingest data into buffer."""
        for reading in readings:
            self.buffer.push(reading)
            self.stats["total"] += 1

    def detect_anomalies(self, readings):
        """Stage 2: Check for anomalies."""
        for reading in readings:
            anomaly = self.detector.check(reading)
            if anomaly:
                self.stats["anomalies"] += 1

    def prioritize(self, readings):
        """Stage 3: Enqueue for priority processing."""
        for reading in readings:
            self.processor.enqueue(reading)

    def process(self):
        """Stage 4: Process by priority."""
        while self.processor.queue:
            reading, priority = self.processor.process_next()
            if reading:
                self.stats["processed"] += 1

    def run(self):
        """Execute full pipeline."""
        readings = self.stream.generate()

        # Use threads for concurrent processing stages
        t1 = threading.Thread(target=self.ingest, args=(readings,))
        t2 = threading.Thread(target=self.detect_anomalies, args=(readings,))
        t3 = threading.Thread(target=self.prioritize, args=(readings,))

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        self.process()

    def report(self):
        """Generate pipeline report."""
        print(f"\n{''*60}")
        print("   PIPELINE STATISTICS")
        print(f"{''*60}")
        print(f"  Total readings:     {self.stats['total']}")
        print(f"  Processed:          {self.stats['processed']}")
        print(f"  Anomalies detected: {self.stats['anomalies']}")

        # Priority distribution
        priority_dist = Counter(r["priority"] for r in self.processor.processed)
        print(f"\n  Priority Distribution:")
        for priority in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            count = priority_dist.get(priority, 0)
            bar = "" * count
            print(f"    {priority:<10} {count:>3}  {bar}")

        # Anomaly report
        if self.detector.anomalies:
            print(f"\n{''*60}")
            print("    ANOMALY REPORT")
            print(f"{''*60}")
            print(f"  {'Sensor':<15} {'Value':>8} {'Expected':>10} {'Severity':<10}")
            print(f"  {''*43}")
            for a in self.detector.anomalies[:15]:
                print(f"  {a['sensor']:<15} {a['value']:>8.2f} {a['expected']:>10} {a['severity']:<10}")

            # Most problematic sensors
            print(f"\n  Most Problematic Sensors:")
            for sensor, count in sorted(self.detector.sensor_counts.items(),
                                        key=lambda x: -x[1]):
                print(f"    {sensor}: {count} anomalies")

        # Buffer state
        print(f"\n{''*60}")
        print("   BUFFER STATE (Last 10 readings)")
        print(f"{''*60}")
        print(f"  Moving Average: {self.buffer.moving_average:.2f}")
        for r in self.buffer.get_all()[-5:]:
            print(f"  [{r['timestamp']}] {r['sensor']}: {r['value']}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("   REAL-TIME DATA PROCESSING PIPELINE")
    print("=" * 60)

    pipeline = DataPipeline()

    print("\n   Running pipeline...")
    start = time.perf_counter()
    pipeline.run()
    elapsed = time.perf_counter() - start

    print(f"   Pipeline completed in {elapsed:.4f} seconds")

    pipeline.report()

    print(f"\n{'='*60}")
