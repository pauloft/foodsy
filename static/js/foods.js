/* Javascript code for Food Nutrients app */
$(document).ready(function() {
 
    $('#foodSearchForm').on('submit', function(event){
        $('#output').text("Searching the database. Please wait...").show();

        $.ajax({
            type: 'POST',
            url: '/lookup',
            data: { 'searchText': $('#searchText').val() },
            dataType: 'JSON'
        })
        .done(function(data){
            if (data.food_list && data.results) {
                
                var res = "";
                var num_cols = data.food_list.length;
                var div_width = Math.floor(12/(num_cols));
                var col_class = "col-md-"+div_width;
                for (i=0; i<num_cols; i++) {
                    res += "<div class="+col_class+">";
                    res += "<h3 class='capitalize-food-name'><u>" + data.food_list[i] + "</u></h3>";
                    res += "<h4>Food Groups</h4><ul>";

                    var food = data.results[ data.food_list[i] ];
                    for (g=0; g<food['food_groups'].length; g++) {
                        res += "<li>" + food['food_groups'][g] + "</li>";
                    }
                    res += "</ul>";
                    // end food groups

                    // display manufacturer select options

                    res += "</div>";
                }
                
                $('#output').html(res);
            } else {
                $('#output').text(data.error).show();
            }
        });
        event.preventDefault();
    });
});