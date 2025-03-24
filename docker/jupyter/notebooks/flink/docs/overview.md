
# Flink Overview

### Architecture

---

### Streaming Process

---

##### Batch Processing

---
In this paradigm, also know as `bounded data streams`,  you can choose to ingest the entire dataset before producing any results, which means that is possible to sort the data, compute global statistics or produce a final report that summarizes all of the inputs.

##### Stream Processing

---
On the other hand, involves `unbounded data streams` where the input may never end and so you are forced to continuously process the data as it arrives.

##### Streaming DataFlows

---
In Flink, applications are composed of `streaming dataflows` that may be transformed by `user-defined operators`. These dataflows form direct graphs that start with one or more sources and end in one or more sinks.
![[Screenshot 2024-09-12 at 21.24.07.png]]
Often there is a one-to-one correspondence between the transformations in the program and the operators in the dataflow. Sometimes, however, one transformation may consist of multiple operators.

An application may consume real-time data from streaming sources such as message queues or distributed logs, like Apache Kafka or Kinesis. But flink can also consume bounded, historic data from a variety of data sources. Similarly, the streams of results being produced by a Flink application can be sent to a wide variety of systems that can be connected as sinks.

![[Screenshot 2024-09-12 at 21.29.12.png]]

##### Parallels DataFlows

---
Programs in Flink are by default parallel and distributed. During execution, a stream has one or more `stream partitions`, and each operator has one or more `operation subtasks`. The operator subtasks are independent of one another, and execute in different threads and possibly on different machines or containers.

The number of operator subtasks is the parallelism of that particular operator. Different operator of the same program may have different levels of parallelism.
