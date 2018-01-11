package demo

import org.apache.spark.streaming._
import org.apache.spark.SparkConf
import quickexample.StreamingExamples

/**
  * Created by Tse-En on 2017/11/20.
  */
object StatefulNetworkWordCount extends App {

  StreamingExamples.disableLog()

  val sparkConf = new SparkConf().setMaster("local[*]").setAppName("StatefulNetworkWordCount")
  // Create the context with a 1 second batch size
  val ssc = new StreamingContext(sparkConf, Seconds(5))
  ssc.checkpoint("persistent")

  def updateFunction(newValues: Seq[Int], currentState: Option[Int]): Option[Int] = {
    val newCount = currentState.getOrElse(0) + newValues.sum
    Some(newCount)
  }

  val lines = ssc.socketTextStream("localhost", 9999)
  val words = lines.flatMap(_.split(" "))
  val pairs = words.map(word => (word, 1))

  // Update state using `updateStateByKey`
  val stateDstream = pairs.updateStateByKey[Int](updateFunction _)

  stateDstream.print()
  ssc.start()
  ssc.awaitTermination()
}
