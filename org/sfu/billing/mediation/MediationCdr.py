from org.sfu.billing.mediation.MediationProcess import MediationProcess

class MediationCdr(MediationProcess):
    """Implementation class for MediationProcess for cdr"""

    # This method will hold all validations to be done on cdr, 1 validation implemented is to filter out call drops
    # Input: Mapped dataframe with proper structure and datatypes
    # Output: Validated frames with all irrelevent records filtered out
    def validate(self, mapped_frame):
        validated_df = mapped_frame.filter(mapped_frame['callStatus']==0)
        return validated_df
    
    # Method for flattening cdr data, already recieving flattened data from simulator, if not implementation needs to be provided.
    # Input: Validated frame 
    # Output: Flattened frame
    def aggregate(self, validated_df):
        return validated_df




