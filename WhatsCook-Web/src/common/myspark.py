from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession


class Myspark(object):
    LRMODEL_PATH = "src/common/MLmodels/lrModel"
    PIPLINEMODEL_PATH = "src/common/MLmodels/pplmodel"
    SPARK = None
    PPL = None
    LR = None

    @staticmethod
    def initialize():
        try:
            Myspark.SPARK = SparkSession.builder.appName("Recipe Recommender").getOrCreate()
            Myspark.PPL = PipelineModel.load(Myspark.PIPLINEMODEL_PATH)
            Myspark.LR = LogisticRegressionModel.load(Myspark.LRMODEL_PATH)
        except:
            print("Man! Having problem building spark session")
            import traceback
            traceback.print_exc()
            Myspark.SPARK = None

    @staticmethod
    def create_df_by_ingred(ingredients):
        return Myspark.SPARK.createDataFrame([(1, ingredients)], ['id', 'ingredients'])

    @staticmethod
    def stop():
        try:
            Myspark.SPARK.stop()
        except Exception as e:
            print(e)
            pass
