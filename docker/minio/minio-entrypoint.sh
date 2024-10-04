#/bin/bash  
    
sleep 5
/usr/bin/mc config host add local http://minio:9000 minio minio123
/usr/bin/mc mb local/warehouse
/usr/bin/mc mb local/warehouse/bronze
/usr/bin/mc mb local/warehouse/silver
/usr/bin/mc mb local/warehouse/gold
/usr/bin/mc mb local/flink
/usr/bin/mc mb local/flink/flink-savepoints
/usr/bin/mc mb local/flink/flink-checkpoints
exit 0