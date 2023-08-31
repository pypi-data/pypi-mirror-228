import time

from citybrain_platform import JobStatus
import citybrain_platform
from citybrain_platform import Column, ColumnType


citybrain_platform.api_key = "MTAwMDEkMTY5MjE1NTM0NyQxMDAwMQ"
citybrain_platform.api_baseurl = "http://localhost:8080/platform/"

columns = [
    Column("col_str", ColumnType.STRING, "aa"),
    Column("col_id", ColumnType.TIMESTAMP),
]

partition_columns = [
    Column("col_pt", ColumnType.INT, "ppt")
]

# create table
# ok = citybrain_platform.Computing.create_table(name="mbt_test6", columns=columns, partition_columns=partition_columns, description="ssdad")
# print(ok)

# get table schema
# schema = citybrain_platform.Computing.get_table_schema(name="mbt_test4")
# print(schema)

# upload data to table
# result = citybrain_platform.Computing.upload_table_data(name="mbt_test2", append=True, csv_filepath="aa.csv", partition_key={"col_pt": "19"})
# print(result)

# truncate table
# result = citybrain_platform.Computing.truncate_table(name="mbt_test1", partition_key={"col_pt": "1"})
# print(result)

# drop table
# result = citybrain_platform.Computing.drop_table(name="mbt_test2")
# print(result)

# public table
# public_table_name = citybrain_platform.Computing.public_table(name="mbt_test1")
# print(public_table_name)

# get available table list
# result = citybrain_platform.Computing.list_tables()
# print(result)

# create sql job
# job_id = citybrain_platform.Computing.create_job(
#     sql="select avg(osmid) from osm_node where osmid between 80080000 and 90080000;",
#     worker_limit=10,
#     split_size=256
# )
# print(jobID)

# stop running job
# result = citybrain_platform.Computing.stop_job(job_id="fab7b329-aef9-4c96-a9ac-1b47b1468e79")
# print(result)

# get job status
job_status = citybrain_platform.Computing.get_job_status(job_id="dd124677-a95e-4b40-a339-806af93c4be1")
print(job_status)


# job_id = citybrain_platform.Computing.create_job(sql="SELECT * FROM mbt_test2")
# print(job_id)

# get job results
# citybrain_platform.Computing.get_job_results(job_id="dd124677-a95e-4b40-a339-806af93c4be1", filepath="a.csv")


# sqlresult = "select * from cesm_ass1_50year_0730 limit 1000"
# jobresult_id = citybrain_platform.Computing.create_job(sql=sqlresult)

# while True:
#     status = citybrain_platform.Computing.get_job_status(job_id=jobresult_id)
#     print(status.status)
#     if status.status == JobStatus.RUNNING:
#         print(status.progress)
#     if status.status == JobStatus.TERMINATED:
#         break
#     time.sleep(1)

# print("downloading result")
# citybrain_platform.Computing.get_job_results(job_id=jobresult_id, filepath="cesm_ass1_50year_0730.csv")
