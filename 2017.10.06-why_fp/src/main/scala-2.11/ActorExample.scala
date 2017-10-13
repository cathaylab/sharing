import akka.actor.{Actor, ActorRef, ActorSystem, Props}

/**
  * Created by andy on 04/10/2017.
  */
object ActorExample {
  def main(args: Array[String]): Unit = {
    val system = ActorSystem("counter-system")
    val countActor = system.actorOf(Props[CounterActor])
    val displayActor = system.actorOf(Props[DisplayActor])
    val thread1 = new Thread {
      override def run(): Unit = {
        for (i <- 1 to 5) countActor ! AddCountRequest(1, displayActor, "thread1")
      }
    }
    val thread2 = new Thread {
      override def run(): Unit = {
        for (i <- 1 to 5) countActor ! AddCountRequest(1, displayActor, "thread2")
      }
    }

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    system.terminate()
  }
}

class CounterActor extends Actor {
  var counter: Int = 0

  def receive = {
    case AddCountRequest(value, outputActor, threadId) =>
      counter += value
      outputActor ! DisplayRequest(s"The current counter value: $counter, updated by $threadId")
  }
}

class DisplayActor extends Actor {
  def receive = {
    case DisplayRequest(context: String) =>
      println(context)
  }
}

case class AddCountRequest(value: Int, outputActor: ActorRef, threadId: String)
case class DisplayRequest(value: String)
