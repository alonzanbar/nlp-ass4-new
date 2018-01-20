

from parse_tree_utils import get_parse_tree_path, extract_dep_map, build_graph


def extract_features(pair, doc):
    en1, en2 = pair
    start = en1.end
    end = en2.start
    prev_word = doc[en1.start - 1].text if en1.start > 0 else 'None'
    next_word = doc[en2.end].text if en2.end < len(doc) else 'None'
    prev_tag = doc[en1.start - 1].tag_ if en1.start > 0 else 'None'
    word_dep , typed_dep_map = extract_dep_map(en1.root,en2.root,doc)
    words_set = set([t.lemma_ for t in doc[start:end]])
    consitutient_path = (get_parse_tree_path(doc.text, en1.root.text, en2.root.text))
    features = {

        'entity1-type': en1.label,
        'entity1-head': en1.root.lemma_,
        #'entity1-text': (en1.text).replace(" ","-"),
        'entity2-type': en2.label,
        'entity2-head': en2.root.lemma_,
        #'entity2-text': (en2.text).replace(" ","-"),
        'tag-before': prev_tag,
        'concatenatedtypes': en1.label_ + en2.label_,
        #'syntactic-path': "-".join([w.pos_ for w in doc[start:end]]),
        #'base-syntactic-path': "-".join([w.tag_ for w in doc[start:end]]),
        'word-before-entity1': prev_word,
        'word-after-entity2': next_word,
        'dep-path': typed_dep_map,
        'word-dep-path' : word_dep,
        'dis_ent_distance': len(typed_dep_map) / 3,
        'between-entities-word': words_set,
        'consitutient_path': consitutient_path

    }

    return features
