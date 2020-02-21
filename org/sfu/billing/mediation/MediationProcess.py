from abc import ABC, abstractmethod

class MediationProcess(ABC):
    """
    Abstract class for mediation layer.
    Enforces a structure, any subclass has to mandatorily provide method definitions
    """

    @abstractmethod
    def validate(self, mapped_frame):
        pass

    @abstractmethod
    def aggregate(self, validated_df):
        pass

    def execute(self,mapped_frame):
        self.validated_frame = self.validate(mapped_frame)
        self.flattened_cdrFrame = self.aggregate(self.validated_frame)
        return self.flattened_cdrFrame


    
