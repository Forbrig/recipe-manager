$(document).ready(function() {
    // console.log('it worked');
    $('.nav-link').click(function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
    })
})

function dataTableRecipeManager(id_tabela, content, options) {
    if ($('#'+id_tabela).attr('data-table-created') == "true") {
        $('#'+id_tabela).DataTable().destroy();
    }
    
    $('#'+id_tabela+' tbody').html(content);
    if (content != "") {
        if (options.lengthMenu != undefined) {
            options.lengthMenu[0].push(-1);
            options.lengthMenu[1].push("All");
        }
        options.lengthMenu = (options.lengthMenu == undefined ? [[10, 50, 100, 500, -1],[10, 50, 100, 500, "All"]] : options.lengthMenu);
        options.sortable = (options.sortable == undefined ? false : options.sortable);
        options.retrieve = true;

        $('#'+id_tabela).DataTable(options);
        $('#'+id_tabela).attr('data-table-created', "true");
    }
}