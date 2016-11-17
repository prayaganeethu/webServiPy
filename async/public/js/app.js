$(document).ready(function() {
     var lock = new Auth0LockPasswordless(AUTH0_CLIENT_ID, AUTH0_DOMAIN, {
        auth: {
          redirectUrl: AUTH0_CALLBACK_URL
        }
     });

    $('.btn-login').click(function(e) {
      e.preventDefault();
        lock.sms({callbackURL: AUTH0_CALLBACK_URL});
    });
});
