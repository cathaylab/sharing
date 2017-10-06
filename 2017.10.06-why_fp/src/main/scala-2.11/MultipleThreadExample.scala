/**
  * Created by andy on 01/10/2017.
  */
object MultipleThreadExample {
  def main(args: Array[String]): Unit ={
    val thread1 = new HelloWord()
    val thread2 = new HelloWord()

    thread1.start()
    thread2.start()
  }
}

class HelloWord extends Thread {
  override def run(): Unit = {
    println("Hello ")
    println("World ")
  }
}