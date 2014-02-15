from django.db import models

# Create your models here.
class UsersModel(models.Model):
     ## The success return code
    SUCCESS               =   1

    ## Cannot find the user/password pair in the database (for login only)
    ERR_BAD_CREDENTIALS   =  -1

    ## trying to add a user that already exists (for add only)
    ERR_USER_EXISTS       =  -2

    ## invalid user name (empty or longer than MAX_USERNAME_LENGTH) (for add, or login)
    ERR_BAD_USERNAME      =  -3

    ## invalid password name (longer than MAX_PASSWORD_LENGTH) (for add)
    ERR_BAD_PASSWORD      =  -4


    ## The maximum length of user name
    MAX_USERNAME_LENGTH = 128

    ## The maximum length of the passwords
    MAX_PASSWORD_LENGTH = 128


    user = models.CharField(max_length=MAX_USERNAME_LENGTH);
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH);
    count = models.IntegerField();

    def login(self, user, password):
        list_of_matching_users = UsersModel.objects.filter(user=user, password=password);
        if (list_of_matching_users.count() == 0):
            return UsersModel.ERR_BAD_CREDENTIALS;
        else:
            temp_user = list_of_matching_users.get(user=user, password=password);
            temp_count = temp_user.count + 1;
            temp_user.count = temp_count;
            temp_user.save();
            return temp_count;


    def add(self, user, password):
        #import pdb; pdb.set_trace()
        list_of_matching_users = UsersModel.objects.filter(user=user);
        if (list_of_matching_users.count() != 0):
            return UsersModel.ERR_USER_EXISTS;
        else:
            def valid_username(username):
                return username != "" and len(username) <= UsersModel.MAX_USERNAME_LENGTH;

            def valid_password(password):
                return len(password) <= UsersModel.MAX_PASSWORD_LENGTH;

            if not valid_username(user):
                return UsersModel.ERR_BAD_USERNAME
            if not valid_password(password):
                return UsersModel.ERR_BAD_PASSWORD

            new_user = UsersModel(user=user, password=password,count=1);
            new_user.save();
            return new_user.count;


    def TESTAPI_resetFixture(self):
        try:
            UsersModel.objects.all().delete();
        finally:
            return UsersModel.SUCCESS;
