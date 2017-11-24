package quickexample

import com.datastax.spark.connector.streaming._
import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by Tse-En on 2017/11/22.
  */
object WordcountCassandra extends App {

  StreamingExamples.disableLog()

  val sparkConf = new SparkConf()
    .setMaster("local[*]")
    .setAppName("StatefulNetworkWordCount")
    .set("spark.cassandra.connection.host", "127.0.0.1")

  val ssc = new StreamingContext(sparkConf, Seconds(1))
  val lines = ssc.socketTextStream("localhost", 9999)

  val words = lines.flatMap(_.split(" "))
  val pairs = words.map(word => (word, 1))
  val wordCounts = pairs.reduceByKey(_ + _).map(x => x.swap).transform(rdd=>rdd.sortByKey(false))

  wordCounts.print()
  wordCounts.saveToCassandra("my_streaming", "words")

  ssc.start()
  ssc.awaitTermination() // Wait for the computation to terminate

}
