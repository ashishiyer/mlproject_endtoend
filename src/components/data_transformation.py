import pandas as pd
from dataclasses import dataclass
import numpy as np
import sys
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import os
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str = os.path.join('artifacts',"preprocessor.pkl")



class DataTransformation:
    def __init__(self):
        self.data_trasformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        try : 
            numerical_features = ["writing_score","reading_score"]
            categorical_features = ["gender",
                                    "race_ethnicity",
                                    "parental_level_of_education",
                                    "lunch",
                                    "test_preparation_course"
                                    ] 
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ])
            
            logging.info("Numerical encoding completed")
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder())
                ]
            )
            logging.info("Categorical encoding completed")
            
            logging.info(f"Numerical features : {numerical_features}")
            logging.info(f"Categorical features : {categorical_features}")

            preprocessor = ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_features),
                ("cat_pipeline",cat_pipeline,categorical_features)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try : 
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Datasets loaded")

            preprocessing_object = self.get_data_transformer_object()
            target_column_name = "math_score"
            numerical_features = ["writing_score","reading_score"]
            categorical_features = ["gender",
                                    "race_ethnicity",
                                    "parental_level_of_education",
                                    "lunch",
                                    "test_preparation_course"
                                    ] 
            
            input_train_feature_df = train_df.drop(columns=[target_column_name],axis=1)
            target_train_feature_df = train_df[target_column_name]

            input_test_feature_df = test_df.drop(columns=[target_column_name],axis=1)
            target_test_feature_df = test_df[target_column_name]

            input_feature_train_array = preprocessing_object.fit_transform(input_train_feature_df)
            input_feature_test_array = preprocessing_object.transform(input_test_feature_df)

            train_arr = np.c_[input_feature_train_array,target_train_feature_df]
            test_arr = np.c_[input_feature_test_array,target_test_feature_df]

            """Save preprocessor"""
            save_object(self.data_trasformation_config.preprocessor_obj_file_path,
                        preprocessing_object)


            return (train_arr,
                    test_arr,
                    self.data_trasformation_config.preprocessor_obj_file_path)


        except Exception as e:
            raise CustomException(e,sys)

