name := "AkkaStreamExample"

version := "1.0"

scalaVersion := "2.11.12"

libraryDependencies ++= {
  val AkkaVersion = "2.4.16"
  val AkkaHttpVersion = "10.0.0"

  Seq(
    //"com.typesafe.akka" %% "akka-stream" % AkkaVersion,
    "com.typesafe.akka" %% "akka-http" % AkkaVersion,
    "com.typesafe.akka" %% "akka-http" % AkkaHttpVersion,
    "com.typesafe.akka" %% "akka-http-spray-json" % AkkaHttpVersion,
    "org.json4s" % "json4s-jackson_2.11" % "3.5.0",
    "org.scalatest" %% "scalatest" % "2.2.6" % "test",
    "com.typesafe.akka" %% "akka-testkit" % AkkaVersion,
    "com.typesafe" % "config" % "1.3.0",
    "ch.qos.logback" % "logback-classic" % "1.1.2"
  )
}