import akka.{Done, NotUsed}
import akka.actor.ActorSystem
import akka.stream.scaladsl.RunnableGraph
import akka.stream.{ActorMaterializer, ThrottleMode}
import akka.stream.scaladsl.{Flow, Keep, Sink, Source}

import scala.concurrent.duration._
import scala.concurrent.Future

/**
  * Created by andy on 20/12/2017.
  */
object BackPressureExampe {
  def main(args: Array[String]): Unit = {
    implicit val system = ActorSystem("QuickStart")
    implicit val materializer = ActorMaterializer()

    val source: Source[Int, NotUsed] = Source(1 to 10)
    val slowSource: Source[Int, NotUsed] = source.throttle(1, 1.second, 1, ThrottleMode.shaping)
    val sink: Sink[Int, Future[Done]] = Sink.foreach[Int](ele => println(s"receive: $ele on ${Thread.currentThread().getName}"))
    val slowSink: Sink[Int, Future[Done]] = Flow[Int].throttle(1, 1.second, 1, ThrottleMode.shaping).toMat(sink)(Keep.right)

    def getFlow(source: Source[Int, NotUsed], sink: Sink[Int, Future[Done]]): RunnableGraph[Future[Done]] = {
      source.map(ele => { print(s"send on ${Thread.currentThread().getName}...   "); ele}).toMat(sink)(Keep.right)
    }

    implicit val ec = system.dispatcher
    //getFlow(source, sink).run.onComplete(_ => println("Quick Source & Quick Sink Finish"))
    //getFlow(slowSource, sink).run.onComplete(_ => println("Slow Source & Quick Sink Finish"))
    getFlow(source, slowSink).run.onComplete(_ => println("Quick Source & Slow Sink Finish"))
    //getFlow(slowSource, slowSink).run.onComplete(_ => { println("Slow Source & Slow Sink Finish"); system.terminate() })

  }

}
