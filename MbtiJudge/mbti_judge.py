import mbti_call as mt
import tensorflow as tf
import numpy as np
import pandas as pd
from transformers import *
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import warnings
warnings.filterwarnings(action='ignore')

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
train = pd.read_csv('dataset/train_set.csv')
test = pd.read_csv('dataset/test_set.csv')

# train 데이터를 버트 인풋에 맞게 변환 -- 재 학습용 지금은 필요 X
train_x, train1_y, train2_y, train3_y , train4_y = mt.load_data(train)


#이부분 부터 뷰에서 필요 모델불러옴
mbti_model = mt.create_mbti_bert()
#가중치 조정
mbti_model.load_weights("newhuggingfacembti_bert.h5")


#테스트 셋 불러옴
test_set = mt.predict_load_data(test)

#결과값 가져옴 preds로 만듦
preds = mbti_model.predict(test_set,verbose=1)

#preds mbti 데이터 프레임화 시켜서 반환시켜줌
preds_total = mt.mbti_result(preds)

preds_total.to_csv('result.csv',index=False)