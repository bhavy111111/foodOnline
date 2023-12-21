from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
#from django.db.models.signals import post_save , pre_save
#from django.dispatch import receiver
from django.db.models.fields.related import ForeignKey, OneToOneField

class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('Username must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        #Encode the password and store into password variable
        user.set_password(password)
        #It will take the default databse which we have 
        user.save(using=self._db)
        return user
    
    def create_superuser(self ,  first_name,last_name,username , email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff = True
        user.is_superadmin=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER=2

    ROLE_CHOICE = (
        (VENDOR , 'VENDOR'),
        (CUSTOMER , 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50 , unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=12,blank=True)

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE , blank=True,null=True)
    #required fields

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' , 'first_name' , 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    #If user is active super user and admin
    def has_module_perms(self,app_label):
        return True



    
class UserProfile(models.Model):
    #when user is deleted user profile will be deleted -CASCADE
    user = OneToOneField(User , on_delete = models.CASCADE , blank=True,null=True)
    profile_picture = models.ImageField(upload_to='media/profile_pictures',blank=True,null=True)
    cover_photo = models.ImageField(upload_to='media/cover_photos',blank=True,null=True)
    address_line_1 = models.CharField(max_length = 50 , blank=True , null=True)
    country = models.CharField(max_length=15 , blank=True , null = True)
    state = models.CharField(max_length = 15 , blank=True,null=True)
    city = models.CharField(max_length=15 , blank=True,null=True)
    pincode = models.CharField(max_length=6 , blank=True,null=True)
    latitude = models.CharField(max_length=20,blank=True,null=True)
    longitutde =models.CharField(max_length=20,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
'''
#Post_Save
#Reciver function - We basically want the recoever function to connect to sender function via signals
@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender , instance , created ,**kwargs):
    #if True
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('userprofile is created')
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #Create the userprofile if not exist
            UserProfile.objects.create(user=instance)
            print('Profile was not exist so i created')

        print('User iis updated')

#post_save.connect(post_save_create_profile_receiver,sender=User)
        
#Lets make pre_save , which will tell which username is being saved before getting into the database
        
@receiver(pre_save , sender = User)
def pre_save_profile_receiver(sender,instance,**kwargs):
    print(instance.username , 'this username has been saved')
'''

    



