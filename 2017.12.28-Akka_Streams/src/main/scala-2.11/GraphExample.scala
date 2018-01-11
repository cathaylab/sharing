import akka.actor.ActorSystem
import com.freedomandy.data.Stock
import com.freedomandy.service.StockService
//import akka.actor.Status.Success
import akka.stream._
import akka.stream.scaladsl._
import org.slf4j.LoggerFactory

import scala.concurrent.duration._

/**
  * Created by andy on 17/12/2017.
  */
object GraphExample {
  private val log = LoggerFactory.getLogger(this.getClass)

  def main(args: Array[String]): Unit = {
    implicit val system = ActorSystem("QuickStart")
    implicit val materializer = ActorMaterializer()
    implicit val ec = system.dispatcher

    println("Start stock polling")

    val stocks =
      Source.tick(0.seconds, 2.minutes, ()).take(180).mapAsync[Option[Stock]](1)(_ => StockService().getStock("TPE","2330"))

    val g = RunnableGraph.fromGraph(GraphDSL.create() { implicit b =>
      import GraphDSL.Implicits._

      val bcast = b.add(Broadcast[Option[Stock]](3))

      stocks ~> bcast.in

      bcast.out(0) ~> Flow[Option[Stock]].filter(_.isDefined).map(ele => s"save to mongo: ${ele.get}") ~> Sink.foreach(println)

      bcast.out(1) ~> Flow[Option[Stock]].filter(_.isDefined).map(ele => s"publish to kafka: ${ele.get}") ~> Sink.foreach(println)

      bcast.out(2) ~> Flow[Option[Stock]].filter(_.isDefined).map(ele => s"publish to elastic search: ${ele.get}") ~> Sink.foreach(println)


      ClosedShape
    })

    g.run()
  }
}
