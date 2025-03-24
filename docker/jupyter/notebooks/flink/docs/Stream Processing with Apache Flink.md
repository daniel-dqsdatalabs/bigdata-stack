# Stream Processing with Apache Flink

**Apache Flink** is a distributed stream processor that implements stateful stream processing applications. It efficiently runs such applications at large scale in a fault-tolerant manner.

## 1. Stateful Stream Processing

**Topics:**
- 1.1 Event-Driven Applications
- 1.2 Data Pipelines
- 1.3 Stream Analytics

Stateful stream processing is an application design pattern for processing unbounded streams of events. Any application that processes a stream of events that has transformations in multiple records at once needs to be stateful, with the ability to store and access intermediate data. When an application receives an event, it can perform arbitrary computations that involve reading data from or writing data to the state. State can be stored and accessed in many different places including program variables, local files, or embedded or external databases.

Flink stores the application state locally in memory or in an embedded database. Since Flink is a distributed system, the local state needs to be protected against failures to avoid data loss in case of application or machine failure. Flink guarantees this by periodically writing a consistent checkpoint of the application state to a remote and durable storage.

> **Event Log Systems**
>
> Stateful stream processing applications often ingest their incoming events from an event log system. An event log system stores and distributes event streams. Events are written to a durable, append-only log, which means that the order of written events cannot be changed. Stream that is written to an event log can be read many times by the same or different consumers. Due to the append-only property of the log, events are always published to all consumers in exactly the same order. Apache Kafka is the most popular event log system.

Connecting a stateful streaming application running on Flink and an event log system is an interesting approach, since in this architecture the event log persists the input events and can replay them in deterministic order. In case of failure, Flink recovers a stateful streaming application by restoring its state from a previous checkpoint and resetting the read position on the event log. The application will replay (and fast forward) the input events from the event log until it reaches the tail of the stream. This technique is used to recover from failures but can also be leveraged to update an application, fix bugs and repair previously emitted results, migrate an application to a different cluster, or perform A/B tests with different application versions.

> **Note:**
>
> A/B tests, also known as split testing, are experiments conducted in marketing and UX design to compare two versions of a webpage or app to determine which one performs better. The A version (control) is usually the current design, while the B version (variation) has one element changed. By running A/B tests, businesses can make data-driven decisions to optimize their design and improve user experience, leading to higher conversions and better outcomes.

### 1.1 Event-Driven Applications

Event-driven applications are stateful streaming applications that ingest event streams and process the events with application-specific business logic. Depending on the business logic, an event-driven application can trigger actions such as sending an alert or an email or write events to an outgoing event stream to be consumed by another event-driven application.

> **Note:**
>
> This type of application are an evolution of microservices. They communicate via event logs instead of REST calls and hold application data as local state instead of writing it to and reading it from an external datastore. So, one application emits its output to an event log and another application consumes the events the other application emitted. The event log decouples senders and receivers and provides asynchronous, nonblocking event transfer. Each application can be stateful and can locally manage its own state without accessing external datastores.

### 1.2 Data Pipelines

A traditional approach to synchronize data in different storage systems is periodic ETL jobs. However, they do not meet the latency requirements for many of today's use cases. An alternative is to use an event log to distribute updates. The updates are written to and distributed by the event log. Consumers of the log incorporate the updates into the affected data stores. Depending on the use case, the transferred data may need to be normalized, enriched with external data, or aggregated before it is ingested by the target data store.

Ingesting, transforming, and inserting data with low latency is another common user case for stateful stream processing applications. This type of applications is called a data pipeline.

> **Important:**
>
> Data pipelines must be able to process large amount of data in a short time. A processor that operates a data pipeline should also feature many source and sink connectors to read data from and write data to various storage systems.

### 1.3 Stream Analytics

A streaming analytics application continuously ingests streams of events and updates its result by incorporating the latest events with low latency. Typically, streaming applications store their result in an external data store that supports efficient updates, such as a database or key-value store. The live updated results of a streaming analytics application can be used to power dashboard applications.

## 2. Stream Processing Fundamentals

**Topics:**
- 2.1 Dataflow Graphs
- 2.2 Data Parallelism and Task Parallelism
- 2.3 Data Exchange Strategies
- 2.4 Latency and Throughput
- 2.5 Operations on Data Streams

### 2.1 Dataflow Graphs

Describes how data flows between operations. Dataflow programs are commonly represented as direct graphs, where nodes are called operators and represent computations and edges represent data dependencies. Operators are the basic functional units of a dataflow application. They consume data from inputs, perform a computation on them, and produce data to outputs for further processing. Operators without inputs are called data sources and operators without outputs are called data sinks. A dataflow graph must have at least one data source and one data sink.

![Dataflow Graph Example](./Screenshot%202024-09-13%20at%2012.23.42.png)

This type of dataflow are called logical because they convey a high-level view of the computation logic. In order to execute a dataflow program, its logical graph is converted into a *physical dataflow graph, which specifies in detail how the program is executed*.

### 2.2 Data Parallelism and Task Parallelism

You can exploit parallelism in dataflow graphs in different ways.

> **Data Parallelism (Same Operator)**
>
> First, you can partition your input data and have tasks of the same operation execute on the data subsets in parallel. Data parallelism is useful because it allows for processing large volumes of data and spreading the computation load across several computing nodes.

> **Task Parallelism (Different Operators)**
>
> Second, you can have tasks from different operators performing computations on the same or different data in parallel. Using task parallelism, you can better utilize the computing resources of a cluster.

### 2.3 Data Exchange Strategies

**Data exchange strategies define how data items are assigned to tasks in a physical dataflow graph**. It can be automatically chosen by the execution engine depending on the semantics of the operators or explicitly imposed by the dataflow programmer.

> **Data Exchange Strategies:**
>
> - **Forward Strategy**:
>   The forward strategy sends data from a task to a receiving task. If both tasks are located on the same physical machine (which is often ensured by task schedulers), this exchange strategy avoids network communications.
> - **Broadcast Strategy**:
>   Sends every data item to all parallel tasks of an operator. Because this strategy replicates data and involves network communication, it is fairly expensive.
> - **Key-Based Strategy**:
>   Partitions data by a key attribute and guarantees that data items having the same key will be processed by the same task. In figure 1, the output of the "Extract Hashtags" operator is partitioned by the key (the hashtag), so that the count operator tasks can correctly compute the occurrences of each hashtag.
> - **Random Strategy**:
>   Uniformly distributes data items to operator tasks in order to evenly distribute the load across computing tasks.

### 2.4 Latency and Throughput

**While you want latency to be as low as possible, you generally want throughput to be as high as possible.**

> **Latency**
>
> Indicates how long it takes for an event to be processed. Essentially, it is the time interval between receiving an event and seeing the effect of processing this event in the output. In data streaming, latency is measured in units of time, such as milliseconds. Depending of the application, you might care about average latency, maximum latency, or percentile latency. For example, a 95th-percentile latency value of 10 ms means that 95% of events are processed within 10 ms.

> **Throughput**
>
> Is a measure of the system's processing capacity - its rate of processing. That is, throughput tells us how many events the system can process per time unit. Throughput is measured in events or operations per time unit. **It is important to note that the rate of processing depends on the rate of arrival; low throughput does not necessarily indicates bad performance.**

> **Peak Throughput**
>
> Refers to the performance limit when your system is at its maximum load. Ideally, you would like to keep the latency constant and independent of the rate of the incoming events. However, once we reach a rate of incoming events such that the system resources are fully used, we will have to start buffering events. At this point, the system has reached its peak throughput and further increasing the event rate will only result in worse latency. If the system continues to receive data at a higher rate than it can handle, buffers might become unavailable and data might get lost. **This situation is commonly know as backpressure and there are different strategies to deal with it.**

#### Latency vs Throughput

At this point, it should be clear that latency and throughput are not independent metrics. If events take a long time to travel in the data processing pipeline, we cannot easily ensure high throughput. Similarly, if a system's capacity is small, events will be buffered and have to wait before they get processed. The main takeaway here is that lowering latency increases throughput. Naturally, if a system can perform operations faster, it can perform more operations in the same amount of time. In fact, that's what happens when you exploit parallelism in a stream processing pipeline. By processing several streams in parallel, you lower the latency while processing more events at the same time.

### 2.5 Operations on Data Streams

Stream processing engines usually provide a set of built-in operations to ingest, transform, and output streams. These operators can be combined into dataflow processing graphs to implement the logic of streaming applications.

**Operations can be either stateless or stateful.** Stateless operations do not maintain any internal state. That is, the processing of an event does not depend on any events seen in the past and no history is kept. Stateless operations are easy to parallelize, since events can be processed independently of each other and of their arriving order. Moreover, in the case of a failure, a stateless operator can be simply restarted and continue processing from where it left off. In contrast, stateful operators may maintain information about the events they have received before
