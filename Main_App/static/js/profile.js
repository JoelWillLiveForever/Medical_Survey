// var form;

function showModalWin(analysis_id) {
    var darkLayer = document.createElement('div'); // слой затемнения
    darkLayer.id = 'shadow'; // id чтобы подхватить стиль
    document.body.appendChild(darkLayer); // включаем затемнение

    var modalWin = document.getElementById('popup' + analysis_id); // находим наше "окно"
    modalWin.style.display = 'unset'; // "включаем" его

    darkLayer.onclick = function () {  // при клике на слой затемнения все исчезнет
        darkLayer.parentNode.removeChild(darkLayer); // удаляем затемнение
        modalWin.style.display = 'none'; // делаем окно невидимым
        return false;
    };
}


// ХЗ
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// wrap request in a function:
function send_typeNtoken(type) {
    console.log(type)

    const csrftoken = getCookie('csrftoken');

    $.ajax({
    url : 'profile',
    data : {
        'csrfmiddlewaretoken' : csrftoken,
        'type' : type,
    },
    method : 'POST'});
}
// https://stackoverflow.com/questions/65309532/how-to-pass-data-from-ajax-to-django-view

// function proceed() {
//     // if (form != null)
//     // {
//     //     form = document.createElement('form');

//     //     form.setAttribute('method', 'post');
//     //     form.style.display = 'hidden';

//     //     document.body.appendChild(form)
//     // }

//     var form = document.createElement('form');

//     form.setAttribute('method', 'post');
//     form.style.display = 'hidden';

//     document.body.appendChild(form)

//     form.submit();
// }