from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import User , UserProfile

#Post_Save
#Reciver function - We basically want the recoever function to connect to sender function via signals
@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender , instance , created ,**kwargs):
    #if True
    print(created)
    if created:
        print('created')
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
    print(instance.username , 'this username has been saved --presave signals')


    