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