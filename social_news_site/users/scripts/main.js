// Форма авторизации
$('#login__form').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: this.method,
        url: this.action,
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response) {

            window.location.reload();
        },
        error: function(response) {

            const modal__errors = $('.modal__errors');
            modal__errors.addClass('active');
            modal__errors.text(response.responseJSON.detail);
        },

    });
});

// Форма Регистрации
$('#register__form').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: this.method,
        url: this.action,
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response) {
            window.location.href = '/'
        },
        error: function(response) {

            //console.log(response.responseJSON.username);
            $('.form__input').css({'border': 'none', 'border-bottom': '1px solid #999'});
            $('.form__error').text('');

            for (el in response.responseJSON) {
                $(`.form__input.${el}`).css('border', '1px solid red');
                $(`.form__error.${el}`).text(response.responseJSON[el][0]);
                
            }
            
        },

    });
});


// Взаимодействие с модальным окном регистрации
const modal_signup = $('.modal__signup');
const btn_signup = $('.signup');
const modal__signup_close = $('.modal__signup__close');

btn_signup.click(() => modal_signup.addClass('active'));

modal__signup_close.click(() => modal_signup.removeClass('active'));

// Взаимодействие с модальным окном авторизации
const modal_signin = $('.modal__signin');
const btn_signin = $('.signin');
const modal__signin_close = $('.modal__signin__close');

btn_signin.click(() => modal_signin.addClass('active'));

modal__signin_close.click(() => modal_signin.removeClass('active'));


// Изменение фото в профиле
$('#id_photo').css('visibility', 'collapse');
$('.profile__change__photo__button').click((e) => {
    e.preventDefault();

    $('#id_photo').click();

    $('#id_photo').change(() => {
        $('#change_photo').submit();
    });

});


// создание темы
$('.create__theme').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: this.method,
        url: this.action,
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response) {
            // console.log(response)
            window.location.href = response.theme
        },
        error: function(response) {

            for (el in response.responseJSON) {

                $(`.create__${el}__error`).text(response.responseJSON[el])

                $(`.create__${el}`).css('border', '1px solid #c20000')
            }
            
        },

    });
});


// Форма смены пароля
// $('.edit__password__content').submit(function(e) {
//     e.preventDefault();
//     $.ajax({
//         type: this.method,
//         url: this.action,
//         data: $(this).serialize(),
//         dataType: 'json',
//         success: function(response) {
//             console.log(response)
//         },
//         error: function(response) {

//             console.log(response)

//             // for (el in response.responseJSON) {
//             //     console.log(el)   
//             // }
            
//         },

//     });
// });