package mwe

import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.kinesis.shaded.org.apache.flink.connector.aws.config.AWSConfigConstants
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment
import org.apache.flink.streaming.connectors.kinesis.FlinkKinesisConsumer
import org.apache.flink.streaming.connectors.kinesis.config.ConsumerConfigConstants

import java.util.Properties

object MWE {
  def main(args: Array[String]): Unit = {

    val consumerProps = new Properties
    val region = sys.env("AWS_REGION")
    consumerProps.setProperty(AWSConfigConstants.AWS_REGION, region)

    val streamName = sys.env("KINESIS_STREAM_NAME")
    val profileName = sys.env("AWS_PROFILE_NAME")
    consumerProps.setProperty(AWSConfigConstants.AWS_CREDENTIALS_PROVIDER, "PROFILE")
    consumerProps.setProperty(AWSConfigConstants.AWS_PROFILE_NAME, profileName)

    consumerProps.setProperty(ConsumerConfigConstants.STREAM_INITIAL_POSITION, "LATEST")

    val stringSchema = new SimpleStringSchema
    val flinkConsumer = new FlinkKinesisConsumer[String](streamName, stringSchema, consumerProps)

    val streamEnv: StreamExecutionEnvironment = StreamExecutionEnvironment.getExecutionEnvironment
    streamEnv.addSource(flinkConsumer).print()

    streamEnv.execute("mwe")
  }
}
