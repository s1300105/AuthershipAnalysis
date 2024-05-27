from django.db.models.signals import post_save
from django.dispatch import receiver
from collections import Counter
from app_analysis.models import FileModel,FreqWord

import nltk

@receiver(post_save, sender=FileModel)
def create_frequent_words(sender, instance, created, **kwargs):
    print("get signal")
    if created:
        file_path = instance.file_field.path
        with open(file_path, 'r', encoding="shift_jis") as file:
            raw = file.read()
        tokens = nltk.word_tokenize(raw)
        text = nltk.Text(tokens)
        tokens_l = [w.lower() for w in tokens] #全小文字
        fdist = nltk.FreqDist(tokens_l)
        for word,count in fdist.items():
            FreqWord.objects.create(relate_file=instance, word=word, count=count)
