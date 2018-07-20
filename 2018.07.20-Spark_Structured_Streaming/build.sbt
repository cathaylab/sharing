name := "StructureStreaming"

version := "0.1"

scalaVersion := "2.11.8"

libraryDependencies ++= Seq(
  "org.apache.spark" % "spark-core_2.11" % "2.2.0",
  "org.apache.spark" % "spark-sql_2.11" % "2.2.0",
  "org.apache.spark" % "spark-streaming_2.11" % "2.2.0",
  "org.apache.spark" % "spark-yarn_2.11" % "2.2.0",
  "org.apache.spark" % "spark-hive_2.11" % "2.2.0",
  "org.apache.spark" % "spark-sql-kafka-0-10_2.11" % "2.2.0",
  "org.apache.spark" % "spark-mllib_2.11" % "2.2.0",
  "com.github.hirofumi" %% "xgboost4j-spark" % "0.7.1-p1"
)