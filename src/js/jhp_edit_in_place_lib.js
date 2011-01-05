/*

Photolog GAE app helper javascript

Version 1.0.0

Authors:
	Jaehong Park

*/
function setClickable(id_editable) 
{
		
    if(id_editable=="editInPlaceTitle")
    {
        $("#"+id_editable).editInPlace({
            default_text: "(Click to add title)",
            url: '/update',
            params: 'target=title&gkey='+$('meta[name=key]').attr("content"),
            success: function(data){;}
        });
		
    }
    else if(id_editable=="editInPlaceTextBox")
    {
        $("#"+id_editable).editInPlace({
            default_text: "(Click to add Description)",
            field_type: "textarea",
            url: '/update',
            params: 'target=desc&gkey='+$('meta[name=key]').attr("content"),
            //show_buttons: true,
            success: function(data){;}
        });
			
    }
    else
    {
        $("."+id_editable).editInPlace({
            default_text: "(Click to add Tags)",
            url: '/update',
            params: 'target=tags&gkey='+$('meta[name=key]').attr("content"),
            success: function(data){ ;}
        });
    }

}


function setClickableEx(id_editable) 
{
		
			if(id_editable=="editInPlaceTitle")
			{
				$("#"+id_editable).editInPlace({
					default_text: "(Click to add title)",
					url: '/update',
					params: 'target=title&gkey='+$('#gkey').val(),
					success: function(data){;}
				});
		
			}
			else if(id_editable=="editInPlaceTextBox")
			{
				$("#"+id_editable).editInPlace({
					default_text: "(Click to add Description)",
					field_type: "textarea",
					textarea_rows: "20",
					textarea_cols: "40", 
					url: '/updates',
					params: 'target=desc&gkey='+$('#gkey').val(),
					//show_buttons: true,
					success: function(data){;}
				});
			
			}
			else
			{
				$("#"+id_editable).editInPlace({
					default_text: "(Click to add Tags)",
					url: '/update',
					params: 'target=tags&gkey='+$('#gkey').val(),
					success: function(data){ ;}
				});
			}

}