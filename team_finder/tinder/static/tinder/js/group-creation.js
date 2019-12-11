const passwordBox = $('#password-box');

$(() => {
   if ($("#id_private").is(':checked')){
       passwordBox.show();
   }
});
$("#id_private").change(() => {
    passwordBox.toggle();
});