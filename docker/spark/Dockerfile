FROM apache/spark:4.1.0-preview4-scala2.13-java17-python3-ubuntu

USER root

# Add Spark dependencies
ADD https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.8/postgresql-42.7.8.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/software/amazon/awssdk/s3/2.40.4/s3-2.40.4.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/io/delta/delta-spark_2.13/4.0.0/delta-spark_2.13-4.0.0.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/io/delta/delta-storage/4.0.0/delta-storage-4.0.0.jar /opt/spark/jars

COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf

RUN chown -R spark:spark /opt/spark/jars
