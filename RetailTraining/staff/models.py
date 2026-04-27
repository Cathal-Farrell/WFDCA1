from django.db import models

# Create your models here.

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    content = models.CharField(max_length=20000)
    roleID = models.ForeignKey('store.Role', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200) 

    def __str__(self):
        return self.question_text
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.choice_text