# PySpark (Batch Processing): Core Concepts and Critical Considerations  
*Last Updated: 2025-09-24*  

## Table of Contents  
1. [Fundamental Architecture](#1-fundamental-architecture)  
2. [Key Concepts](#2-key-concepts)  
3. [Critical Pitfalls](#3-critical-pitfalls)  
4. [Best Practices](#4-best-practices)  
5. [Performance Optimization](#5-performance-optimization)  

---

## 1. Fundamental Architecture  
PySpark processes data through **lazy evaluation** and **Directed Acyclic Graph (DAG)** execution, optimizing operations before execution.  

### Core Components:  
- **RDD (Resilient Distributed Dataset)**:  
  Immutable distributed collection of objects partitioned across nodes.  
  ```python  
  rdd = sc.parallelize([1,2,3,4,5])  
  ```  
- **DataFrame/Dataset**:  
  Structured API with schema enforcement and Catalyst optimizer.  
  ```python  
  df = spark.read.parquet("data.parquet")  
  ```  
- **SparkSession**:  
  Entry point for DataFrame and SQL operations:  
  ```python  
  from pyspark.sql import SparkSession  
  spark = SparkSession.builder.appName("example").getOrCreate()  
  ```  

---

## 2. Key Concepts  
### A. Execution Model  
- **Stages**:  
  Groups of tasks that can be executed together (narrow vs wide transformations).  
- **Shuffling**:  
  Data redistribution between executors (e.g., during `groupBy` or `join`).  

### B. Memory Management  
- **Storage Memory**:  
  Cached data using `persist()` or `cache()`.  
  ```python  
  df.persist(StorageLevel.MEMORY_AND_DISK)  
  ```  
- **Execution Memory**:  
  Used for shuffles, joins, and aggregations.  

### C. Partitioning  
- **Optimal Partition Size**:  
  Target 128MB-200MB per partition.  
  ```python  
  df = df.repartition(100)  # Explicit partitioning  
  ```  

---

## 3. Critical Pitfalls  
### A. OOM (Out-of-Memory) Errors  
- **Cause**:  
  Improper caching or large driver collections via `collect()`.  
  **Solution**:  
  ```python  
  df.limit(1000).collect()  # Instead of full collect  
  ```  

### B. Shuffle Overhead  
- **Symptom**:  
  Slow `groupBy`/`join` operations.  
  **Fix**:  
  ```python  
  spark.conf.set("spark.sql.shuffle.partitions", "200")  
  ```  

### C. Skewed Data Distribution  
- **Detection**:  
  Uneven task durations in Spark UI.  
  **Mitigation**:  
  ```python  
  from pyspark.sql.functions import rand  
  df = df.withColumn("salt", rand() * numBuckets)  
  ```  

### D. UDF Performance  
- **Warning**:  
  Python UDFs (User Defined Functions) bypass Catalyst optimization.  
  **Alternative**:  
  Use built-in functions or Scala UDFs via `pandas_udf`.  

---

## 4. Best Practices  
### A. Data Handling  
1. **Schema Enforcement**:  
   ```python  
   from pyspark.sql.types import StructType, IntegerType  
   schema = StructType().add("id", IntegerType(), nullable=False)  
   ```  
2. **File Formats**:  
   Prefer Parquet/ORC over CSV for large datasets.  

### B. Resource Configuration  
| Parameter | Recommendation |  
|-----------|----------------|  
| `spark.executor.memory` | 4g-8g (leave 1GB for OS) |  
| `spark.executor.cores` | 3-5 cores per executor |  
| `spark.dynamicAllocation.enabled` | `true` for variable workloads |  

### C. Monitoring Tools  
- **Spark UI**:  
  Access at `http://driver-node:4040`  
- **Logging**:  
  ```python  
  spark.sparkContext.setLogLevel("WARN")  
  ```  

---

## 5. Performance Optimization  
### Tuning Strategies:  
1. **Broadcast Join**:  
   ```python  
  spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "100485760")  # ~100MB  
  ```  
2. **Predicate Pushdown**:  
   ```python  
  df.filter("date > '2025-01-01'").explain()  # Check filter placement  
  ```  
3. **Code Generation**:  
   Verify whole-stage codegen in physical plan:  
   ```  
   == Physical Plan ==  
   *(1) Project [...]  
   +- *(1) Filter [...]  
   ```  

### Advanced Techniques:  
- **Partition Pruning**:  
  ```python  
  df = spark.read.parquet("path/date=20250924")  
  ```  
- **Z-Ordering**:  
  (Delta Lake specific)  
  ```python  
  df.write.format("delta").option("delta.autoOptimize.optimizeWrite", "true")  
  ```  

---

## Summary Checklist  
- [ ] Validate partition sizes (128-200MB range)  
- [ ] Check Spark UI for skewed tasks  
- [ ] Use `.persist()` judiciously with storage levels  
- [ ] Prefer DataFrame API over RDDs for optimizer benefits  
- [ ] Monitor garbage collection time in executor logs  

