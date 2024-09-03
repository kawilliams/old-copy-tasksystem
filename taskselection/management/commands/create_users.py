from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import sys
import csv

User = get_user_model()

class Command(BaseCommand):
  help = 'Creates new users in the db for the given csv file'

  def add_arguments(self, parser):
    parser.add_argument('users', type=str)
    parser.add_argument('--clear', dest='clear_users', default=False, action='store_true')


  def handle(self, *args, **options):
    if options['clear_users']:
      print('Setting --clear will delete all users (except superusers) from the database.')
      ans = input('Is this ok? (Y/N) ')
      if ans =='Y':
        print('Deleting all users')
        User.objects.filter(is_superuser=False).delete()
    
    with open(options['users'], 'r', encoding='utf-8-sig') as csvfile:
      csvreader = csv.DictReader(csvfile, delimiter=',')
      # if this doesn't work the delimiter might be wrong
      for row in csvreader:
        try:
          print(row)
          user = User.objects.create_user(username=row['username'], 
                                          email=row['username'], 
                                          first_name=row['firstname'], 
                                          last_name=row['lastname'])
          user.set_password(row['password'])
          user.save()

          assert authenticate(username=row['username'], password=row['password'])
          self.stdout.write("User {0} successfully created.".format(row['username']))
        except:
          print('There was a problem creating the user: {0}.  Error: {1}.' \
                .format(row['username'], sys.exc_info()[1]))



