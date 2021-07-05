print("Do you really want to reset database? (Y)")
confirm = input()
if confirm == 'Y':
    from bollards_api import db
    from bollards_api.models import User, Bollard
    db.drop_all()
    db.create_all()
    default_user = User(username='jma', password='password')
    print('Users:')
    print(User.query.all())
    print('Bollards:')
    print(Bollard.query.all())
