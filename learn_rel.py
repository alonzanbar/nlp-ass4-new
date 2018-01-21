import sys

from ConvertFeatures import convert
from ExtractFeatures import extract
from TrainSolver import train
from eval import eval_main
from predict import  predict_main

if __name__=="__main__":
    train_file = sys.argv[1]
    feature_file = sys.argv[2]
    features_vecs = sys.argv[3]
    model_file_name=  sys.argv[4]
    map_file_name = sys.argv[5]
    test_file_name = sys.argv[6]
    out_file  = sys.argv[7]
    extract(train_file,feature_file)
    convert(feature_file,features_vecs,map_file_name)
    train(features_vecs,model_file_name)
    predict_main(model_file_name,map_file_name,test_file_name,out_file,True)
    eval_main(test_file_name,out_file)