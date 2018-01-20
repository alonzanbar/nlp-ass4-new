import logging

import scipy
import pickle
import sys
from ExtractPairs import get_DEV_pairs, extract_features_pairs, get_TEST_pairs, read_sentences_from_annotated

from utils import load_map, convert_features, PERSON_STR, save_file

LIVE_IN = "Live_In"

def get_en_type_from_pair(pair):
    for en in pair[0]:
        if en.label_ in PERSON_STR:
            p_en = en
        else:
            loc_en = en
    return p_en,loc_en

def predict(model,featuremap,test_file_name):
    predictions =[]
    rev_featuremap = {v:k for k,v in featuremap.items()}
    match = total_preds = total_true =  0.0
    for sent_id, sent in read_sentences_from_annotated(test_file_name).iteritems():
        live_num= 0
        for rel in sent.relations:
            if  LIVE_IN == rel:
                live_num+=1
        if live_num==0:
            continue
        total_true+=live_num
        print ("\n----------------------------")
        print(sent.sent)
        for ann in sent.annotations:
            print (ann)
        doc =sent.get_nlpsent()
        pairs = get_DEV_pairs(sent)
        samples = extract_features_pairs(doc, pairs)

        for i,(y,x) in enumerate(samples):
            feature_v = convert_features(featuremap,x)
            v = scipy.sparse.csr_matrix(feature_v)
            pred = model.predict(v)
            pred_str = rev_featuremap[str(int(pred[0]))]
            if pred_str=='1': # if we predict current pair includes the relation
                p_en,loc_en = get_en_type_from_pair(pairs[i])
                print("predicted : entity 1: {} , entity2 : {}".format(p_en,loc_en))
                predictions.append((sent_id, p_en, LIVE_IN, loc_en, sent.sent))
                if str(y)=='1': # if this pair was tagged with the relation
                    logging.info(sent_id + " " + sent.sent)
                    print("match !")
                    match+=1

                total_preds+=1
            total_true+=1 if y==1 else 0

    prec = match / total_preds
    recall = match / total_true
    f1 = 2 * prec * recall / (prec + recall)
    print("total_true: {}, total_preds: {}, match: {}".format(total_true,total_preds,match))
    print("prec : {}, recall : {}, f1 : {}".format(prec, recall, f1))
    return predictions

def predict_test(model,featuremap,test_file):
    rev_featuremap = {v: k for k, v in featuremap.items()}
    for sent_str in read_sentences_from_annotated(test_file_name):
        pairs = get_TEST_pairs(doc)
        samples = extract_features_pairs(doc, pairs)
        for i, (y, x) in enumerate(samples):
            feature_v = convert_features(featuremap, x)
            v = scipy.sparse.csr_matrix(feature_v)
            pred = model.predict(v)
            pred_str = rev_featuremap[str(int(pred[0]))]
            if pred_str == '1':  # if we predict current pair includes the relation
                p_en, loc_en = get_en_type_from_pair(pairs[i])
                predictions.append((sent_id, p_en, rel, loc_en, sent_str))
    return predictions


if __name__=="__main__":
    model_file_name=  sys.argv[1]
    map_file_name = sys.argv[2]
    test_file_name = sys.argv[3]
    out_file  = sys.argv[4]
    predict_type = sys.argv[5] if len(sys.argv)>5 else None

    model  = pickle.load(open(model_file_name, 'rb'))

    featuremap = load_map(map_file_name)
    if predict_type:
        predictions  = predict(model,featuremap,test_file_name)
    else:
        predictions = predict_test(model,featuremap,test_file_name)

    save_file(out_file,predictions)