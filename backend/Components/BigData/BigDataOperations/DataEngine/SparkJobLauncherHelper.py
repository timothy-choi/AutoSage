from pyspark.sql import SparkSession

def create_spark_session(app_name="SparkApp", master="local[*]"):
    return SparkSession.builder.appName(app_name).master(master).getOrCreate()

def run_spark_job(job_func, *args, app_name="SparkApp", master="local[*]", **kwargs):
    spark = create_spark_session(app_name=app_name, master=master)
    try:
        return job_func(spark, *args, **kwargs)
    except Exception as e:
        print(f"[SparkJobLauncher] Error running job: {e}")
        raise
    finally:
        spark.stop()

def read_csv(spark, path, **options):
    return spark.read.options(**options).csv(path)

def write_parquet(df, path, **options):
    df.write.options(**options).parquet(path)