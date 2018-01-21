# Save Model Using Pickle
from sklearn.linear_model import LogisticRegression
import pickle
import sys
from sklearn.datasets import load_svmlight_file


def train_model(in_file):
    X, Y = load_svmlight_file(in_file)

    model = LogisticRegression()
    model.fit(X, Y)
    correct=0.0
    for v,x in enumerate(X):
        correct+=1 if model.predict(x)== Y[v] else 0
    print correct/len(Y)
    return model

def save_model(out_file,model):
    pickle.dump(model, open(out_file, 'wb'))

def train(features_vecs,model_file):
    model = train_model(features_vecs)
    save_model(model_file,model)


if __name__ == "__main__":
    train(sys.argv[1],sys.argv[2])
    # in_file = get_abs_file('..\\out\\feature_map')
    # model_file = ('..\\out\\model_test1')
    # main(["",in_file,model_file])

