import tensorflow as tf
import numpy as np
import pandas as pd
from transformers import *
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
import os


tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
# train = pd.read_csv('dataset/train_set.csv')
# test = pd.read_csv('dataset/test_set.csv')

# 트레인데이터 컨버트용
def convert_data(data_df):
    global tokenizer
    
    SEQ_LEN = 128
    BATCH_SIZE = 20
    # 판단할 문장을 포함하고 있는 칼럼
    DATA_COLUMN = "feature_total"
    # mbti를 (각각 레이블 1 -> i_e , 2 -> n_s , 3-> f_t , 4-> j_p를 의미) 포함하고 있는 칼럼
    LABEL_COLUMN1 = "mbti_i_e"
    LABEL_COLUMN2 = "mbti_n_s"
    LABEL_COLUMN3 = "mbti_f_t"
    LABEL_COLUMN4 = "mbti_j_p"

    tokens, masks, segments, targets1 , targets2, targets3, targets4 = [], [], [], [], [], [], []
    
    for i in tqdm(range(len(data_df))):
        # token : 문장을 토큰화함
        token = tokenizer.encode(data_df[DATA_COLUMN][i], max_length=SEQ_LEN, truncation=True, padding='max_length')
       
        # 마스크는 토큰화한 문장에서 패딩이 아닌 부분은 1, 패딩인 부분은 0으로 통일
        num_zeros = token.count(0)
        mask = [1]*(SEQ_LEN-num_zeros) + [0]*num_zeros
        
        # 문장의 전후관계를 구분해주는 세그먼트는 문장이 1개밖에 없으므로 모두 0
        segment = [0]*SEQ_LEN

        # 버트 인풋으로 들어가는 token, mask, segment를 tokens, segments에 각각 저장
        tokens.append(token)
        masks.append(mask)
        segments.append(segment)
        
        # 정답(각각 레이블 1 -> i_e , 2 -> n_s , 3-> f_t , 4-> j_p를 의미)을 targets 변수에 저장해 줌
        targets1.append(data_df[LABEL_COLUMN1][i])
        targets2.append(data_df[LABEL_COLUMN2][i])
        targets3.append(data_df[LABEL_COLUMN3][i])
        targets4.append(data_df[LABEL_COLUMN4][i])

    # tokens, masks, segments, 정답 변수 targets를 numpy array로 지정    
    tokens = np.array(tokens)
    masks = np.array(masks)
    segments = np.array(segments)
    targets1 = np.array(targets1)
    targets2 = np.array(targets2)
    targets3 = np.array(targets3)
    targets4 = np.array(targets4)

    return [tokens, masks, segments], targets1 , targets2 , targets3 , targets4

#트레인 데이터 토큰화,마스킹,세그먼트화 + 타겟조정
def load_data(pandas_dataframe):
    # 판단할 문장을 포함하고 있는 칼럼
    DATA_COLUMN = "feature_total"
    # mbti를 (각각 레이블 1 -> i_e , 2 -> n_s , 3-> f_t , 4-> j_p를 의미) 포함하고 있는 칼럼
    LABEL_COLUMN1 = "mbti_i_e"
    LABEL_COLUMN2 = "mbti_n_s"
    LABEL_COLUMN3 = "mbti_f_t"
    LABEL_COLUMN4 = "mbti_j_p"

    data_df = pandas_dataframe
    data_df[DATA_COLUMN] = data_df[DATA_COLUMN].astype(str)
    data_df[LABEL_COLUMN1] = data_df[LABEL_COLUMN1].astype(int)
    data_df[LABEL_COLUMN2] = data_df[LABEL_COLUMN2].astype(int)
    data_df[LABEL_COLUMN3] = data_df[LABEL_COLUMN3].astype(int)
    data_df[LABEL_COLUMN4] = data_df[LABEL_COLUMN4].astype(int)

    data_x, data1_y , data2_y, data3_y, data4_y = convert_data(data_df)
    return data_x, data1_y , data2_y, data3_y, data4_y


#모델 생성 - 버트모델 가중치는 따로 불러옴
def create_mbti_bert():
    loss = {'mbti_e_i' : tf.keras.losses.BinaryCrossentropy(from_logits = True), 'mbti_n_s': tf.keras.losses.BinaryCrossentropy(from_logits = True), 'mbti_n_s': tf.keras.losses.BinaryCrossentropy(from_logits = True), 'mbti_n_s': tf.keras.losses.BinaryCrossentropy(from_logits = True) }
    SEQ_LEN = 128
    BATCH_SIZE = 20
    # 버트 pretrained 모델 로드
    model = TFBertModel.from_pretrained('bert-base-multilingual-cased')
    # 토큰 인풋, 마스크 인풋, 세그먼트 인풋 정의
    token_inputs = tf.keras.layers.Input((SEQ_LEN,), dtype=tf.int32, name='input_word_ids')
    mask_inputs = tf.keras.layers.Input((SEQ_LEN,), dtype=tf.int32, name='input_masks')
    segment_inputs = tf.keras.layers.Input((SEQ_LEN,), dtype=tf.int32, name='input_segment')
    # 인풋이 [토큰, 마스크, 세그먼트]인 모델 정의
    bert_outputs = model([token_inputs, mask_inputs, segment_inputs])

    bert_outputs = bert_outputs[1]
    mbti_e_i = tf.keras.layers.Dense(1, activation='sigmoid',kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02),name='mbti_e_i')(bert_outputs)
    mbti_n_s = tf.keras.layers.Dense(1, activation='sigmoid',kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02),name='mbti_n_s')(bert_outputs)
    mbti_f_t = tf.keras.layers.Dense(1, activation='sigmoid',kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02),name='mbti_f_t')(bert_outputs)
    mbti_j_p = tf.keras.layers.Dense(1, activation='sigmoid',kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02),name='mbti_j_p')(bert_outputs)
  
    mbti_model = tf.keras.Model([token_inputs, mask_inputs, segment_inputs], [mbti_e_i,mbti_n_s,mbti_f_t,mbti_j_p])
    mbti_model.compile(optimizer=tf.keras.optimizers.Adam(lr=3e-5), loss=loss, metrics = ['acc'])
    return mbti_model

# 예측 컨버트 데이터 생성을 위함
def predict_convert_data(data_df):
    global tokenizer
    tokens, masks, segments = [], [], []
    SEQ_LEN = 128
    BATCH_SIZE = 20
    # 판단할 문장을 포함하고 있는 칼럼
    DATA_COLUMN = "feature_total"
    # mbti를 (각각 레이블 1 -> i_e , 2 -> n_s , 3-> f_t , 4-> j_p를 의미) 포함하고 있는 칼럼
    LABEL_COLUMN1 = "mbti_i_e"
    LABEL_COLUMN2 = "mbti_n_s"
    LABEL_COLUMN3 = "mbti_f_t"
    LABEL_COLUMN4 = "mbti_j_p"


    for i in tqdm(range(len(data_df))):
        token = tokenizer.encode(data_df[DATA_COLUMN][i], max_length=SEQ_LEN, truncation=True, padding='max_length')
        num_zeros = token.count(0)
        mask = [1]*(SEQ_LEN-num_zeros) + [0]*num_zeros
        segment = [0]*SEQ_LEN

        tokens.append(token)
        segments.append(segment)
        masks.append(mask)

    tokens = np.array(tokens)
    masks = np.array(masks)
    segments = np.array(segments)
    return [tokens, masks, segments]

# 로드 데이터 하면 토큰,세그먼트,마스킹
def predict_load_data(pandas_dataframe):

    # 판단할 문장을 포함하고 있는 칼럼
    DATA_COLUMN = "feature_total"
    # mbti를 (각각 레이블 1 -> i_e , 2 -> n_s , 3-> f_t , 4-> j_p를 의미) 포함하고 있는 칼럼
    LABEL_COLUMN1 = "mbti_i_e"
    LABEL_COLUMN2 = "mbti_n_s"
    LABEL_COLUMN3 = "mbti_f_t"
    LABEL_COLUMN4 = "mbti_j_p"

    data_df = pandas_dataframe
    data_df[DATA_COLUMN] = data_df[DATA_COLUMN].astype(str)
    data_x = predict_convert_data(data_df)
    return data_x

#결과 mbti추출하는 함수
def mbti_result(preds):
    mbti_e_i ,mbti_n_s , mbti_f_t , mbti_j_p = [] , [] , [], []
    for i in range(0,len(preds[0])):
        if preds[0][i] > 0.5:
            mbti_e_i.append('I')
        else:
            mbti_e_i.append('E')
    for i in range(0,len(preds[1])):
        if preds[1][i] > np.median(preds[1]):
            mbti_n_s.append('S')
        else:
            mbti_n_s.append('N')
    for i in range(0,len(preds[2])):
        if preds[2][i] > 0.5:
            mbti_f_t.append('T')
        else:
            mbti_f_t.append('F')
    for i in range(0,len(preds[3])):
        if preds[3][i] > 0.5:
            mbti_j_p.append('P')
        else:
            mbti_j_p.append('J')
    preds_total = pd.DataFrame({'preds_e_i':mbti_e_i,'preds_n_s':mbti_n_s,'preds_f_t':mbti_f_t,'preds_j_p':mbti_j_p})
    preds_total['predict_mbti'] = preds_total['preds_e_i'] + preds_total['preds_n_s'] + preds_total['preds_f_t'] + preds_total['preds_j_p']
    preds_total.drop(['preds_e_i','preds_n_s','preds_f_t','preds_j_p'],axis=1,inplace=True)
    return preds_total