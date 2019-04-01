import pickle
import os

# if new installation, create a global user table to keep track of all users and their notebooks
# first user, username: admin, password: secret
# can add permission settings for different notebooks

def create_new_user_table():
	
	if (user_table_exists()):
		return False

	fileObject = open("USERTABLE", "wb")

	newTable =  [
					{
						"username": "admin",
						"password": "secret",
						"notebooks": []
					}
				]


	pickle.dump(newTable, fileObject)

	fileObject.close()

	return True

# check whether the global user table exists

def user_table_exists():
	return os.path.exists("USERTABLE")