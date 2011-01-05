/*

Photolog GAE app helper javascript

Version 1.0.0

Authors:
	Jaehong Park

*/
function applystyle_rotate_n_style(intIndex,copy_of_this)
{
		var sub_select;

		sub_select = copy_of_this.find('div:first');
        sub_select.toggleClass('rotate');


		if(sub_select.hasClass('rotate'))
		{
			/ * adding rotation  if it is rotatable */
			var rn = Math.floor(Math.random()*11);
			var rt;
			if(intIndex%2)
			{
				rt = 'rotate(-'+rn.toString()+'deg)';
			}
			else
			{
				rt = 'rotate('+rn.toString()+'deg)';
			}
			sub_select.css({'-webkit-transform':rt,'-moz-transform':rt});
		}
		
        apply_frame_style(copy_of_this);
/*        
		if(sub_select.hasClass('image'))
		{
            sub_select.toggleClass('instax_child_img');
		}
		
		if(sub_select.hasClass('location'))
		{
			sub_select.find('img:first').addClass('thumb_child_img');
		}

		if(sub_select.hasClass('longtext'))
		{
			sub_select.find('div:first').addClass('jSticky-medium');
		
		}
		
		if(sub_select.hasClass('trackback'))
		{
			sub_select.find('div:first').addClass('jSticky-medium');
		}
*/
		//copy_of_this.appendTo('#deco_children');
}

function apply_frame_style(copy_of_this)
{
    copy_of_this.find('div.image').toggleClass('instax_child_img');
    copy_of_this.find('div.image-title').show();
    copy_of_this.find('div.location img').addClass('thumb_child_img');
    copy_of_this.find('div.longtext div:first').addClass('jSticky-medium');
    copy_of_this.find('div.trackback div:first').addClass('jSticky-medium');
}

function disable_style(copy_of_this)
{
        copy_of_this.toggleClass('apsolute');
        copy_of_this.css('top','auto');
        copy_of_this.css('left','auto');        
        sub_select = copy_of_this.find('div:first');
        sub_select.attr('style','display:block;left:auto;top:auto');
        sub_select.toggleClass('rotate');
        

		if(sub_select.hasClass('image'))
		{
            sub_select.find('div.image-title').hide();
            sub_select.toggleClass('instax_child_img');
		}
		
		if(sub_select.hasClass('location'))
		{
			sub_select.find('img:first').toggleClass('thumb_child_img');
		}

		if(sub_select.hasClass('longtext'))
		{
			sub_select.find('div:first').toggleClass('jSticky-medium');
		
		}
		
		if(sub_select.hasClass('trackback'))
		{
			sub_select.find('div:first').toggleClass('jSticky-medium');
		}
        


}