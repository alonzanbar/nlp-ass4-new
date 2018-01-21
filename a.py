SHIFT = 1
START = "START"
END = "END"

UP = "UP"
DOWN = "DOWN"
TOP = "TOP"


def to_string_points_to_the_other(first_chunk, second_chunk, sentence, id):
    first, second = find_dependency_routes(first_chunk, second_chunk, sentence)
    if len(first) == 1:
        # print "1"
        return ["TheFirstPointsToTheSecond%s" % id]
    # print len(first)
    return []


def to_string_previous_tag(chunk, sentence, id):
    return "PreviousTag%s(%s)" % (id, get_previous_tag(chunk, sentence))


def parse_chunk(chunk):
    return ' '.join(word['word'] for word in chunk)


def to_string_words_in_chunk(chunk):
    return "WordsInChunk(%s)" % parse_chunk(chunk)

def to_string_word_before_chunk(id, chunk, sentence):
    return "WordBeforeChunk%s(%s)" % (id, get_previous_word(chunk, sentence))

def to_string_word_after_chunk(id, chunk, sentence):
    return "WordAfterChunk%s(%s)" % (id, get_next_word(chunk, sentence))


def get_previous_tag(chunk, sentence):
    id_first_word_in_chunk = chunk[0]['id']
    if id_first_word_in_chunk - 1 - SHIFT >= 0:
        return sentence["words"][id_first_word_in_chunk - 1 - SHIFT]['pos']
    return START

def get_previous_word(chunk, sentence):
    id_first_word_in_chunk = chunk[0]['id']
    if id_first_word_in_chunk - 1 - SHIFT >= 0:
        return sentence["words"][id_first_word_in_chunk - 1 - SHIFT]['word']
    return START

def get_next_word(chunk, sentence):
    id_last_word_in_chunk = chunk[-1]['id']
    if id_last_word_in_chunk + 1 - SHIFT < len(sentence["words"]):
        return sentence["words"][id_last_word_in_chunk + 1 - SHIFT]['word']
    return START


def to_string_distance_between_chunks(first_chunk, second_chunk, sentence):
    if first_chunk[0]['id'] > second_chunk[0]['id']:
        return "Distance(%s)" % ((first_chunk[0]['id'] - second_chunk[-1]['id']) < 10)
    return "Distance(%s)" % ((second_chunk[0]['id'] - first_chunk[-1]['id']) < 10)


def type_tag(chunk, id):
    return "Type%s(%s)" % (id, chunk[0]['ner'])

def concat_tag(chunk1, chunk2):
    return "TypeConcat(%s)" % (chunk1[0]['ner']+chunk2[0]['ner'])

def to_string_find_dependency_tag_list(first_chunk, second_chunk, sentence):
    graph = find_dependency_graph(first_chunk, second_chunk, sentence)
    all_dependency_tags = []
    i = 0
    while graph[i] != graph[i + 1]:
        all_dependency_tags.append(to_string_dependency_tag(UP, graph[i], sentence))
        i += 1
        if i + 1 >= len(graph):
            return all_dependency_tags
    i += 1
    all_dependency_tags.append(to_string_dependency_tag(TOP, graph[i], sentence))
    i += 1
    while i < len(graph):
        all_dependency_tags.append(to_string_dependency_tag(DOWN, graph[i], sentence))
        i += 1
    return all_dependency_tags


def to_string_find_dependency_word_list(first_chunk, second_chunk, sentence):
    graph = find_dependency_graph(first_chunk, second_chunk, sentence)
    all_dependency_tags = []
    i = 0
    while graph[i] != graph[i + 1]:
        all_dependency_tags.append(to_string_dependency_word(UP, graph[i], sentence))
        i += 1
        if i + 1 >= len(graph):
            return all_dependency_tags
    i += 1
    all_dependency_tags.append(to_string_dependency_word(TOP, graph[i], sentence))
    i += 1
    while i < len(graph):
        all_dependency_tags.append(to_string_dependency_word(DOWN, graph[i], sentence))
        i += 1
    return all_dependency_tags


def to_string_find_dependency_type_list(first_chunk, second_chunk, sentence):
    graph = find_dependency_graph(first_chunk, second_chunk, sentence)
    all_dependency_tags = []
    i = 0
    while graph[i] != graph[i + 1]:
        all_dependency_tags.append(to_string_dependency_type(UP, graph[i], sentence))
        i += 1
        if i + 1 >= len(graph):
            return all_dependency_tags
    i += 1
    all_dependency_tags.append(to_string_dependency_type(TOP, graph[i], sentence))
    i += 1
    while i < len(graph):
        all_dependency_tags.append(to_string_dependency_type(DOWN, graph[i], sentence))
        i += 1
    return all_dependency_tags


def to_string_find_dependency_type_list2(first_chunk, second_chunk, sentence):
    graph = find_dependency_graph(first_chunk, second_chunk, sentence)
    all_dependency_tags = []
    i = 0
    # while graph[i] != graph[i + 1]:
    #     all_dependency_tags.append(to_string_dependency_type(UP, graph[i], sentence))
    #     i += 1
    #     if i + 1 >= len(graph):
    #         return all_dependency_tags
    # i += 1
    # all_dependency_tags.append(to_string_dependency_type(TOP, graph[i], sentence))
    # i += 1
    while i < len(graph):
        tag = word_content(i, sentence)['dependency']
        feature = "DependencyType2(%s)" % tag
        all_dependency_tags.append(feature)
        i += 1
    return all_dependency_tags


def to_string_dependency_tag(direction, id, sentence):
    word_context = sentence["words"][id - SHIFT]
    tag = word_context['tag']
    return "DependencyTag%s(%s)" % (1, tag)


def to_string_dependency_type(direction, id, sentence):
    tag = word_content(id, sentence)['dependency']
    return "DependencyType%s(%s)" % (direction, tag)


def word_content(id, sentence):
    return sentence["words"][id - SHIFT]


def to_string_dependency_word(direction, id, sentence):
    word_context = sentence["words"][id - SHIFT]
    tag = word_context['lemma']
    return "DependencyWord%s(%s)" % (1, tag)


def find_dependency_route(chunk, sentence):
    parent = chunk[0]['parent']
    current_id = chunk[0]['id']
    while sentence['words'][parent - SHIFT] in chunk:
        current_id = parent
        parent = sentence['words'][parent - SHIFT]['parent']
    path = [current_id]
    while True:
        path.append(parent)
        if parent == 0:
            break
        parent = sentence['words'][parent - SHIFT]['parent']
    return path


def dispose_overlapping(first_route, second_route):
    overlapping = -1
    while overlapping > -len(first_route) and overlapping > -len(second_route) and first_route[overlapping] == \
            second_route[overlapping]:
        overlapping -= 1
    if overlapping == -1:
        return first_route, second_route
    return first_route[0:overlapping + 1], second_route[0:overlapping + 1]


# TODO: Use this method to get features.
def find_dependency_graph(first_chunk, second_chunk, sentence):
    first, second = find_dependency_routes(first_chunk, second_chunk, sentence)
    return first + list(reversed(second))


def find_dependency_routes(first_chunk, second_chunk, sentence):
    first_route = find_dependency_route(first_chunk, sentence)
    second_route = find_dependency_route(second_chunk, sentence)
    first, second = dispose_overlapping(first_route, second_route)
    return first, second


def to_string_second_previous_tag(chunk, sentence, id):
    return "SecondPreviousTag%s(%s)" % (id, get_second_previous_tag(chunk, sentence))


def get_second_previous_tag(chunk, sentence):
    id_first_word_in_chunk = chunk[0]['id']
    if id_first_word_in_chunk - 2 - SHIFT >= 0:
        return sentence["words"][id_first_word_in_chunk - 2 - SHIFT]['pos']
    return START


def to_string_forward_tag(chunk, sentence, id):
    return "ForwardTag%s(%s)" % (id, get_forward_tag(chunk, sentence))


def get_forward_tag(chunk, sentence):
    id_first_word_in_chunk = chunk[-1]['id']
    if id_first_word_in_chunk + 1 - SHIFT < len(sentence["words"]):
        return sentence["words"][id_first_word_in_chunk + 1 - SHIFT]['pos']
    return END


def to_string_second_forward_tag(chunk, sentence, id):
    return "SecondForwardTag%s(%s)" % (id, get_second_forward_tag(chunk, sentence))


def get_second_forward_tag(chunk, sentence):
    id_first_word_in_chunk = chunk[0]['id']
    if id_first_word_in_chunk + 2 - SHIFT < len(sentence["words"]):
        return sentence["words"][id_first_word_in_chunk + 2 - SHIFT]['pos']
    return END


def to_string_chunk_head(chunk, sentence, id):
    return "HeadTag%s(%s)" % (id, get_head_tag(chunk, sentence))


def to_string_chunk_head_dependency(chunk, sentence, id):
    return "HeadDependency%s(%s)" % (id, get_head_dependency(chunk, sentence))


def get_head_tag(chunk, sentence):
    ids = set()
    for word in chunk:
        ids.add(word["id"])
    for word in chunk:
        if word["parent"] not in ids:
            return sentence["words"][word["parent"] - SHIFT]["tag"]


def get_head_dependency(chunk, sentence):
    ids = set()
    for word in chunk:
        ids.add(word["id"])
    for word in chunk:
        if word["parent"] not in ids:
            return sentence["words"][word["parent"] - SHIFT]["dependency"]


def to_string_bag_of_words(first_chunk, second_chunk, sentence):
    first, second = get_first_and_second_chunk(first_chunk, second_chunk)
    between_words = sentence["words"][first[-1]["id"]:second[0]["id"] - 1]

    return ["BagOfWords%s" % word["lemma"] for word in between_words]


def get_first_and_second_chunk(first_chunk, second_chunk):
    if first_chunk[0]["id"] < second_chunk[0]["id"]:
        return first_chunk, second_chunk
    return second_chunk, first_chunk


def get_head_id(chunk, sentence):
    ids = set()
    for word in chunk:
        ids.add(word["id"])
    for word in chunk:
        if word["parent"] not in ids:
            return word["id"]


class FeaturesBuilder():
    def __init__(self):
        pass

    def build_features(self, first_chunk, second_chunk, sentence):
        return [   type_tag(first_chunk, 1),
                   type_tag(second_chunk, 2),
                   to_string_words_in_chunk(first_chunk),
                   to_string_words_in_chunk(second_chunk),
                   concat_tag(first_chunk,second_chunk),
                   to_string_word_before_chunk(1, first_chunk, sentence),
                   to_string_word_after_chunk(2, second_chunk, sentence),
                   to_string_forward_tag(first_chunk, sentence, 1),
                   to_string_chunk_head(first_chunk, sentence, 1),
                   to_string_chunk_head(second_chunk, sentence, 2)] \
               + to_string_find_dependency_tag_list(first_chunk, second_chunk, sentence) \
               + to_string_find_dependency_word_list(first_chunk, second_chunk, sentence) \
               + to_string_find_dependency_type_list(first_chunk, second_chunk, sentence)  \
               + to_string_bag_of_words(first_chunk, second_chunk, sentence)

    # def build_features(self, first_chunk, second_chunk, sentence):
    #     return [  # to_string_previous_tag(first_chunk, sentence, 1),
    #                to_string_previous_tag(second_chunk, sentence, 2),
    #                # to_string_second_previous_tag(first_chunk, sentence, 1),
    #                # to_string_second_previous_tag(second_chunk, sentence, 2),
    #                type_tag(first_chunk, 1),
    #                type_tag(second_chunk, 2),
    #                # concat_tag(first_chunk,second_chunk),
    #                # to_string_words_in_chunk(first_chunk),
    #                # to_string_words_in_chunk(second_chunk),
    #                #to_string_word_before_chunk(1, first_chunk, sentence),
    #                #to_string_word_after_chunk(2, second_chunk, sentence),
    #                to_string_forward_tag(first_chunk, sentence, 1),
    #                to_string_distance_between_chunks(first_chunk,second_chunk, sentence),
    #                # to_string_forward_tag(second_chunk, sentence, 2),
    #                # to_string_second_forward_tag(first_chunk, sentence, 1),
    #                # to_string_second_forward_tag(second_chunk, sentence, 2),
    #                to_string_chunk_head_dependency(first_chunk, sentence, 1),
    #                to_string_chunk_head_dependency(second_chunk, sentence, 2),
    #                to_string_chunk_head(first_chunk, sentence, 1),
    #                to_string_chunk_head(second_chunk, sentence, 2)] \
    #            + to_string_find_dependency_tag_list(first_chunk, second_chunk, sentence) \
    #            + to_string_find_dependency_word_list(first_chunk, second_chunk, sentence) \
    #            + to_string_find_dependency_type_list(first_chunk, second_chunk, sentence)  \
    #            #+ to_string_bag_of_words(first_chunk, second_chunk, sentence)

class FeatureBuilders:
    ALL = [FeaturesBuilder()]