/* French initialisation for the jQuery UI date range picker plugin. */

(function($){
    $.daterangepicker_fr = {
        settings : {
            // presetRanges: array of objects for each menu preset.
            // Each obj must have text, dateStart, dateEnd. dateStart, dateEnd accept
            // date.js string or a function which returns a date object
            presetRanges: [
                // {
                //     text: "Aujourd'hui",
                //     dateStart: 'today',
                //     dateEnd: 'today'
                // },
                // {
                //     text: 'Cette semaine',
                //     dateStart: 'today-7days',
                //     dateEnd: 'today'
                // }
                // {
                //     text: 'Depuis le début du mois',
                //     dateStart: function(){
                //         return Date.parse('today').moveToFirstDayOfMonth();
                //     },
                //     dateEnd: 'today'
                // },
                // {
                //                     text: "Cette année",
                //                     dateStart: function(){
                //                         var x= Date.parse('today');
                //                         x.setMonth(0);
                //                         x.setDate(1);
                //                         return x;
                //                     },
                //                     dateEnd: 'today'
                //                 }
            ],
            presets: {
                allDatesAfter: 'A partir du ...',
                allDatesBefore: 'Avant le ...',
                specificDate: 'Date précise',
                dateRange: 'Période'
            },
            rangeStartTitle: 'Date de début',
            rangeEndTitle: 'Date de fin',
            nextLinkText: 'Suivant',
            prevLinkText: 'Précédent',
            doneButtonText: 'Valider',
            posX: null,
            posY: null,
            dateFormat: 'dd/mm/yy',
            datepickerOptions: $.datepicker.regional['fr']
        }
    };
})(jQuery);
