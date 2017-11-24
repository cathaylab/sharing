package demo

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}
import quickexample.StreamingExamples

/**
  * Created by Tse-En on 2017/11/20.
  */
object WindowWordCount extends App {

  StreamingExamples.disableLog()

  val sparkConf = new SparkConf().setMaster("local[*]").setAppName("HotWords")
  val ssc = new StreamingContext(sparkConf, Seconds(1))

  val lines = ssc.socketTextStream("localhost", 9999)
  val words = lines.flatMap(_.split(" "))
  val pairs = words.map(word => (word, 1))

  val windowDStream = pairs.reduceByKeyAndWindow((v1: Int, v2: Int) => v1 + v2, Seconds(10), Seconds(2))

  windowDStream.print()
  ssc.start()
  ssc.awaitTermination()

}
