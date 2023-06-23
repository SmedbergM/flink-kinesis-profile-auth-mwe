ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.15"

lazy val root = (project in file("."))
  .settings(
    name := "flink-kinesis-profile-auth-mwe"
  )

val flinkDependencies = {
  val groupId = "org.apache.flink"
  val version = "1.15.2"
  Seq(
    groupId %% "flink-streaming-scala" % version,
    groupId % "flink-clients" % version
  )
}

libraryDependencies ++= flinkDependencies
