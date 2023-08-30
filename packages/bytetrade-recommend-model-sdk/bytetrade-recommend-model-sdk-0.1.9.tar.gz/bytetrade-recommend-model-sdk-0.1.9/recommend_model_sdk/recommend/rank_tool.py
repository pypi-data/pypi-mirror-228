from recommend_model_sdk.tools.common_tool import CommonTool
from imblearn.over_sampling import RandomOverSampler
import numpy as np
import random
from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost import XGBClassifier

class CTRRankTool:
    """_summary_
    Click Through Rate
    """
    def __init__(self) -> None:
        self.__ros = RandomOverSampler(random_state=0)
        self.__common_tool = CommonTool()
        self.__logger = self.__common_tool.get_logger()


    
    def batch_next(self,iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]
            
    def validate_entry_id_set(self,entry_id_set):
        if isinstance(entry_id_set,set) is False:
            raise ValueError("entry_id_set is not set")
        for current_entry_id in  entry_id_set:
            if isinstance(current_entry_id,int) is False:
                raise ValueError("current_entry_id is not int")
    
    def configure_positive_and_negative_sample_ratio(self, positive_entry_id_set,negative_entry_id_set,embedding_dim):
        """_summary_
        Args:
            positive_entry_id_set (_type_): _description_
            negative_entry_id_set (_type_): _description_
            embedding_dim (_type_): _description_
        """
        if isinstance(embedding_dim,int) is False:
            raise ValueError("embedding_dim is not int")
        if embedding_dim < 1:
            raise ValueError("embedding_dim is small than 1")
        majority_number = max(len(positive_entry_id_set),len(negative_entry_id_set))
        
        if 2 * ( majority_number * 0.9 ) < embedding_dim * 30:
            self.__logger.debug(f'2 * ( majority_number * 0.9 ) < embedding_dim * 30')
            return 
        if len(positive_entry_id_set) < 100:
            self.__logger.debug(f'positive_entry_id_set length small than {len(positive_entry_id_set)}')
            return 
        positive_train_x,positive_test_x,positive_train_y,positive_test_y = train_test_split(list(positive_entry_id_set),[1]*len(positive_entry_id_set),test_size=0.1)
        negative_train_x, negative_test_x,negative_train_y,negative_test_y = train_test_split(list(negative_entry_id_set),[0]*len(negative_entry_id_set),test_size=0.1)
        
        train_x = positive_train_x.extend(negative_train_x)
        train_y = positive_train_y.extend(negative_train_y)
        
        test_x = positive_test_x.extend(negative_test_x)
        test_y = positive_test_y.extend(negative_test_y)
        # process 
        resampled_x, resampled_y = self.__ros.fit_resample(train_x, train_y)
        train_tuple = list(zip(resampled_x,resampled_y))
        test_tuple = list(zip(test_x,test_y))
        return train_tuple,test_tuple
        
            
    
    def train(self,positive_entry_id_set,negative_entry_id_set,embedding_dimension,method_according_entry_id_and_label_to_get_embedding):
        """_summary_
        def method_according_entry_id_and_label_to_get_embedding(entry_id_and_label_tuple_list):
            return train_x_embedding, train_y_embedding
        Args:
            positive_entry_id_set (_type_): _description_
            negative_entry_id_set (_type_): _description_
            embedding_dimension (_type_): _description_
            method_according_entry_id_set_to_get_embedding (_type_): _description_

        Raises:
            ValueError: _description_
        """
        self.validate_entry_id_set(positive_entry_id_set)
        self.validate_entry_id_set(negative_entry_id_set)
        if len(negative_entry_id_set) != len(positive_entry_id_set):
            raise  ValueError("negative_entry_id_set not equal positive_entry_id_set")
        entry_id_list = list(positive_entry_id_set.union(negative_entry_id_set))
        entry_id_to_click_label = dict()
        for current_positive_entry_id in positive_entry_id_set:
            entry_id_to_click_label[current_positive_entry_id] = 1
        for current_negative_entry_id in negative_entry_id_set:
            entry_id_to_click_label[current_negative_entry_id] = 0
        iterations = 1
        sklearn_model = xgb.XGBClassifier(max_depth=5,learning_rate= 0.5, verbosity=1, objective='binary:logistic',random_state=1)
        train_tuple_list,test_tuple_list = self.configure_positive_and_negative_sample_ratio(positive_entry_id_set,negative_entry_id_set,embedding_dimension)
        random.shuffle(train_tuple_list)
        random.shuffle(test_tuple_list)
        # 
        for current_batch_entry_id_and_label_tuple_list in self.batch_next(train_tuple_list,100):
            current_train_x_batch_embeddding,current_train_y_batch_label = method_according_entry_id_and_label_to_get_embedding(current_batch_entry_id_and_label_tuple_list)
            if isinstance(current_train_x_batch_embeddding,np.ndarray) is False:
                raise ValueError("x_batch_embedding is not numpy ndarray")
            if isinstance(current_train_y_batch_label,np.ndarray) is False:
                raise ValueError("y_batch_label is not numpy ndarray")
            if current_train_x_batch_embeddding.shape[0] != current_train_y_batch_label.shape[0]:
                raise ValueError("entrx_batch_embeddding number of items not equal y_batch_label")
            if len(test_tuple_list) > 100:
                temp_test_tuple_list = random.sample(test_tuple_list,100)
            else:
                temp_test_tuple_list = test_tuple_list
            
            if (iterations == 1):
                current_test_x_batch_embedding,current_test_y_batch_label = method_according_entry_id_and_label_to_get_embedding(temp_test_tuple_list)
                sklearn_model = sklearn_model.fit(current_train_x_batch_embeddding, current_train_y_batch_label, eval_set=[(current_test_x_batch_embedding, current_test_y_batch_label)],
                        verbose=False, eval_metric = ['logloss'],
                        early_stopping_rounds = 1, 
                        xgb_model = sklearn_model
                        )
            else:
                sklearn_model = sklearn_model.fit(current_train_x_batch_embeddding, current_train_y_batch_label, eval_set=[(current_test_x_batch_embedding, current_test_y_batch_label)],
                        verbose=False, eval_metric = ['logloss'],
                        early_stopping_rounds = 1, 
                        )
        
        # upload model to s3