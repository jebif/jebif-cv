$(document).ready(function(){
    // Set ``daterangepicker`` widget for creation date field
    $('#id_available_on').focus(function () {
        if($('.ui-daterangepickercontain').length == 0){
            fr_settings = $.daterangepicker_fr.settings;
            fr_settings['posX'] = $(this).offset().left;
            fr_settings['posY'] = $(this).offset().top + $('#id_available_on').height() + 12;
            $('#id_available_on').daterangepicker(fr_settings);
        }
    });

    // Set ``autocomplete`` widget for metadata fields
    var name_choices = $('[name="keyword"]').attr('choices').split(';');
    $('[name="keyword"]').autocomplete(name_choices);
});
