import users_mgt as um

um.create_user_table()
um.add_user('testuser', 'test1', 'test1@test.com')
um.show_users()
