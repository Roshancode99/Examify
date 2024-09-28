from django.db import models
from django.db.models import JSONField

# Create your models here.
class StrategyName(models.Model):
    strategyname = models.CharField(max_length=100, primary_key=True,unique=True)


class Question(models.Model):
    DIFFICULTY_CHOICES = (
        ('ease', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    qtype = (
        ("coding", "Coding"),
        ("subjective", "Subjective"),
        ("mcq", "MCQ")
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    recommended_time = models.IntegerField(blank= False)
    inputs = JSONField(defualt=list,null=True,Blank=True)
    starter_code = models.TextField(blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    tscore = models.IntegerField(default = 0)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10, choices=qtype)


    class Meta:
        ordering = ('-created_at',)


class McqOptions(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    isValid = models.BooleanField(default=False)


class Test(models.Model):
    title = models.CharField(max_length=255)
    role = models.TextField(blank=False, default=None)
    attempted = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)
    public= models.BooleanField(default=False)
    questions = models.ManyToManyField(Question, related_name='tests', through="TestsQuestionsRelation")
    duration = models.IntegerField(default=40)
    cutoff = models.IntegerField(default = 0)
    mcqScores = models.IntegerField(default = 5)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestsQuestionsRelation(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('test', 'question')


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name= models.TextField(default = "")
    input_data = models.TextField()
    expected_output = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("self score", self.score)
        print("question score", self.question.tscore)

        self.question.tscore = int(self.question.tscore) + int(self.score)
        self.question.save()



class Clients(models.Model):
    isAdmin = models.BooleanField(db_column="IsAdmin",null=False,defualt=False)
    password = models.CharField(db_column="Password",max_length=250,null=False)
    firstname = models.CharField(db_column="FirstName",max_length=100,null=False,default='')
    lastname = models.CharField(db_column="LastName",max_length=100,null=False,default='')
    email = models.CharField(db_column="Email",max_length=100,unique=True,null=False)
    isdisabled = models.BooleanField(db_column='isDisabled',default=False)
    createddate = models.DateTimeField(db_column='CreatedDate',auto_now_add=True)
    updatedate = models.TimeField(db_column='UpdateDate',auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            test_invitations = TestInvitation.objects.filter(client_email = self.email)

            for test_invitation in test_invitations:
                test_invitation.client_name = f"{self.firstname} {self.lastname}"
                test_invitation.save()
        except TestInvitation.DoesNotExist:
            pass



class TestInvitation(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    client_email = models.CharField(max_length=100, blank=False) 
    client_name = models.CharField(max_length=100, default="")
    token = models.TextField()
    isAttempted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('client_email', 'test')



class QuestionAttempt(models.Model):
    user = models.ForeignKey(Clients, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code=models.TextField(default="")
    result = models.IntegerField(default=0)
    output=JSONField(default=list,null=True,blank=True)
    stderr=models.TextField(default="")
    for_test = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ans = models.TextField(default="", blank=True)


class TestAttempt(models.Model):
    status = (
        ("N/A", "n/a"),
        ("idle", "idle"),
        ("Running", "running"),
        ("Completed", "completed")
    )
    user = models.ForeignKey(Clients, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    time_taken = models.IntegerField(default=0)  
    score = models.IntegerField(default=0)
    question_attempts = models.ManyToManyField(QuestionAttempt, through="TestQuestionAttemtRelation")
    contact_email = models.TextField(blank=False)
    experience=models.IntegerField(default=0, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    stratagyStatus = models.CharField(max_length=15, choices=status, default="N/A")

    class Meta:
        unique_together = ('user', 'test',)
            



class TestQuestionAttemtRelation(models.Model):
    tAttempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE)
    qAttempt = models.ForeignKey(QuestionAttempt, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tAttempt', 'qAttempt')


#SuspiciousActivity

class TestPing(models.Model):
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class TabSwitchActivity(models.Model):
    TabSwitchActionChoice = (
        ('TAB_LEAVE', 'Tab Leave'),  
        ('TAB_RETURN', 'Tab Return'),      
    )
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10, choices=TabSwitchActionChoice)

class WindowSwitchActivity(models.Model):
    WindowSwitchActionChoice = (
        ('WINDOW_SWITCH', 'Window Switch'), 
        ('BROWSER_RETURN', 'Browser Return'), 
    )
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=14, choices=WindowSwitchActionChoice)


class CopyPasteActivity(models.Model):
    ACTION_CHOICES = (
        ('copy', 'Copy'),
        ('paste', 'Paste'),
    )
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE)
    action = models.CharField(max_length=5, choices=ACTION_CHOICES)
    copied_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

