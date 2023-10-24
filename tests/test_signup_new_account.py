

def test_signup_new_account(app):
    username = "adm"
    password = "nopassword"
    app.james.make_shure_user_exist(username, password)
