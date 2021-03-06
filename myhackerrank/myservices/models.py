from django.db import models
from django import forms
import random
import string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import os


#one to many relationship with interviews table
class Candidate(models.Model):
	user_name = models.EmailField()
	created_at = models.DateTimeField()
	def save(self):
		if not self.id:
			self.created_at = timezone.now()
		super(Candidate, self).save()
	def __str__(self):
		return 'Candidate: {}'.format(self.user_name)

#many to many relationship between interviews and problems
class Problem(models.Model):
	difficulty = models.CharField(max_length=20)
	problem_name = models.CharField(max_length=20)
	problem_path = models.CharField(max_length=64)
	#changes the display on the admin site and when you print
	def __str__(self):
		return '{} : {} : {}'.format(self.difficulty, self.problem_name, self.id)

	def display_file(self):
		filep = settings.PROBLEM_PATH_PREFIX + self.problem_path
		with open(filep) as f:
			return f.read()


#pass it length 64 for a 512 bits hash string
def random_string(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))


#does this need a foreign key to candidate with the one-to-one field
class Interview(models.Model):
	INTERVIEW_STATUS_CHOICES = (
		('Draft', 'Draft'),
		('Online', 'Online'),
		('Started', 'Started'),
		('Completed', 'Completed'),
		)
	started_at = models.DateTimeField(null=True, default=None)
	status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES)
	hash_str = models.CharField(max_length=64, db_index=True) #access the problems using .problem_set.all()
	#access the submission ids using .hackerrank_set.all()
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
	problems = models.ManyToManyField(Problem)
	created_at = models.DateTimeField()
	duration = models.FloatField()

	def save(self):
		if not self.id:
			self.hash_str = random_string(64)
			self.created_at = timezone.now()
		super(Interview, self).save()
		message = settings.DEFAULT_DOMAIN + '/interview/' + self.hash_str
		send_mail('Interview link', message , os.getenv('NOTIFICATION_EMAIL_SENDER'), ['test@gmail.com'], fail_silently=False)


#each submission has a foreign key to the candidate it belongs to as well as the interview?? Many submissions for one interview and one candidate

class Submission(models.Model):
	submit_id = models.IntegerField(null=True, default=None)
	result = models.CharField(max_length=20, null=True, default=None)
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE) 
	interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
	submit_at = models.DateTimeField()

	def save(self):
		if not self.id:
			self.submit_at = timezone.now()
		super(Submission, self).save()


