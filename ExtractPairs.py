import logging
import re
import sys
from FeatureBuilder import extract_features
from annotated_sentence import sentence
from temp_code.spc import read_sentences_from_annotated, nlp
from utils import PERSON_STR, LOCTATION_STRS, LIVE_IN
import yappi

NUMBER_NRG = 5

def format_token(token):
    return '{0}-{1}'.format(token.lower_, token.tag_)


def process_file(infile):
    samples=[]
    for sent in read_sentences_from_annotated(infile).itervalues():
        pairs = get_TRAIN_pairs(sent)
        pair_samples = extract_features_pairs(sent.nlpsent, pairs)
        samples.extend(pair_samples)
    return samples

def read_sentences_from_annotated(fname):
    lines_dic={}
    for line in open(fname):
        id = line.split("\t")[0]
        if id in lines_dic:
            lines_dic[id].add_annotation(line)
        else:
            lines_dic[id] = sentence(line,True)


    return lines_dic

def extract_features_pairs(doc, pairs):
    samples=[]
    for pair, label in pairs:
        print(pair)
        if not pair[0] or not pair[1] or not pair[0].root.text.strip() or not pair[1].root.text.strip():
            continue
        features_dict = extract_features(pair, doc)
        features=[]
        for k, v in features_dict.items():
            if isinstance(v,set):
                for it in v:
                    features.append("{0}={1}".format(k, it))
            else:
                features.append("{0}={1}".format(k, v))
        samples.append((label, features))
    return samples


def save_words(output_file,samples):
    with open(output_file, 'w') as outfile:
        for label,features in samples:
                 outfile.write(str(label) +'\t' + '\t'.join(features)+"\n")

def get_TRAIN_pairs(sent):
    for ann in sent.annotations:
        if ann.rel == LIVE_IN:
            replace_en(sent.get_nlpsent(), ann.en1, PERSON_STR)
            replace_en(sent.get_nlpsent(),ann.en2, LOCTATION_STRS)
    pairs = get_pairs_supervised(sent)
    return pairs


def get_DEV_pairs(sent):
    return get_pairs_supervised(sent)

def get_TEST_pairs(doc):
    return get_all_pairs(doc)


def get_all_pairs(doc):
    pairs = []
    for en_id1 in range(len(doc.ents)):
        for en_id2 in range(en_id1, len(doc.ents)):
            en1 = doc.ents[en_id1]
            en2 = doc.ents[en_id2]
            if (en1.label_ in PERSON_STR and en2.label_ in LOCTATION_STRS) or \
                    (en1.label_ in LOCTATION_STRS and en2.label_ in PERSON_STR):
                pairs.append(([en1, en2], 0))
    return pairs


def get_pairs_supervised(sent):
    pairs = []

    for [ne1, ne2],_ in get_all_pairs(sent.get_nlpsent()):
        label=0
        for ann in sent.annotations:
            if ann.rel==LIVE_IN and ((ne1.text == ann.en1 and ne2.text == ann.en2) or \
                    (ne1.text == ann.en2 and ne2.text == ann.en1)):
                label=1
                print ("found : entity1 : {}, entity2 : {}".format(ne1,ne2) )

        pairs.append(([ne1, ne2], label))
    return pairs


def replace_en(doc,str,labels):
    gold_words  = re.split(' |-',str)
    sent_words = [w.text for w in doc]
    label = nlp.vocab.strings[labels[0]]
    try:
        start, end  = sent_words.index(gold_words[0]),sent_words.index(gold_words[len(gold_words)-1])+1
    except ValueError:
        logging.info("found bad title : "+str)
        return
    span = None
    for en in doc.ents:
        if en.start==start or en.end==end:
            span=en
            break
    if span :
        doc.ents = [e for e in doc.ents if e !=span]
        if  span.label_ in labels:
            label = span.label
    doc.ents += ((label, start, end),)




if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    yappi.start()
    samples= process_file(infile)
    save_words(outfile,samples)
    yappi.get_func_stats().print_all()