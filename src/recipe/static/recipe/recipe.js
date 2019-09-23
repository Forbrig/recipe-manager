$(document).ready(function () {
    var input = $(".maskmoney").maskMoney({thousands: ",", decimal: ".", suffix: "€", allowZero: true});
    loadRecipes();
})

$('#newRecipe').click(function() {
    clearRecipeModal();
    $('#recipeModal').modal('show');
})

$('#addNewRecipeIngredient').click(function() {
    clearRecipeIngredientModal();
    $('#recipeModal').modal('hide');
    $('#recipeIngredientModal').modal('show');
})

$('#recipeIngredientModal').on('hidden.bs.modal', function() {
    $('#recipeModal').modal('show');
})

$('#recipeModal').on('hidden.bs.modal', function() {
    loadRecipes();
})

$('#showRecipeIngredientSearch').click(function() {
    $('.ingredientSearch').toggle();
    $("#autocomplete_ingredients").focus();
})

$('#saveNewRecipe').click(function() {
    if ($('#recipe-name').val() == '') {
        alertify.warning('Please write a name for the recipe.');
        $('#recipe-name').focus();
        return;
    }
    // $('#ingredientModal').modal('hide');
    saveRecipe();
})

$('#addRecipeIngredient').click(function() {
    if ($('#ingredient-id').val() == 0) {
        alertify.warning('No ingredient selected.');
        return;
    }
    saveRecipeIngredient();
    $('#recipeIngredientModal').modal('hide');
    $('#recipeModal').modal('show');
})


$('#recipesTable').on('click','.edit_recipe',function() {
    data = JSON.parse($(this).parent().parent().attr('data'));
    
    $('#recipe-id').val(data.id);
    $('#recipe-name').val(data.name);
    $('#recipe-description').val(data.description);
    $('#recipe-preparation').val(data.preparation);
    loadRecipeIngredients();
    $('#recipeModal').modal('show');
})

$('#recipesTable').on('click','.delete_recipe',function() {
    data = JSON.parse($(this).parent().parent().attr('data'));
    
    bootbox.confirm({
        title: "Delete recipe",
        message: "Are you sure you want to delete this recipe?",
        buttons: {
            confirm: {
                label: "<i class='fa fa-trash-alt'></i> Confirm",
                className: 'btn-danger'
            },
            cancel: {
                label: "<i class='fa fa-arrow-left'></i> Cancel",
                className: 'btn-secondary'
            }
        },
        callback: function (result) {
            if (result == true) {
                deleteRecipe(data.id);
            }
        }
    });
})

$('#recipeIngredientsTable').on('click','.delete_recipe_ingredient',function() {
    data = JSON.parse($(this).parent().parent().attr('data'));

    $('#recipeModal').modal('hide');
    bootbox.confirm({
        title: "Remove ingredient from recipe",
        message: "Are you sure you want to remove this ingredient from the recipe?",
        buttons: {
            confirm: {
                label: "<i class='fa fa-trash-alt'></i> Confirm",
                className: 'btn-danger'
            },
            cancel: {
                label: "<i class='fa fa-arrow-left'></i> Cancel",
                className: 'btn-secondary'
            }
        },
        callback: function (result) {
            if (result == true) {
                deleteRecipeIngredient(data.id);
            }
            $('#recipeModal').modal('show');
        }
    });
})

$('#recipeIngredientsTable').on('click','.edit_recipe_ingredient',function() {
    data = JSON.parse($(this).parent().parent().attr('data'));

    $('#recipeModal').modal('hide');

    // {"id": 9, "recipe_id": 3, "ingredient_id": 4, "ammount": 500, "measureUnit": "", "price": "0.50", "name": "Carrot"}

    $('#ingredient-id').val(data.ingredient_id);
    $('#ingredient-recipe-name').val(data.name);
    $('#ingredient-recipe-measure').val(data.measureUnit);
    $('#ingredient-recipe-ammount').val(data.ammount);
    $('#ingredient-recipe-price').val(data.price).maskMoney('mask');

    $('#recipeIngredientModal').modal('show');
    
})

function loadRecipes() {
    $.post('../recipe_list', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
    }, function (ret) {
        if (ret.code == 1) {
            dataTableRecipeManager('recipesTable', ret.html, {})
            alertify.success(ret.msg);
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}

function clearRecipeModal() {
    $('#recipe-id').val(0);
    $('#recipe-name').val('');
    $('#recipe-description').val('');
    $('#recipe-preparation').val('');
    $('#recipe-price').val('0.00').maskMoney('mask');
    $('#recipeIngredientsDiv').hide();
}

function clearRecipeIngredientModal() {
    $('#ingredient-id').val(0);
    $('#ingredient-recipe-name').val('').show();
    $('#autocomplete_ingredients').val('').hide();
    $('#ingredient-recipe-measure').val('');
    $('#ingredient-recipe-ammount').val('');
    $('#ingredient-recipe-price').val('0.00').maskMoney('mask');
}

function saveRecipe() {
    $.post('../recipe_save', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
        'id': $('#recipe-id').val(),
        'name': $('#recipe-name').val(),
        'description': $('#recipe-description').val(),
        'preparation': $('#recipe-preparation').val(),
    }, function (ret) {
        if (ret.code == 1) {
            alertify.success(ret.msg);
            $('#recipeIngredientsDiv').show();
            // loadRecipes();
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}

function deleteRecipeIngredient(id) {
    $.post('../recipe_ingredient_delete', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
        'id': id,
    }, function (ret) {
        if (ret.code == 1) {
            alertify.success(ret.msg);
            loadRecipeIngredients();
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}

$('#ingredient-recipe-ammount').change(function() {
    if ($('#ingredient-id').val() > 0 && $('#ingredient-recipe-ammount').val() > 0) {
        recalculateIngredientPrice();
    }
});

// recalculate the price based on ammount
function recalculateIngredientPrice() {
    newAmmount = $('#ingredient-recipe-ammount').val();
    basePrice = $('#ingredient-recipe-price').attr('data-price');
    baseAmmount = $('#ingredient-recipe-price').attr('data-ammount');
    newPrice = parseFloat(basePrice * newAmmount / baseAmmount).toFixed(2);

    $('#ingredient-recipe-price').val(newPrice).maskMoney('mask');
}

// autocomplete of the recipe ingredients
$(function () {
    $("#autocomplete_ingredients").bind("keydown", function (event) {
            $('#ingredient-id').val(0);
        }).autocomplete({
            minLength: 1,
            source: function (request, response) {
                $.getJSON("../autocomplete_ingredients", {
                    term: request.term,
                }, response);
            },
            select: function (event, ui) {
                this.value = ui.item.label;
                $('#ingredient-id').val(ui.item.id)
                $('#ingredient-recipe-name').val(ui.item.label);
                $('#ingredient-recipe-measure').val(ui.item.measure);
                $('#ingredient-recipe-ammount').val(ui.item.ammount);
                $('#ingredient-recipe-price').val(ui.item.price).maskMoney('mask');

                // save the price per ammount and measure to calculate the new price if the ammount or the measure change
                $('#ingredient-recipe-price').attr('data-price', ui.item.price);
                $('#ingredient-recipe-price').attr('data-measure', ui.item.measure);
                $('#ingredient-recipe-price').attr('data-ammount', ui.item.ammount);
                $('.ingredientSearch').toggle(); // hide autocomplete again
                return false;
            }
        });
});

function loadRecipeIngredients() {
    $.post('../recipe_ingredients_load', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
        'id': $('#recipe-id').val(),
    }, function (ret) {
        if (ret.code == 1) {
            alertify.success(ret.msg);
            dataTableRecipeManager('recipeIngredientsTable', ret.html, {})
            $('#recipe-price').val(ret.totalRecipePrice).maskMoney('mask');
            $('#recipeIngredientsDiv').show();
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}

function saveRecipeIngredient() {
    $.post('../recipe_ingredient_save', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
        'recipe': $('#recipe-id').val(),
        'ingredient': $('#ingredient-id').val(),
        'ammount': $('#ingredient-recipe-ammount').val(),
        'measureUnit': $('#ingredient-recipe-measure').val(),
    }, function (ret) {
        if (ret.code == 1) {
            alertify.success(ret.msg);
            $('#recipeIngredientsDiv').show();
            loadRecipeIngredients();
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}

function deleteRecipe(id) {
    $.post('../recipe_delete', {
        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
        'id': id,
    }, function (ret) {
        if (ret.code == 1) {
            alertify.success(ret.msg);
            loadRecipes();
        } else {
            console.log(ret);
            alertify.warning(ret.msg);
        }
    })
}
