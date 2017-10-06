/**
  * Created by andy on 29/09/2017.
  */
object RaceConditionExample {
  private var count: Int = 0

  def ++() : Int = /*this.synchronized*/ {
    count = count + 1
    count
  }

  def ++(currentCount: Int): Int = {
    currentCount + 1
  }

  def +:(value: Int): Unit = /*this.synchronized*/ {
    count = count + value
  }

  def main(args: Array[String]): Unit = {
    def asyncIncrement(id: String, times: Int): Thread = {
      def increment(id: String, times: Int, currentValue: Int =0): Int = {
        if (times == 0) {
          currentValue
        } else increment(id, times -1, {
          val cur = ++(currentValue)

          println(s"$id thread: $cur")
          Thread.sleep(500)
          cur
        })
      }

      val thread = new Thread {
        override def run(): Unit = {
          // ==Side Effect==
          for (i <- 1 to times) {
            println(s"$id thread: ${++} ")
            Thread.sleep(500)
          }

          // ==Tail Recursion Example==
          /*val result = increment(id, times)
          +:(result)*/

          // ==High order function Example==
          /*val result = (1 to times).foldLeft(0)((A,B) => { val cur = A + 1; println(s"$id thread: $cur"); Thread.sleep(500); cur })
          add(result)*/
        }
      }

      thread.start()
      thread
    }

    val aIncrementer = asyncIncrement("A", 5)
    val bIncrementer = asyncIncrement("B", 5)

    aIncrementer.join()
    bIncrementer.join()

    println(s"\nTotal Count: $count")
  }
}
