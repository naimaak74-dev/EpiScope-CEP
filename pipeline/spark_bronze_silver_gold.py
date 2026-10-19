"""Starter Spark pipeline. Verify column names and Spark/Java installation before running."""
import argparse
from pathlib import Path
from pyspark.sql import SparkSession, functions as F

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True); p.add_argument("--output",default="data/lakehouse")
    p.add_argument("--batch-id",default="manual-batch")
    a=p.parse_args()
    spark=(SparkSession.builder.appName("EpiScope-Bronze-Silver-Gold").getOrCreate())
    raw=spark.read.option("header",True).option("inferSchema",True).csv(a.input)
    bronze=raw.withColumn("_batch_id",F.lit(a.batch_id)).withColumn("_ingested_at",F.current_timestamp())
    bronze_path=f"{a.output}/bronze"
    bronze.write.mode("append").parquet(bronze_path)
    # Flexible starter: standardise common date/count names; actual encounter data may need aggregation first.
    cols={c.lower():c for c in bronze.columns}
    date_col=next((cols[x] for x in ["encounter_date","report_date","date","visit_date"] if x in cols),None)
    district_col=next((cols[x] for x in ["district","district_name","district_id"] if x in cols),None)
    disease_col=next((cols[x] for x in ["disease","disease_name","condition","diagnosis"] if x in cols),None)
    if date_col and district_col and disease_col:
        silver=(bronze.withColumn("date",F.to_date(F.col(date_col)))
                .withColumn("district",F.col(district_col).cast("string"))
                .withColumn("disease",F.col(disease_col).cast("string"))
                .filter(F.col("date").isNotNull() & F.col("district").isNotNull() & F.col("disease").isNotNull())
                .dropDuplicates())
        silver.write.mode("overwrite").partitionBy("date").parquet(f"{a.output}/silver")
        gold=(silver.groupBy("date","district","disease").agg(F.count("*").alias("case_count")))
        gold.write.mode("overwrite").partitionBy("date").parquet(f"{a.output}/gold")
        gold.write.mode("overwrite").option("header",True).csv(f"{a.output}/gold_csv")
        print("Pipeline completed. Review quarantine needs and idempotency before production use.")
    else:
        print("Bronze written, but expected date/district/disease columns were not found.")
        print("Available columns:", bronze.columns)
    spark.stop()
if __name__=="__main__": main()
