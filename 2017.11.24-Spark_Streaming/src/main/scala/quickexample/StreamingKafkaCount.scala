package quickexample

import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkConf
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka010._


/**
  * Created by Tse-En on 2017/10/6.
  */
object StreamingKafkaCount extends App {

  val kafkaParams = Map[String, Object](
    "bootstrap.servers" -> "localhost:9092",
    "key.deserializer" -> classOf[StringDeserializer],
    "value.deserializer" -> classOf[StringDeserializer],
    "group.id" -> "stream",
    "auto.offset.reset" -> "latest",
    "enable.auto.commit" -> (true: java.lang.Boolean)
  )

  val Array(brokers, topics) = Array("localhost:9092","test")

  // Create context with 2 second batch interval
  val sparkConf = new SparkConf().setMaster("local[*]").setAppName("stockStreaming")
  val ssc = new StreamingContext(sparkConf, Seconds(2))
  ssc.checkpoint("stock")

  // Create direct kafka stream with brokers and topics
  val topicsSet = topics.split(",").toSet
//  val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
  val messages = KafkaUtils.createDirectStream[String, String](
    ssc,
    LocationStrategies.PreferConsistent,
    ConsumerStrategies.Subscribe[String, String](topicsSet, kafkaParams))

  // Get the lines, split them into words, count the words and print
  val lines = messages.map(_.value)
  val words = lines.flatMap(_.split(" "))
  val wordCounts = words.map(x => (x, 1L)).reduceByKey(_ + _)//.reduceByKeyAndWindow(_+_, _-_, Minutes(10), Seconds(2), 2)
  wordCounts.print()

  // Start the computation
  ssc.start()
  ssc.awaitTermination()

}
