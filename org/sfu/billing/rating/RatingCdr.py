import sys
from org.sfu.billing.utils.dataLayer import dataLoader
from org.sfu.billing.rating.Rating import Rating
from pyspark.sql import  functions as F


class RatingCdr(Rating):
    """
    CDR class for Rating
    """
    def __init__(self):
        """
        This class is a constructor for the
        :param Cdr: the
        """
        try:
            dl = dataLoader()
            self.__customers = dl.loadCustomers()
            self.__offers = dl.loadOffers()
            # to check the bahaviour  without streaming comment it out
            #self.__medi_df = dl.loadCDR()

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception("This is a Spark reading from MongoDb Exception ")



    def execute(self, med_df):
        """
        In this method all rates will be calculated
        :param med_df:
        :return: a dataframe of the customers including the rating as well
        """
        #to check the bahaviour  without streaming comment it out
        #med_df =self.__medi_df
        timeFormat = "%Y-%m-%d %H:%M:%S"
        timeDiff = (F.unix_timestamp('dateTimeDisconnect', format=timeFormat)- F.unix_timestamp('dateTimeConnect', format=timeFormat))
        med_df = med_df.withColumn("duration", timeDiff)

        med_df = med_df.join(self.__customers, med_df['callingPartyNumber'] == self.__customers['numbers'])
        med_df = med_df.drop(med_df['numbers'])
        #med_df['offerId'] == self.__offers['offerId']
        med_df = med_df.join(self.__offers, 'offerId')

        med_df = med_df.withColumn('bill', F.round(med_df['rate']*med_df['duration'],3))

        return med_df




"""
if __name__== "__main__":
    rcdr = RatingCdr()
    md = None
    md = rcdr.execute(md)
    print(md.show(10))
    print("hello")
    #print(rcdr.show(10))

"""