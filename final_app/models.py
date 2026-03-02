from django.db import models
from django.contrib.auth.models import User


class usertables(models.Model):
   jobseeker=models.ForeignKey(User,on_delete=models.CASCADE)
   phonenumber=models.IntegerField( null=True, blank=True)

def __str__(self):
        return self.username

class adminmodel(models.Model):
    jobadmin=models.ForeignKey(User,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200)


class addjob(models.Model):
     admin = models.ForeignKey(adminmodel, on_delete=models.CASCADE, related_name='posted_jobs', null=True)
     job_name=models.CharField(max_length=200)
     job_salary=models.IntegerField()
     job_skill=models.CharField(max_length=520)
     job_qualification=models.CharField(max_length=200,null=True)
    
     def __str__(self):
        return self.job_name


class detail_of_jobseeker(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
     f_name=models.CharField(max_length=200)
     l_name=models.CharField(max_length=200)
     email=models.EmailField()
     dob=models.DateField(null=True, blank=True)
     phonenumber=models.IntegerField(null=True, blank=True)
     location=models.CharField(max_length=200)
     lat_quali=models.CharField(max_length=200)
     skill=models.CharField(max_length=200)
     year_of_exp=models.IntegerField(null=True, blank=True)
     img=models.ImageField(upload_to="image/",null=True)
     def get_skills_list(self):
        """Splits the skill string into a list for the template"""
        if self.skill:
            return [s.strip() for s in self.skill.split(',')]
        return []





class AppliedJob(models.Model):
    job = models.ForeignKey(addjob, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default="Pending")

    def __str__(self):
        return f"{self.user.username} - {self.job.job_name}"