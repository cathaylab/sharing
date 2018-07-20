package com.cathay.ddt.lab

import java.sql.Timestamp
import org.apache.spark.sql.SparkSession

import org.apache.spark.sql.functions._

object StructuredNetworkWordCountWindowed extends App {

  val spark = SparkSession
    .builder
    .master("local")
    .appName("StructuredNetworkWordCountWindowed")
    .getOrCreate()

  import spark.implicits._

  // Create DataFrame representing the stream of input lines from connection to host:port
  val lines = spark.readStream
    .format("socket")
    .option("host", "192.168.1.249")
    .option("port", 9999)
    .option("includeTimestamp", true)
    .load()

  // Split the lines into words, retaining timestamps
  val words = lines.as[(String, Timestamp)].flatMap(line =>
    line._1.split(" ").map(word => (word, line._2))
  ).toDF("word", "timestamp")

  // Group the data by window and word and compute the count of each group
//  val windowedCounts = words.groupBy(
//    window($"timestamp", "9 seconds", "3 seconds"), $"word"
//  ).count().orderBy("window")


  val windowedCounts = words
    .withWatermark("timestamp", "10 seconds")
    .groupBy(
      window($"timestamp", "10 seconds", "5 seconds"),
      $"word")
    .count()

  // Start running the query that prints the windowed word counts to the console
  val query = windowedCounts.writeStream
    .outputMode("update")
    .format("console")
    .option("truncate", "false")
    .start()

  query.awaitTermination()



}
