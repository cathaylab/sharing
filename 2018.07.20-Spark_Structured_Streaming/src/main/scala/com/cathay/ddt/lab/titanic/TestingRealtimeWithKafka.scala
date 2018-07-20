package com.cathay.ddt.lab.titanic

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types.{DoubleType, StringType, StructField, StructType}

object TestingRealtimeWithKafka extends App {

  // the directory where we store the testing csv file
  val fileDir = "data/titanic/test"
  val checkpoint_location = "kafkacheckpoint"

  Logger.getLogger("org").setLevel(Level.OFF)
  Logger.getLogger("com").setLevel(Level.OFF)
  Logger.getRootLogger.setLevel(Level.OFF)

  // define the spark session
  val spark: SparkSession = SparkSession.builder()
    .appName("Spark Structured Streaming XGBOOST")
    .master("local[*]")
    .getOrCreate()

  // define the schema of the csv file
  val schema = StructType(
    Array(StructField("PassengerId", DoubleType),
      StructField("Pclass", DoubleType),
      StructField("Name", StringType),
      StructField("Sex", StringType),
      StructField("Age", DoubleType),
      StructField("SibSp", DoubleType),
      StructField("Parch", DoubleType),
      StructField("Ticket", StringType),
      StructField("Fare", DoubleType),
      StructField("Cabin", StringType),
      StructField("Embarked", StringType)
    ))

  case class Passenger(PassengerId: Double, Pclass: Double, Name: String, Sex: String, Age: Double, SibSp: Double, Parch: Double, Ticket: String, Fare: Double, Cabin: String, Embarked: String)
  object Passenger {
    def apply(rawStr: String): Passenger = {
      val startIndex = rawStr.indexOf("\"")
      val lastIndex = rawStr.lastIndexOf("\"")
      val part1 = rawStr.substring(0,startIndex).split(",")
      val part2 = rawStr.substring(lastIndex+1).split(",")
      Passenger(
        part1(0).toDouble,
        part1(1).toDouble,
        rawStr.substring(startIndex+1, lastIndex),
        part2(1),
        if(part2(2).isEmpty) 0 else part2(2).toDouble,
        if(part2(3).isEmpty) 0 else part2(3).toDouble,
        if(part2(4).isEmpty) 0 else part2(4).toDouble,
        part2(5),
        if(part2(6).isEmpty) 0 else part2(6).toDouble,
        part2(7),
        part2(8))
    }
  }

  // read the csv test data in a realtime df from kafka testing topic
  val df = spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("startingOffsets", "latest")
    .option("subscribe", "testing")
    .load()

  import spark.implicits._
  val kafkadf = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    .as[(String, String)].toDF("key", "value").map(r ⇒ Passenger(r.getString(1)))

  // start writing the data in our custom sink
  kafkadf.writeStream
    .format("com.cathay.ddt.lab.titanic.XGBoostMLSinkProvider")
    .queryName("XGBoostQuery")
    .trigger(Trigger.ProcessingTime("3 seconds"))
    .option("truncate", false)
    .option("checkpointLocation", checkpoint_location)
    .start()

  // wait for query to terminate
  spark.streams.awaitAnyTermination()

}
