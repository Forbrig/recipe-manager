$(document).ready(function () {
    console.log('it works');

    //Buttons examples
    var table = $('#datatable-buttons').DataTable({
        lengthChange: false,
        buttons: ['copy', 'excel', 'pdf']
    });

    // table.buttons().container().appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');

    loadIngredients();
})

function loadIngredients() {
    $.post('ingredients/',{
        'csfrmiddlewaretoken': $('#csfrmiddlewaretoken').val(),
        'action': 'GET_ALL_INGREDIENTS',
    }, function (retorno) {
        ret = JSON.parse(retorno);
        console.log(ret);
        
        // if (ret.code == 1) {
        //     $('#ingredients_table_body').html(ret.html);
        //     console.log('success')
        //     // alertify.success(ret.msg);
        // } else {
        //     console.log(ret);
        //     // alertify.warning(ret.msg);
        // }
    })
}

function saveNewIngredient(params) {
    
}