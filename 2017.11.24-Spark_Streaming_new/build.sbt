name := "streaming-wordcount"

version := "1.0"

scalaVersion := "2.11.8"



// https://mvnrepository.com/artifact/org.apache.spark/spark-core_2.11
libraryDependencies += "org.apache.spark" % "spark-core_2.11" % "2.1.0"

// https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-10_2.11
libraryDependencies += "org.apache.spark" % "spark-streaming-kafka-0-10_2.11" % "2.1.0"

// https://mvnrepository.com/artifact/org.apache.spark/spark-streaming_2.11
libraryDependencies += "org.apache.spark" % "spark-streaming_2.11" % "2.1.0"

// https://mvnrepository.com/artifact/org.apache.spark/spark-sql_2.10
libraryDependencies += "org.apache.spark" % "spark-sql_2.11" % "2.1.0"

//resolvers += "Spark Packages Repo" at "https://dl.bintray.com/spark-packages/maven"
//libraryDependencies += "datastax" % "spark-cassandra-connector" % "2.0.1-s_2.11"

libraryDependencies += "com.datastax.spark" %% "spark-cassandra-connector" % "2.0.3"
