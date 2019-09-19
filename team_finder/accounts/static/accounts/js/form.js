var REG_CONJ = $("#register_field");
var REG_FIELD = $("#id_register");
var COURSE_SELECT = $("#id_course");
var MODAL_CHOICE = $("#modals_choice");
var IS_STUDENT = $("#id_is_student");

var TOTAL = {
    value : 0,
    add_value : function(val) {
        this.value = this.value + val;
        $("#valorfinal").html("Valor da inscrição:<br>R$"+this.value+",00");
    },
    remove_value : function(val) {
        this.value = this.value - val;
        $("#valorfinal").html("Valor da inscrição:<br>R$"+this.value+",00");
    },
    set_value(val){
	this.value = val;
},
};

var studentCalendar = {
    seg : [false],
    ter : [false,false],
    qua : [false,false],
    qui : [false,false],
    sex : [false,false],

    is_valid(){
        if (this.seg[0] &&
            this.ter[0] && this.ter[1] &&
            this.qua[0] && this.qua[1] &&
            this.qui[0] && this.qui[1] &&
            this.sex[0] && this.sex[1]) {
            $("#btnregister").attr("disabled", false);
        } else {
            $("#btnregister").attr("disabled", true);
        }
    },

    add_lecture(day, hour, hourf) {
        if (hour == "19:30" && hourf == "20:30"){
            this[day][0] = true;
        } else if (hour == "19:30" && hourf == "22:00"){
            this[day][0] = true;
            this[day][1] = true;
        } else if (hour == "21:00" && hourf == "22:00"){
            this[day][1] = true;
        } else if (hour == "19:00" && hourf == "22:00") {
	    this[day][0] = true;
            this[day][1] = true;
	}
    },

    remove_lecture(day, hour, hourf) {
        if (hour == "19:30" && hourf == "20:30"){
            this[day][0] = false;
	} else if (hour == "19:30" && hourf == "22:00"){
            this[day][0] = false;
            this[day][1] = false;
        } else if (hour == "21:00" && hourf == "22:00"){
            this[day][1] = false;
        } else if (hour == "19:00" && hourf == "22:00") {
	    this[day][0] = false;
            this[day][1] = false;
	} 
    }
};

//init
$(function() {
    block();
    if (!REG_CONJ.is(":checked")) {
        REG_CONJ.hide();
        MODAL_CHOICE.hide();
        $("#valorfinal").html("Valor da inscrição:<br>R$20,00");
    };
});

IS_STUDENT.change(function() {
    REG_CONJ.toggle();
    MODAL_CHOICE.toggle();
    $('#ul1').tabs('select', 'lecturestab');
    if ($(this).is(":checked")) {
        REG_FIELD.attr('required', true);
        COURSE_SELECT.attr('required', true);
        TOTAL.remove_value(5);
        studentCalendar.is_valid();
        $("#btnregister").attr("disabled",true);
    } else {
        REG_FIELD.attr('required', false);
        COURSE_SELECT.attr('required', false);
        TOTAL.add_value(5);
        $("#btnregister").attr("disabled",false);
        $("input").prop("checked", false);
        $("input").attr("disabled", false);
        $("tr").css('color', 'black');
    }
});

function validateStudent() {
    if (IS_STUDENT.is(":checked")) {
        studentCalendar.is_valid();
    }
}

$("input[name='lectures']").change(function () {

    var dayInWeek = $(this).closest("div").attr("data-day");
    var dayConj = $("div[data-day='" + dayInWeek + "'] tbody tr");
    var tr = $(this).closest("tr");

    //Remove a palestra selecionada da lista
    dayConj = $($.grep(dayConj, function (n) {
        return $(n)[0] !== tr[0];
    }));


    var hour = $(this).closest("tr").find(".hour").text().split(" - ");
    var hourInit = hour[0];
    var hourFinal = hour[1];

    if ($(this).is(":checked")) {
        studentCalendar.add_lecture(dayInWeek,hourInit,hourFinal);
        dayConj.each(function() {
            var siblingHour = $(this).find(".hour").text().split(" - ");

            var siblingInit = siblingHour[0];
            var siblingFinal = siblingHour[1];

            if ((hourInit <= siblingInit) && (siblingInit <= hourFinal) || (siblingInit <= hourFinal && hourFinal <= siblingFinal)) {
                $(this).find("input").attr('disabled', true);
                $(this).css('color', 'lightgrey');
            }
        });
    } else {
        studentCalendar.remove_lecture(dayInWeek,hourInit, hourFinal);
        dayConj.each(function () {
            var siblingHour = $(this).find(".hour").text().split(" - ");

            var siblingInit = siblingHour[0];
            var siblingFinal = siblingHour[1];

            if ((hourInit <= siblingInit) && (siblingInit <= hourFinal) || (siblingInit <= hourFinal && hourFinal <= siblingFinal)) {
                $(this).find("input").attr('disabled', false);
                $(this).css('color', 'black');
            }
        });
	check_value();
    }
    
    if (REG_FIELD.is(":visible")) {
        studentCalendar.is_valid();
    }
});

$("#btnregister").click(function(){
    check_value();
});

// verificação pós f5
function block () {
    $("input[name='lectures']:checked").each(function(){
	
        var dayInWeek = $(this).closest("div").attr("data-day");
        var dayConj = $("div[data-day='" + dayInWeek + "'] tbody tr");
        var tr = $(this).closest("tr");

        //Remove a palestra selecionada da lista
        dayConj = $($.grep(dayConj, function (n) {
            return $(n)[0] !== tr[0];
        }));


        var hour = $(this).closest("tr").find(".hour").text().split(" - ");
        var hourInit = hour[0];
        var hourFinal = hour[1];
        var validat = $(this).closest("tr").find("#costvalue").text().substr(2,3);
        if (validat == "") {
            validat = 0;
        }

        if ($(this).is(":checked")) {
            studentCalendar.add_lecture(dayInWeek,hourInit,hourFinal);
            dayConj.each(function() {
                var siblingHour = $(this).find(".hour").text().split(" - ");

                var siblingInit = siblingHour[0];
                var siblingFinal = siblingHour[1];

                if ((hourInit <= siblingInit) && (siblingInit <= hourFinal) || (siblingInit <= hourFinal && hourFinal <= siblingFinal)) {
                    $(this).find("input").attr('disabled', true);
                    $(this).css('color', 'lightgrey');
                }
            });
        } else {
            studentCalendar.remove_lecture(dayInWeek,hourInit, hourFinal);
            dayConj.each(function () {
                var siblingHour = $(this).find(".hour").text().split(" - ");

                var siblingInit = siblingHour[0];
                var siblingFinal = siblingHour[1];

                if ((hourInit <= siblingInit) && (siblingInit <= hourFinal) || (siblingInit <= hourFinal && hourFinal <= siblingFinal)) {
                    $(this).find("input").attr('disabled', false);
                    $(this).css('color', 'black');
                }
            });
        }

        if (REG_FIELD.is(":visible")) {
            studentCalendar.is_valid();
        }
    });
}
//

//Verificando o valor
function check_value () {
	TOTAL.value = 0;
	var cost_init;
	if ($("#studentYN").text() == "True " || IS_STUDENT.is(":checked")) {
		cost_init = 15;
	} else {
		cost_init = 20;
	};

    checados = $("input[name='lectures']:checked");
    
    if (checados.length == 1 && $(checados[0]).closest("tr").find(".lectitle").text() == "Abertura Semana Acadêmica - Potencializando o aprender: possibilidades a partir da disciplina intelectual") {
        cost_init = 0;
    };

	TOTAL.add_value(cost_init);
    checados.each(function() {

        var dayInWeek2 = $(this).closest("div").attr("data-day");
        var dayConj2 = $("div[data-day='" + dayInWeek2 + "'] tbody tr");
        var tr2 = $(this).closest("tr");

        //Remove a palestra selecionada da lista
        dayConj2 = $($.grep(dayConj2, function (n) {
            return $(n)[0] !== tr2[0];
        }));

        var validat = $(this).closest("tr").find("#costvalue").text().substr(2,3);
        if (validat == "") {
            validat = 0;
        }

        TOTAL.add_value(parseInt(validat));

    });
};
//
