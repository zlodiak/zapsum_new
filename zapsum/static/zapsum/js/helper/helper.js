$(document).ready(function(){		
	/*********************************************************************************************** active menu punkt */
	var	pathname = location.pathname,
		pathnameList = pathname.split('/'),
		slug1 = pathnameList[1],
		slug2 = pathnameList[2];

	var coll_links,
		flag_sub,
		menu_container = $('.nav_top');

	//console.log('slug1::' + slug1);
	//console.log('slug2::' + slug2);

	menu_container.find('a').removeClass('active');

	if(slug1 == ''){
		//console.log('main page');
		menu_container.find('a').eq(1).closest('li').addClass('active');	// for index punkt
	}
	else if(slug1 != 'accounts'){
		//console.log('page');
		coll_links = menu_container.find('a[href="/' + slug1 + '/"]');

		$(coll_links).each(function(){
			var	href = $(this).attr('href');

			flag_sub = $(this).closest('.dropdown-menu');
			
			if(flag_sub.length > 0){
				$(flag_sub).siblings('a').closest('li').addClass('active');	// for sub punkts
			}
			else{
				$(this).closest('li').addClass('active');	// for root punkts
			}
		});			
	}
	else{
		//console.log('account page');
		if(slug2 == 'authentication'){
			menu_container.find('a[href="/accounts/authentication/"]').closest('li').addClass('active');
		}
		else{
			menu_container.find('a[href="/accounts/registration/"]').closest('li').addClass('active');
		}
	}

	
});