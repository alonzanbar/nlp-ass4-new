from spc import nlp


class sentence:
    def __init__(self,sent_str,is_annotated):
        line1= sent_str.split("\t")
        self.id = line1[0]
        self.annotations = []
        self.relations=[]
        if is_annotated:
            self.add_annotation(sent_str)
            sent = sent_str[sent_str.find("(") + 1:sent_str.find(")")]
        else:
            sent = line1[2]
        sent = sent.replace("-LRB-", "(")
        sent = sent.replace("-RRB-", ")")
        self.sent = sent
        self.nlpsent = None


    def add_annotation(self,sent):
        line1 = sent.split("\t")
        self.annotations.append(annotation([line1[1],line1[2],line1[3]]))
        self.relations.append(line1[2])

    def get_nlpsent(self):

        if not self.nlpsent :
            self.nlpsent = nlp(unicode(self.sent))
        return self.nlpsent

class annotation:
    def __init__(self,annotation):
        self.en1 = annotation[0]
        self.rel = annotation[1]
        self.en2 = annotation[2]

    def __repr__(self):
        return self.en1 + " " + self.rel + " " + self.en2
