keywords = {
    'ABDUCTION_TYPE': ['অপহরণ', 'অপহরণকারী', 'অপহৃত', 'মুক্তিপণ', 'অপহরণের'],
    'DRUGS_TYPE': ['মাদক', 'মাদকের', 'হেরোইন', 'হেরোইনের', 'ইয়াবা', 'মাদকদ্রব্য', 'মাদকদ্রব্যয়ের', 'ফেনসিডিল',
                   'ফেনসিডিলে'],
    'MURDER_TYPE': ['হত্যা', 'হত্যাকারী', 'খুন', 'হত্যার', 'খুনের', 'ছুরিকাঘাত', 'ছুরিকাঘাতের', 'ছুরিকাঘাতে',
                    'কুপিয়ে'],
    'THEFT_TYPE': ['চুরি', 'চুরির', 'চোর', 'চোরের', 'ডাকাত', 'ডাকাতি', 'ডাকাতের', 'ডাকাতির', 'ছিনতাই',
                   'ছিনতাইকারী', 'ছিনতাইয়ের'],
    'RAPE_TYPE': ['ধর্ষণ', 'ধর্ষণের', 'ধর্ষণে', 'ধর্ষণকারী', 'ধর্ষক', 'ধর্ষিত', 'ধর্ষকের', 'ধর্ষিতের', 'ধর্ষিতার',
                  'ধর্ষণচেষ্টা', 'শ্লীলতাহানি', 'সম্ভ্রমহানি']
}

all_keywords = []
keyword2type = dict()
for typ in keywords:
    kws = keywords[typ]
    for kw in kws:
        all_keywords.append(kw)
        keyword2type[kw] = typ


def get_type(keyword):
    return keyword2type[keyword]


def contains_keyword(title):
    kws = []
    for kw in all_keywords:
        if title.find(kw) != -1:
            kws.append(kw)
    return kws


def get_types(kws: list):
    types = set()
    for kw in kws:
        types.add(keyword2type[kw])
    return list(types)


if __name__ == "__main__":
    print(get_types(all_keywords))
