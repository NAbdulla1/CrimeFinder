from bnlp.ner import NER

bn_ner = NER()
model_path = "./bangla_ner/bn_ner.pkl"

suffmap = {'রে': 'র', 'তে': '', 'য়ের': '', 'ের': '', 'ার': 'া', 'ির': 'ি', 'ীর': 'ী', 'য়ে': '', 'ে': '', 'ায়': 'া',
           'ঁর': 'ঁ'}
exception = {'সাভার', 'বাজার', 'কক্সবাজার', 'মৌলভীবাজার'}


def get_location(loc_sentence):
    loc_sentence = loc_sentence.strip()
    result = bn_ner.tag(model_path, loc_sentence)
    addr_part = []
    for res in result:
        if '-LOC' in res[1]:
            if 'নগর' not in res[0] and 'উপজেলা' not in res[0] and 'সদর' not in res[0] and 'এলাকা' not in res[0] and 'ইউনিয়ন' not in res[0] and 'গ্রাম' not in res[0]:
                cur = res[0]
                for s in suffmap:
                    if cur.endswith(s) and cur not in exception:
                        # print(f"replacing {s} with '{suffmap[s]}'", end=' ')
                        # print(f"old: {cur},", end = ' ')
                        cur = cur[:-len(s)] + suffmap[s]
                        # print(f"new: {cur}")
                addr_part.append(cur)
    return addr_part
