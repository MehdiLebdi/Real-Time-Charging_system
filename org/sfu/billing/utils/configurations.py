from pyspark.sql import SparkSession
from org.sfu.billing.utils.propertiesReader import Properties

class SparkConfig:

    properties = Properties.load_properties()

    @staticmethod
    def get_spark():

        spark = SparkSession.builder.appName('Billing_Engine_Listener')\
                            .config("spark.jars.packages",SparkConfig.properties["SPARK"]["DEPENDENCIES"]) \
                            .config('spark.mongodb.input.uri', SparkConfig.properties["DATABASE"]["DB_INPUT_URI"]) \
                            .config('spark.mongodb.output.uri', SparkConfig.properties["DATABASE"]["DB_OUTPUT_URI"]) \
                            .getOrCreate()
        spark.sparkContext.setLogLevel('WARN')
        return spark

    @staticmethod
    def get_events():
        spark = SparkConfig.get_spark()
        bootstrap_servers = SparkConfig.properties["KAFKA"]["SERVER_IP"] + ':' + SparkConfig.properties["KAFKA"]["SERVER_PORT"]
        topics = SparkConfig.properties["KAFKA"]["TOPIC_NAMES"]
        #bootstrap_servers = "PLAINTEXT://" + bootstrap_servers
        print("bootstrap_servers: ", bootstrap_servers)
        #print("topic: ", topics)

        messages = spark.readStream.format('kafka') \
                        .option('kafka.bootstrap.servers', bootstrap_servers) \
                        .option('subscribe', topics) \
                        .load()

        return messages

    @staticmethod
    def stopStreaming(streamingQuery):
        streamingQuery.awaitTermination(SparkConfig.properties.getint("KAFKA","STREAMING_TTL"))
    


