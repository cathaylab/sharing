name := "ReflectionExample"

version := "0.1"

scalaVersion := "2.12.5"

libraryDependencies ++= {
  Seq(
    "org.scalatest" %% "scalatest" % "3.0.1" % Test,
    "org.scala-lang" % "scala-compiler" % "2.12.5"
  )
}