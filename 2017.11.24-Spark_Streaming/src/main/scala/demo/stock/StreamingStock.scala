package demo.stock

import java.sql.Timestamp
import java.text.SimpleDateFormat

import com.datastax.spark.connector.SomeColumns
import com.datastax.spark.connector.streaming._
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkConf
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, KafkaUtils, LocationStrategies}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import quickexample.StreamingExamples

/**
  * Created by Tse-En on 2017/11/23.
  */
object StreamingStock extends App {

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


  val ssc = new StreamingContext(sparkConf, Seconds(2))
  //val lines = ssc.socketTextStream("localhost", 9999)
  val messages = KafkaUtils.createDirectStream[String, String](
    ssc,
    LocationStrategies.PreferConsistent,
    ConsumerStrategies.Subscribe[String, String](topicsSet, kafkaParams))

  val lines = messages.map(_.value)
  val dstream = lines.map(x => parseStock(x))

  dstream.saveToCassandra("my_streaming", "stock", SomeColumns("time", "orderid", "clientid", "symbol", "amount", "price", "buy"))
  dstream.print()

  ssc.start()
  ssc.awaitTermination() // Wait for the computation to terminate

  def parseStock(str: String) = {
    val dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss")
    val e = str.split(",")
    (new Timestamp(dateFormat.parse(e(0)).getTime),
      e(1).toLong,
      e(2).toLong,
      e(3),
      e(4).toInt,
      e(5).toDouble,
      e(6))
  }

}
