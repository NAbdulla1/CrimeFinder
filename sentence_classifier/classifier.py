import pickle
import os


class SentenceClassifier:
    voter_models = []  # the models will vote if it is a location sentence or not
    model_dir = "./sentence_classifier/pre_trained_models"

    def __init__(self):
        for file_name in os.listdir(self.model_dir):
            file_path = os.path.join(self.model_dir, file_name)
            with open(file_path, 'rb') as saved_model:
                retrieved_model = pickle.load(saved_model)
                if file_name == 'bag_of_words.sav':
                    self.vectorizer = retrieved_model
                elif file_name == 'tfidfconverter.sav':
                    self.tfidf_converter = retrieved_model
                else:
                    self.voter_models.append(retrieved_model)

    def is_location_sentence(self, sentence):
        location = 0
        not_location = 0
        vec = self.vectorizer.transform([sentence]).toarray()
        vec = self.tfidf_converter.transform(vec).toarray()
        for model in self.voter_models:
            prediction = model.predict(vec)
            if prediction[0] == 1:
                location += 1
            else:
                not_location += 1
        return location >= not_location

# if __name__ == "__main__":
#    sc = SentenceClassifier()
#    with open('pos.txt') as pos, open('neg.txt') as neg:
#        positive = pos.readlines()
#        negative = neg.readlines()
#    # data = [stem(sen) for sen in positive] + [stem(sen) for sen in negative]
#    data = [sen for sen in positive] + [sen for sen in negative]
#    target = [1] * len(positive) + [0] * len(negative)

#    import random

#    correct = 0
#    for rr in range(1000):
#        ri = random.randint(0, len(target) - 1)
#        sentence = data[ri]
#        label = target[ri]
#        predicted = sc.is_location_sentence(preprocess(sentence))
#        if predicted == label:
#            correct += 1
#    print(correct / 1000.0)
