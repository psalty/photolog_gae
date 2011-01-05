/*

Photolog GAE app helper javascript

Version 1.0.0

Authors:
	Jaehong Park

*/

// reutrn a user's photo tags(keywords)
function browseFlickr()
{
    $('#flickr_result').html("");
    
    $.get('/photolog_flickr_api_helper',
        { method : 'listkeywords',
          username : $('#flickr_id').val()},
        function(data){
            $('#flickr_result').html(data);
        });
}

// return user's photographs that has given keyword
function searchFlickrPhoto(user_id,keyword)
{
    $('#flickr_result').html("");
    $.get('/photolog_flickr_api_helper',
        { method : 'listphotos',
          username : user_id,
          tags : keyword },
        function(data){
            $('#flickr_result').html(data);
         
        });    
}

function previewFlickrImage(user_id,photo_id,server,secret,title)
{
    var preview_image_url = "http://static.flickr.com/"+server+"/"+photo_id+"_"+secret+"_m.jpg";
    var jscript = "javascript:addFlickrImage('"+user_id+"','"+photo_id+"','"+server+"','"+secret+"','"+title+"')";
    
    var div_wrap = $(document.createElement('div')).css('text-align','center');
    var div_img = $(document.createElement('div'));
    var div_btn = $(document.createElement('div')).css('padding-top','10px');
    var img = $(document.createElement('img')).attr('src',preview_image_url);
    var button = $(document.createElement('a')).addClass('minibutton').attr('href',jscript);
    var butttl = $(document.createElement('span')).text('Post As '+$('meta[name=fbn]').attr("content"));
    
    button.append(butttl);
    div_img.append(img);
    div_btn.append(button);
    
    div_wrap.append(div_img);
    div_wrap.append(div_btn);
    
    $('#upload-flickr-detail').html(div_wrap);
}

// add flickr image to datastore
function addFlickrImage(uid,id,srv,scrt,title)
{
    $.post('/create', {target : 'flickr', 
                                    username : $('#flickr_id').val(),
                                    user_id : uid, 
                                    photo_id : id, 
                                    server : srv, 
                                    secret : scrt, 
                                    title : title },
        function(data){
        
            if(data.status == "OK")
            {
                $('#move_to_btn').attr('href','javascript:moveToView("'+data.newkey+'")');
                move_to_step_3();
                
            }
            else
            {
                $('#upload-flickr-detail').text('Error : Fail to Post');
            }
        },"json");
}

// retrieve rss feed of picasa album 
function browsePicasa()
{
    $('#picasa_result').html("");
    var api = 'http://picasaweb.google.com/data/feed/api/user/'+$('#picasa_id').val();
    var feed = new google.feeds.Feed(api);
    feed.setNumEntries(50);
    feed.setResultFormat(google.feeds.Feed.XML_FORMAT);
    feed.load(function(result) 
    {
        if (!result.error) {
        $(result.xmlDocument).find("entry").each(function(){
            
            var album_id = $(this).find('[nodeName=gphoto:id]').text();
      
            var title = $(this).find('title').first().text();
            var div = $(document.createElement('div'));
            var hlink = "javascript:browsePicasaAlbum('"+$('#picasa_id').val()+"','"+album_id+"');";
            var anchor = $(document.createElement('a')).attr('href',hlink);
            anchor.append(document.createTextNode(title));
            div.append(anchor);
            $('#picasa_result').append(div);                    
        });
        
        }
    });
}

// retrieve photographs of an album
function browsePicasaAlbum(user_id,album_id)
{
    $('#picasa_result').html("");
    var api = 'http://picasaweb.google.com/data/feed/api/user/'+user_id+'/albumid/'+album_id+'?thumbsize=72c\,320u'
    var feed = new google.feeds.Feed(api);
    feed.setNumEntries(50);
    feed.setResultFormat(google.feeds.Feed.XML_FORMAT);
    feed.load(function(result) 
    {
        if (!result.error) {
            $(result.xmlDocument).find("entry").each(function(){
            
            var media_group = $(this).find('[nodeName=media:group]');
            
            var image_path  = media_group.find('[nodeName=media:content]').first().attr('url');
            var ts   = media_group.find('[nodeName=media:thumbnail]').first().attr('url');
            var tm  = media_group.find('[nodeName=media:thumbnail]').first().next().attr('url');
            var title       = media_group.find('[nodeName=media:title]').first().text();
            var author      = media_group.find('[nodeName=media:credit]').first().text();
            var tags        = media_group.find('[nodeName=media:keywords]').first().text();
                    
            //var script_path = "javascript:addPicasaImage('"+author+"','"+title+"','"+image_path+"','"+ts+"','"+tm+"','"+tags+"');";
            
            var script_path = "javascript:previewPicasaImage('"+author+"','"+title+"','"+image_path+"','"+ts+"','"+tm+"','"+tags+"');";
            var a = $(document.createElement('a')).addClass('thumb').attr('href',script_path);
            var img = $(document.createElement('img')).attr('src',ts);
                    a.append(img);
                    $('#picasa_result').append(a);
            
            });
        }
    });
}

function previewPicasaImage(author,title,url,ts,tm,keywords)
{
    var script_path = "javascript:addPicasaImage('"+author+"','"+title+"','"+url+"','"+ts+"','"+tm+"','"+keywords+"');";
    
    var div_wrap = $(document.createElement('div')).css('text-align','center');
    var div_img = $(document.createElement('div'));
    var div_btn = $(document.createElement('div')).css('padding-top','10px');
    var img = $(document.createElement('img')).attr('src',tm);
    var button = $(document.createElement('a')).addClass('minibutton').attr('href',script_path);
    var butttl = $(document.createElement('span')).text('Post As '+$('meta[name=fbn]').attr("content"));
    
    button.append(butttl);
    div_img.append(img);
    div_btn.append(button);
    
    div_wrap.append(div_img);
    div_wrap.append(div_btn);
    
    $('#upload-picasa-detail').html(div_wrap);
}

// add picasa image to datastore
function addPicasaImage(author,title,url,ts,tm,keywords)
{
    $.post('/create', {target : 'picasa', 
                                    credit : author, 
                                    url : url,
                                    thumb_s : ts,
                                    thumb_m : tm,  
                                    title : title,
                                    keywords : keywords},
        function(data){
            if(data.status == "OK")
            {
                $('#move_to_btn').attr('href','javascript:moveToView("'+data.newkey+'")');
                move_to_step_3();
                
            }
            else
            {
                $('#upload-flickr-detail').text('Error : Fail to Post');
            }
        },"json");

}

function previewMyContent(key,src)
{
    var script_path = "javascript:move_to_step_3();";
    var div_wrap = $(document.createElement('div')).css('text-align','center');
    var div_img = $(document.createElement('div'));
    var div_btn = $(document.createElement('div')).css('padding-top','10px');
    var img = $(document.createElement('img')).attr('src',src);
    var input = $(document.createElement('input')).attr('type','hidden').attr('id','gkey');
    input.val(key);
    var button = $(document.createElement('a')).addClass('minibutton').attr('href',script_path);
    var butttl = $(document.createElement('span')).text('Stich As '+$('meta[name=fbn]').attr("content"));
    
    button.append(butttl);
    div_img.append(img);
    div_btn.append(button);
    
    div_wrap.append(div_img);
    div_wrap.append(input);
    div_wrap.append(div_btn);
    
    $('#upload-relationship-detail').html(div_wrap);

}


/*
    TBD
*/
function browseRssFeed()
{
    $('#rss_result_list').html('');
    var rssfeed =  $('#rss_url').val();
    var feed = new google.feeds.Feed(rssfeed);
    feed.setResultFormat(google.feeds.Feed.XML_FORMAT);
    feed.load(function(result) 
    {
        if (!result.error) 
        {
            $(result.xmlDocument).find("item").each(function(){
                var title = $('<div/>').html($(this).find('title').first().text());
                var li = $(document.createElement('li'));
                var anchor = $(document.createElement('a'));
                //alert($(this).find('description').first().text());
                // decode strings
                var desc = $('<div/>').html($(this).find('description').first().text());
                var images = $(desc).find('img').first();
    
                var script = "javascript:blogListAllImage('"+title.text()+"','"+$(this).find('description').first().text()+"');";
                
                anchor.attr('href',script);
                anchor.append(document.createTextNode(title.text()));
                li.append(anchor);
                
                $('#rss_result_list').append(li);
            });
        }
    });
}

function blogListAllImage(title,desc)
{
    $('#rss_result').html('');
    var dsc = $('<div/>').html(desc);
    var image_block = $(dsc).find('.imageblock')
    
    var images = image_block.find('img');

    images.each(function(index) 
    {
        var script = "javascript:blogImportImage()";
        var anchor = $(document.createElement('a'));
        anchor.attr('href',script);
        anchor.append($(this).attr('width','80').attr('height','80'));
        $('#rss_result').append(anchor);
    });

    var descriton = dsc.text();
}

