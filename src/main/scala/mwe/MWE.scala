package mwe

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment

object MWE {
  def main(args: Array[String]): Unit = {
    val streamEnv: StreamExecutionEnvironment = StreamExecutionEnvironment.getExecutionEnvironment

    val intSource = streamEnv.fromElements(3, 5, 7, 11, 13, 17, 19)
    intSource.print()

    streamEnv.execute("mwe")
  }
}
