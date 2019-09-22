$(document).ready(function () {
    var input = $(".maskmoney").maskMoney({thousands: ",", decimal: ".", suffix: "€", allowZero: true});
    loadIngredients();
})

$('#newIngredient').click(function() {
    clearIngredientModal();
    $('#ingredientModal').modal('show');
})

$('#saveNewIngredient').click(function() {
    if ($('#ingredient-name').val() == '') {
        alertify.warning('Please write a title.');
        $('#ingredient-name').focus();
        return;
    }

    if ($('#ingredient-measure').val() == '') {
        alertify.warning('Please select a measure unity.');
        $('#ingredient-measure').focus();
        return;
    }

    $('#ingredientModal').modal('hide');
    saveIngredient();
})

$('#igredientsTable').on('click','.edit_ingredient',function() {
    data = JSON.parse($(this).parent().parent().attr('data'));
    
    $('#ingredient-id').val(data.id);
    $('#ingredient-name').val(data.title);
    $('#ingredient-description').val(data.description);
    $('#ingredient-price').val(data.price).maskMoney('mask');
    $('#ingredient-measure').val(data.measureUnit);
    $('#ingredient-ammount').val(data.ammount);

    $('#ingredientModal').modal('show');
})

$('#igredientsTable').on('click','.delete_ingredient',function() {
    data = JSON.parse($(this).parent().parent().attr('data'));
    deleteIngredient(data.id);
})

function loadIngredients() {
    $.post('list', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
    }, function (ret) {
        if (ret.code == 1) {
            dataTableRecipeManager('igredientsTable', ret.html, {})
            alertify.success(ret.msg);
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}

function clearIngredientModal() {
    $('#ingredient-id').val(0);
    $('#ingredient-name').val('');
    $('#ingredient-description').val('');
    $('#ingredient-price').val(0.00).maskMoney('mask');
    $('#ingredient-measure').val('');
    $('#ingredient-ammount').val(1);
}

function saveIngredient() {
    $.post('save', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
        'id': $('#ingredient-id').val(),
        'title': $('#ingredient-name').val(),
        'description': $('#ingredient-description').val(),
        'price': $('#ingredient-price').maskMoney('unmasked')[0],
        'measureUnit': $('#ingredient-measure').val(),
        'ammount': $('#ingredient-ammount').val(),
    }, function (ret) {
        if (ret.code == 1) {
            alertify.success(ret.msg);
            loadIngredients();
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}

function deleteIngredient(id) {
    $.post('delete', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
        'id': id,
    }, function (ret) {
        if (ret.code == 1) {
            alertify.success(ret.msg);
            loadIngredients();
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}