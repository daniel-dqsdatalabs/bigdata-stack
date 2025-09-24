# Spark Streaming: Core Concepts and Critical Considerations  
*Last Updated: 2025-09-24*  

## Table of Contents  
1. [Fundamental Architecture](#1-fundamental-architecture)  
2. [Key Concepts](#2-key-concepts)  
3. [Critical Pitfalls](#3-critical-pitfalls)  
4. [Best Practices](#4-best-practices)  
5. [Performance Optimization](#5-performance-optimization)  

---

## 1. Fundamental Architecture  
Spark Streaming processes data using **micro-batch processing**, where live data streams are divided into small batches (e.g., 1-second intervals).  

### Core Components:  
- **DStream (Discretized Stream)**:  
  Sequence of RDDs representing data streams.  
  ```python  
  from pyspark.streaming import StreamingContext  
  ssc = StreamingContext(sc, batchDuration=1)  # 1-second batches  
  ```  
- **Structured Streaming**:  
  DataFrame/Dataset API with event-time semantics and end-to-end exactly-once guarantees.  

---

## 2. Key Concepts  
### A. Fault Tolerance  
- **Checkpointing**:  
  - *Metadata Checkpoints*: Save configuration to HDFS/S3 for driver recovery.  
  - *Data Checkpoints*: Save stateful computations (e.g., windowed operations).  
  ```scala  
  ssc.checkpoint("hdfs:///checkpoint_dir")  // DStream  
  query = df.writeStream.option("checkpointLocation", "/path")  // Structured  
  ```  

### B. State Management  
- **Stateful vs Stateless**:  
  - *Stateful*: Operations like `updateStateByKey` or `mapWithState` retain data across batches.  
  - *Stateless*: Transformations like `map` or `filter` process each batch independently.  

### C. Event-Time vs Processing-Time  
- **Watermarking**:  
  Handles late-arriving data in Structured Streaming:  
  ```python  
  df.withWatermark("eventTime", "10 minutes")  
  ```  

---

## 3. Critical Pitfalls  
### A. Checkpoint Incompatibility  
- Changing application code invalidates existing checkpoints.  
  **Solution**: Use versioned checkpoint directories.  

### B. Small Batch Sizes  
- Batches <500ms cause excessive scheduling overhead.  
  **Fix**: Monitor `batchProcessingTime` vs `batchInterval`.  

### C. State Store Bloat  
- Unbounded state growth in `updateStateByKey`.  
  **Mitigation**: Use `mapWithState` (DStream) or time-bound watermarks (Structured).  

### D. Data Skew in Window Operations  
- Uneven partition distribution in `reduceByKeyAndWindow`.  
  **Solution**: Repartition before window operations.  

### E. Timezone Mismanagement  
- Event-time processing uses UTC by default.  
  **Fix**: Explicitly set timezones in timestamps.  

---

## 4. Best Practices  
### A. Resource Allocation  
- Allocate 2-4 cores per receiver.  
- Reserve 10% memory for OS/buffers.  

### B. Serialization  
- Use Kryo serialization:  
  ```scala  
  conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")  
  ```  

### C. Monitoring  
- Track metrics:  
  - `numReceivedRecords`  
  - `processingDelay`  
  - `schedulingDelay`  

---

## 5. Performance Optimization  
### Tuning Strategies:  
| Parameter | Recommendation |  
|-----------|----------------|  
| `spark.streaming.blockInterval` | 200ms (balance parallelism/overhead) |  
| `spark.streaming.receiver.maxRate` | Limit to prevent resource starvation |  
| `spark.sql.shuffle.partitions` | Set to 2-3x cores for Structured Streaming |  

### Parallelism Techniques:  
1. **Kafka Direct Approach**:  
   ```python  
   directKafkaStream = KafkaUtils.createDirectStream(  
       ssc, [topic], {"metadata.broker.list": brokers}  
   )  
   ```  
2. **Backpressure**:  
   Enable `spark.streaming.backpressure.enabled=true`.  

---

## Summary Checklist  
- [ ] Validate checkpoint compatibility after code changes  
- [ ] Monitor batch processing vs scheduling delays  
- [ ] Test watermark thresholds for late data  
- [ ] Profile state store memory usage  
- [ ] Use structured streaming for end-to-end exactly-once  

