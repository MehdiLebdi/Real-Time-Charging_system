from org.sfu.billing.utils.configurations import SparkConfig
from org.sfu.billing.utils.dataLayer import  dataLoader
from org.sfu.billing.devices.cdr import CallDetailRecord

from pyspark.sql import functions
from pyspark.sql.functions import split

class Controller:
    """
    Controller class is used to control lifecycle of entire application. It invokes all modules in logical sequence.
    Execution pipeline is Mediation module, Rating Module and Persistent module        
    """

    spark_config = SparkConfig()

    #This method will start streaming of events based on registered topic in kafka
    def stream_rawCdr(self):
        events = self.spark_config.get_events()
        return events

    # This method will determine device type and return its object
    # Default or implemented case as of now is of call detail record
    # There can be other iot devices as well which can be rated
    def device_type(self,events):
        return CallDetailRecord()

    #def process_row(self,row):
    #     # Write row to storage
    #      print("cdr: ", row)
    #      pass
    
    # Main method which includes logic of Lifecycle of application
    # 1.Starts Streaming process
    # 2.Detect type of device
    # 3.Map raw events into structured dataframe
    # 4.Invoke Mediation process
    # 5.Invoke Rating process
    # 6.Check data in hdfs 
    # 7.Persist data on configured database

    def process(self):
        events = self.stream_rawCdr()
        cdr = self.device_type(events)
        mapped_df = cdr.map(events)
        dl = dataLoader()
        normalized_frame = cdr.invoke_mediation(mapped_df)
        rated_frame = cdr.invoke_rating(normalized_frame)
        stream = rated_frame.writeStream.foreachBatch(dl.save_batch).start()
        #stream = normalized_frame.writeStream.foreachBatch(configurations.save_batch).start()
        #stream = normalized_frame.writeStream.outputMode("append").format("console").start()
        self.spark_config.stopStreaming(stream)
        pass    
    
