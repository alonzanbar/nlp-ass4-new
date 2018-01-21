

from parse_tree_utils import get_parse_tree_path, extract_dep_map, build_graph


def extract_features(pair, doc):
    en1, en2 = pair
    start = en1.end
    end = en2.start
    prev_word = doc[en1.start - 1].lemma_ if en1.start > 0 else 'None'
    next_word = doc[en2.end].lemma_ if en2.end < len(doc) else 'None'
    prev_tag = doc[en1.start - 1].tag_ if en1.start > 0 else 'None'
    typed_dep_map = extract_dep_map(en1.root,en2.root,doc)
    word_dep , type_dep , tag_dep = zip(*typed_dep_map)
    words_list = [t.lemma_ for t in doc[start:end]]
    systactic_after = [w.tag_ for w in doc[end+1:]] if end+1<len(doc) else None
    #consitutient_path = (get_parse_tree_path(doc.text, en1.root.text, en2.root.text))
    features = {

        'entity1-type': en1.label,
        'entity1-head': en1.root.lemma_,
        #'entity1-text': "-".join([t.lemma_ for t in doc[en1.start:en1.end]]),
        'entity2-type': en2.label,
        'entity2-head': en2.root.lemma_,
        #'entity2-text': "-".join([t.lemma_ for t in doc[en2.start:en2.end]]),
        'word-before': prev_word,
        'tag-before': prev_tag,
        'concatenatedtypes': en1.label_ + en2.label_,
        #'syntactic-path': [w.pos_ for w in doc[start:end]],
        'base-syntactic-path': [w.tag_ for w in doc[en1.start:en2.end]],
        #'syntatic-after_en2:':systactic_after,
        'word-after-entity2': next_word,
        'dep-path': list(type_dep),
        'word-dep-path' : list(word_dep),
        'tag-dep-path' : list(tag_dep),
        'dis_ent_distance': len(type_dep) / 2,
        'between-entities-word_set': set(words_list),
        'between-entities-word_concat': "-".join(words_list),

        #'consitutient_path': consitutient_path

    }

    return features
