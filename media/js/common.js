$(document).ready(function() {
    /* Hide info msg after 4 sec. */
    if($(".info_msg").length > 0){
        setTimeout(function(){
            $(".info_msg").effect('blind','normal');
        }, 4000);
    }
    
    /* Display a confirmation box on ``delete`` */
    $('.confirm').click(function(){
        return confirm(gettext("Etes-vous sûr?"));
    });
});
