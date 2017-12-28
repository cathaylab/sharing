package demo.stock

import com.datastax.spark.connector.streaming._
import com.datastax.spark.connector.SomeColumns
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkConf
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, KafkaUtils, LocationStrategies}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import quickexample.StreamingExamples

/**
  * Created by Tse-En on 2017/11/23.
  */
object WindowingStock extends App {

  StreamingExamples.disableLog()
  //case class Order(time: Timestamp, orderId: Long, clientId: Long, symbol: String, amount: Int, price: Double, buy: String)

  val kafkaParams = Map[String, Object](
    "bootstrap.servers" -> "localhost:9092",
    "key.deserializer" -> classOf[StringDeserializer],
    "value.deserializer" -> classOf[StringDeserializer],
    "group.id" -> "stream",
    "auto.offset.reset" -> "latest",
    "enable.auto.commit" -> (true: java.lang.Boolean)
  )
  val Array(brokers, topics) = Array("localhost:9092","test")
  val topicsSet = topics.split(",").toSet

  val sparkConf = new SparkConf()
    .setMaster("local[*]")
    .setAppName("StatefulNetworkWordCount")
    .set("spark.cassandra.connection.host", "127.0.0.1")
  val ssc = new StreamingContext(sparkConf, Seconds(1))

  val messages = KafkaUtils.createDirectStream[String, String](
    ssc,
    LocationStrategies.PreferConsistent,
    ConsumerStrategies.Subscribe[String, String](topicsSet, kafkaParams))

  val lines = messages.map(_.value)
  val dstream = lines.map(x => parseStock(x))

  val pairs = dstream.transform { rdd =>
    rdd.filter(_._3 =="B").map(x => (x._1, x._2))
  }

  val windowStock = pairs.reduceByKeyAndWindow((v1: Int, v2: Int) => v1 + v2, Seconds(15), Seconds(5))
  val topStock = windowStock.map(x => x.swap).transform(rdd=>rdd.sortByKey(false)).map(x => x.swap)
  topStock.saveToCassandra("my_streaming", "topstock", SomeColumns("symbol", "count"))

  topStock.print()
  ssc.start()
  ssc.awaitTermination()

  def parseStock(str: String) = {
    val e = str.split(",")
    (e(3), e(4).toInt, e(6))
  }


}