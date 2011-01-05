/*

Photolog GAE app helper javascript

Version 1.0.0

Authors:
	Jaehong Park

*/
function deleteNode(key)
{
    $.post("/delete",
        { gkey: key },
        function(data){
            location.replace("/");
        });
}

function get_children(key)
{
    $.get('/list', 
            {pkey: key,type : 'stitch'},
            function(data) {
            $('#children').html(data);
                $('.child_item_div').fadeIn('slow');
        });
}