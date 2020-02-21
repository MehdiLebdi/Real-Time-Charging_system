from abc import ABC, abstractmethod


class Rating(ABC):
    """
    abstract class for rating
    """

    @abstractmethod
    def execute(self, med_df):
        print("RatingProc: Rating")
        pass


