from django.db import models

# Create your models here.


class Problem(models.Model):
    problem_name = models.CharField(max_length=40)
    problem_level = models.IntegerField()
    problem_desc = models.TextField()

    def __str__(self):
        return self.problem_name


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=30)
    submitted_at = models.DateTimeField()
    submittedcode = models.TextField()

    def __str__(self):
        return self.verdict

class TestCase(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    inp = models.TextField()
    outp = models.TextField()

  
