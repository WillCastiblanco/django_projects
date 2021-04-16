from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors ={}
        if len(postData['first_name'])<2:
            errors['first_name']='First Name must be longer than 2 characters'

        if len(postData['last_name'])<2:
            errors['last_name']='Last Name must be longer than 2 characters'

        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"

        users_with_email = User.objects.filter(email=postData['email'])
        if len(users_with_email)>0:
            error['duplicate']='Email already exists'

        if len(postData['password'])<6:
            errors['password']='Password must be longer than 6 characters'

        if postData['password']!=postData['conf_password']:
            errors['pw_match']='Password is different than confirmed password'

        #email address should be valid
        #passwords should match

        return errors

    def credentials_validator(self,thisEmail,thisPassword):
        users = self.filter(email=thisEmail)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(thisPassword.encode(),user.password.encode())


class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    # birthday =models.DateTimeField()
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

