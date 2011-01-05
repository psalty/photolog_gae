/*

Photolog GAE app helper javascript

Version 1.0.0

Authors:
	Jaehong Park

*/

function uploadWebCam(addr) 
{
    if($('#gkey').val())
        pkey = $('#gkey').val();
        
    getSWF('uploadmod').FlexSubmit(addr);
}

function post(obj)
{
    $.post('/create', $('#imageform').serialize());
}


function getSWF(movieName) 
{
    if (navigator.appName.indexOf("Microsoft") != -1) 
    {
        return window[movieName];
    }
    else 
    {
        return document[movieName];
    }
}

function removeSpaces(string) {
 return string.split(' ').join('');
}


function connectTo(pkey,gkey)
{
        $.post("/stitch", 
            { pkey: pkey , gkey: gkey },
            function(data){
                    $('#connect_button_div').html('Connected');
            });

}

function browseMyHistory(key)
{

    $.get('/list',{ pkey : key,type : 'mycontent' },function(data){
        $('#mylist_result').append(data);
    });

}