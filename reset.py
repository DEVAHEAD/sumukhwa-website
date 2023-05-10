import os

if __name__=='__main__':
    userapp_cache_dir='UserApp\\__pycache__\\'
    userapp_migration_dir='UserApp\\migrations\\'
    art_generator_cache_dir='art_generator\\__pycache__\\'
    art_generator_migration_dir='art_generator\\migrations\\'
    media='media'
    db_file='db.sqlite3'


    try:
        for file in os.listdir(userapp_cache_dir):
            os.remove(os.path.join(userapp_cache_dir,file))

        for file in os.listdir(userapp_migration_dir):
            if os.path.isfile(os.path.join(userapp_migration_dir,file)) and file!="__init__.py":
                os.remove(os.path.join(userapp_migration_dir,file))


        for file in os.listdir(art_generator_cache_dir):
            os.remove(os.path.join(art_generator_cache_dir,file))

        for file in os.listdir(art_generator_migration_dir):
            if os.path.isfile(os.path.join(art_generator_migration_dir,file)) and file!="__init__.py":
                os.remove(os.path.join(art_generator_migration_dir,file))
    except:
        print("!!!!!!!!!!!!!!!!!!!!something wrong with deleting migration and cache")
    try:
        for file in os.listdir(media):
            if os.path.isfile(os.path.join(media,file)):
                os.remove(os.path.join(media,file))
            else:
                os.rmdir(os.path.join(media,file))
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!something wrong with deleting media")
    try:
        os.remove(db_file)
    except:
        pass

    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    os.system('python manage.py runserver')