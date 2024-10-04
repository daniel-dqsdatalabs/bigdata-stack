FROM spark:3.5.2-scala2.12-java17-python3-ubuntu

USER root

# Add Spark dependencies
ADD https://repo1.maven.org/maven2/org/postgresql/postgresql/42.6.0/postgresql-42.6.0.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/software/amazon/awssdk/s3/2.18.41/s3-2.18.41.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.2.0/delta-core_2.12-2.2.0.jar /opt/spark/jars
ADD https://repo1.maven.org/maven2/io/delta/delta-storage/2.2.0/delta-storage-2.2.0.jar /opt/spark/jars

COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf

RUN chown -R spark:spark /opt/spark/jars


