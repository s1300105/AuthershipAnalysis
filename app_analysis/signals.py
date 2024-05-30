from django.db.models.signals import post_save
from django.dispatch import receiver
from collections import Counter
from app_analysis.models import FileModel,FreqWord

import nltk
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = stopwords.words('english')



@receiver(post_save, sender=FileModel)
def create_frequent_words(sender, instance, created, **kwargs):
    print("get signal")
    if created:
        file_path = instance.file_field.path
        with open(file_path, 'r', encoding="shift_jis") as file:
            raw = file.read()
        raw = re.sub("[^a-zA-Z]", " ", raw)
        tokens = nltk.word_tokenize(raw)
        tokens_l = [w.lower() for w in tokens] # all lower case 
        for word in stop_words:
            tokens_l.remove(word) # remove stopwords
        for i, w in enumerate(tokens_l):
            if len(w) == 1:
                del_w = tokens_l.pop(i) # delete 1 charactor token

        fdist = nltk.FreqDist(tokens_l)
        for word,count in fdist.items():
            FreqWord.objects.create(relate_file=instance, word=word, count=count)
