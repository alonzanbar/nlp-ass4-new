import sys


def load_features(f_file):
    fnum = 0
    tnum = 0
    feature_set= set()
    F2I = {}
    for l in file(f_file):
        linelist = l.strip('\n').split('\t')
        feature_set|=set(linelist)

    F2I = {k:v for v,k in enumerate(feature_set)}
    return F2I

def save_words(F2I,f_file,output_q_file,map_file):

    with open(output_q_file, 'w') as outfile:
        for l in file(f_file):
            linelist = l.strip('\n').split('\t')
            label_str = linelist[0]
            features_str_arr = linelist[1:]
            label,features = convert_line(F2I, label_str,features_str_arr)
            outfile.write(label + " " +' '.join([str(f)+":1" for f in features])+"\n")
    with open(map_file,'w') as mapfile:
            for l in F2I.items():
                mapfile.write(l[0] +"\t"+ str(l[1])+"\n")


def convert_line(F2I, label_str,features_str_arr):
    label = str(F2I[label_str])
    features = sorted(set([F2I[i] for i in features_str_arr]))
    return label,features


def convert(features_file,feature_vecs_file,map_file):
    F2I = load_features(features_file)
    save_words(F2I,features_file,feature_vecs_file,map_file)

if __name__ == "__main__":
    convert(sys.argv[1],sys.argv[2],sys.argv[3])
    # dir = os.path.dirname(os.path.realpath('__file__'))
    # filename = os.path.join(dir, 'output.text')
    # load_features(filename)
    # save_words(filename,"output_v.txt","map.txt")




