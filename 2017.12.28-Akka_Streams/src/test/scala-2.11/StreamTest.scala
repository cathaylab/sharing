import akka.NotUsed
import akka.actor.ActorSystem
import akka.stream.{ActorAttributes, ActorMaterializer, ClosedShape, ThrottleMode}
import akka.stream.scaladsl.{Broadcast, Flow, GraphDSL, Keep, Merge, RunnableGraph, Sink, Source}
import akka.util.ByteString
import org.scalatest.{BeforeAndAfterAll, FunSpec, Matchers}

import scala.concurrent.{Future, Promise}
import scala.util.{Failure, Success}

/**
  * Created by andy on 22/12/2017.
  */
class StreamTest extends FunSpec with Matchers with BeforeAndAfterAll {
  private def plusOneStage(): Flow[Int, Int, NotUsed] =
    Flow[Int].map { ele ⇒
      println(s"${Console.BLUE}$ele +1  on thread ${Thread.currentThread().getName}${Console.RESET}")
      Thread.sleep(100) // Simulate long processing

      ele + 1
    }

  private def multipleOneStage(): Flow[Int, Int, NotUsed] =
    Flow[Int].map { ele ⇒
      println(s"${Console.GREEN}$ele *1  on thread ${Thread.currentThread().getName}${Console.RESET}")
      Thread.sleep(100) // Simulate long processing

      ele * 1
    }

  override def beforeAll(): Unit = {}

  override def afterAll(): Unit = {}

  describe("Akka Streams") {
    ignore("Default behavior of Akka Streams put all computations in the same actor") {
      implicit val system = ActorSystem("QuickStart")
      implicit val materializer = ActorMaterializer()

      Source(List(1,10,100))
        .via(plusOneStage)
        .via(multipleOneStage)
        .runWith(Sink.foreach(s ⇒ println(s"Got output $s  on ${Thread.currentThread().getName}")))

      Thread.sleep(1000)
    }

    ignore("Stages demarcated by asynchronous boundaries might run concurrently with each other") {
      implicit val system = ActorSystem("QuickStart")
      implicit val materializer = ActorMaterializer()

      Source(List(1,10,100))
        .via(plusOneStage).async
        .via(multipleOneStage).async
        .runWith(Sink.foreach(s ⇒ println(s"Got output $s  on ${Thread.currentThread().getName}")))

      Thread.sleep(1000)
    }

    ignore("Asynchronously process based on mapAsync operator") {
      implicit val system = ActorSystem("QuickStart")
      implicit val materializer = ActorMaterializer()
      implicit val ec = system.dispatcher

      def plusOneStage(): Flow[Int, Int, NotUsed] =
        Flow[Int].mapAsync(2) { ele ⇒
          Future {
            println(s"${Console.BLUE}$ele +1  on thread ${Thread.currentThread().getName}${Console.RESET}")
            Thread.sleep(100) // Simulate long processing

            ele + 1
          }
        }

      def multipleOneStage(): Flow[Int, Int, NotUsed] =
        Flow[Int].mapAsync(2) { ele ⇒
          Future {
            println(s"${Console.GREEN} $ele *1  on thread ${Thread.currentThread().getName}${Console.RESET}")
            Thread.sleep(100) // Simulate long processing

            ele * 1
          }
        }

      Source(List(1,10,100))
        .via(plusOneStage)
        .via(multipleOneStage)
        .runWith(Sink.foreach(s ⇒ println(s"Got output $s  on ${Thread.currentThread().getName}")))

      Thread.sleep(1000)
    }

    ignore("Materialized value example") {
      implicit val system = ActorSystem("QuickStart")
      implicit val materializer = ActorMaterializer()
      implicit val ec = system.dispatcher

      val source:Source[Int, Promise[Option[Int]]] = Source.maybe[Int]
      val sink: Sink[String, Future[String]] = Sink.fold("get value: ")(_ + _)
      val graph: RunnableGraph[(Promise[Option[Int]],Future[String])] = source.map(_.toString).toMat(sink)(Keep.both)
      val result = graph.run()

      result._2.onSuccess[Unit]({ case result: String => println(result) })
      result._1.success(Some(2))
    }

    ignore("Graph Broadcast example") {
      val g = RunnableGraph.fromGraph(GraphDSL.create() { implicit b =>
        import GraphDSL.Implicits._

        val bcast = b.add(Broadcast[Int](2))

        Source(1 to 10) ~> bcast.in

        bcast.out(0) ~> Sink.foreach[Int](ele => println(s"${Console.GREEN} flow0: receive $ele on thread" +
          s" ${Thread.currentThread().getName}${Console.RESET}"))
        bcast.out(1) ~> Sink.foreach[Int](ele => println(s"${Console.BLUE} flow1: receive $ele on thread" +
          s" ${Thread.currentThread().getName}${Console.RESET}"))

        ClosedShape
      })

      implicit val system = ActorSystem("QuickStart")
      implicit val materializer = ActorMaterializer()

      g.run()
    }

    ignore ("Error recovering example") {
      import akka.stream.Supervision

      val source = Source(1 to 10).map(ele => {
        println(s"${Console.BLUE} send $ele on thread" + s" ${Thread.currentThread().getName}${Console.RESET}")
        ele
      })

      val errorHandling: Supervision.Decider = {
        case e: RuntimeException =>
          println(s"catch error: ${e.toString}")
          Supervision.resume
        case _ =>
          Supervision.stop
      }

      val MockToString: Flow[Int, String, NotUsed] = Flow[Int].map(ele => {
        if (ele % 6 == 0)
          throw new RuntimeException("Failed to generating element")
        else
          ele.toString
      }).withAttributes(ActorAttributes.supervisionStrategy(errorHandling))

      val g = RunnableGraph.fromGraph(GraphDSL.create() { implicit b =>
        import GraphDSL.Implicits._

        source ~> MockToString ~> Sink.foreach[String](ele => println(s"receive: $ele"))

        ClosedShape
      })

      implicit val system = ActorSystem("QuickStart")
      implicit val materializer = ActorMaterializer()

      g.run()
    }
  }
}
