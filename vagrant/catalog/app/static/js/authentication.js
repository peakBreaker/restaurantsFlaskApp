

window.fbAsyncInit = function() {
  FB.init({
    appId      : '135973793632108',
    cookie     : true,
    xfbml      : true,
    version    : 'v2.8'
  });
  FB.AppEvents.logPageView();
};
// Load the fb sdk asynchronously
(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = "//connect.facebook.net/en_US/sdk.js";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));


// Here we run a very simple test of the Graph API after login is
// successful.  See statusChangeCallback() for when this call is made.
function sendTokenToServer() {
 var access_token = FB.getAuthResponse()['accessToken'];
 console.log(access_token)
 console.log('Welcome!  Fetching your information.... ');
 FB.api('/me', function(response) {
   console.log('Successful login for: ' + response.name);
  $.ajax({ // This is the ajax which logins to our app
   type: 'POST',
   url: furl,
   processData: false,
   data: access_token,
   contentType: 'application/octet-stream; charset=utf-8',
   success: function(result) {
     // Handle or verify the server response if necessary.
     if (result) {
       $('#result').html('Login Successful!</br>'+ result + '</br>Redirecting...')
      setTimeout(function() {
       window.location.href = "/restaurants";
      }, 4000);

   } else {
     $('#result').html('Failed to make a server-side call. Check your configuration and console.');
      }
   }

});
 });
}

function signInCallback(authResult) {
  if (authResult['code']) {
    // Hide the sign-in button now that the user is authorized
    $('#signinButton').attr('style', 'display: none');
    // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
    $.ajax({
      type: 'POST',
      url: gurl,
      processData: false,
      data: authResult['code'],
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        // Handle or verify the server response if necessary.
        if (result) {
          $('#result').html('Login Successful!</br>'+ result + '</br>Redirecting...')
         setTimeout(function() {
          window.location.href = "/restaurants";
         }, 4000);

      } else if (authResult['error']) {
    console.log('There was an error: ' + authResult['error']);
  } else {
        $('#result').html('Failed to make a server-side call. Check your configuration and console.');
         }
      }

  }); } }
