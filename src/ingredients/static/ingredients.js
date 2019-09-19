$(document).ready(function () {
    console.log('it works');

    //Buttons examples
    var table = $('#datatable-buttons').DataTable({
        lengthChange: false,
        buttons: ['copy', 'excel', 'pdf']
    });

    var input = $(".maskmoney").maskMoney({thousands: ",", decimal: ".", suffix: " €"});
    input.maskMoney('mask', 0.00);

    // table.buttons().container().appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');

    loadIngredients();

    
})

$('#newIngredient').click(function() {
    console.log('newIngredient');
    
    $('#ingredientModal').modal('show');
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