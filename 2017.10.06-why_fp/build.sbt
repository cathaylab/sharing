name := "why_fp"

version := "1.0"

scalaVersion := "2.11.11"


libraryDependencies ++= {
  val AkkaHttpVersion   = "10.0.0"
  val AkkaVersion = "2.4.16"
  Seq(
    "com.typesafe.akka" %% "akka-actor" % AkkaVersion,
    "com.typesafe.akka" %% "akka-testkit" % AkkaVersion
  )
}