$(document).ready(function(){	
	/********************************************************************************************** more button for new records */
	var	count_new_records = parseInt($('#count_new_records').text(), 10)
		page_new_records = $('.records_line').length;

	$('.new_records .more_button').hide();

/*	console.log(count_new_records);
	console.log(page_new_records);*/

	if(count_new_records > page_new_records){
		$('.new_records .more_button').show(1000);
	};

	$('.new_records .more_button').on('click', function(event){
		event.preventDefault();

		page_new_records = $('.record_line').length;

/*		console.log(count_new_records);
		console.log(page_new_records);*/

		$.ajax({
			url: "/last_records/",
			type: 'POST',
			dataType:"json",
			data: {
				"page_new_records": page_new_records,
				"count_new_records": count_new_records,
				"csrfmiddlewaretoken": $.csrf_token
			},
			error: function() {
				//alert('Ошибка получения запроса');
			},			
			success: function(data) {	
				data = JSON.parse(data);

				$.each(data, function(){
					$('.new_records .list_table tbody').append('<tr class="article record_line"> \
						<td class="cell_title"> \
						<a class="article_link" href="/record/' + this.pk + '/"> \
						<h3 class="h3">' + this.fields.title + '</h3> \
						</a> \
						</td> 	\
						</tr>');					
				});	
			},
			complete: function(){
				page_new_records = $('.record_line').length;
				if(count_new_records <= page_new_records){
					//console.log('eq');
					$('.new_records .more_button').hide();	
				};			
			}
		});			
	});	

	/*********************************************************************************************** ajax search record */
	$('#formSearchRecordSubmit').on('click', function(event){
		var	block_search = $('.search_record .search_list'),
			block_search2 = $('.search_record .list_table tbody'),
			searchWord = $('#formSearchRecordWord').val();

		event.preventDefault();

		$.ajax({
			url: "/search_record/",
			type: 'POST',
			dataType:"json",
			data: {
				"record": searchWord,
				"csrfmiddlewaretoken": $.csrf_token
			},
			beforeSend : function(jqXHR,data){
				block_search2.empty();

				if(!searchWord){
					return false;
				};
			},			
			success: function(data) {	
				try {
					for(var key in data[0]){
						//console.log( "key: " + key + ", value: " + data[0][key] );
						block_search2.append(' \
							<tr class="article"> \
								<td class="cell_title extra_height"><a href="/record/' + key + '/">' + data[0][key]  + '</a></td> \
							</tr>');
					}					

					//window.location.replace('/search_author/');
				} catch(e) {
					$('#mySmallModalLabel').text('Не найдено совпадений');
					$('#infoModal').modal('show');

					setTimeout(function(){
						$('#infoModal').modal('hide');
					}, 2000);	
				}							
				
			}
		});				
	});

	/*********************************************************************************************** more button for new authors */
	var	count_new_authors = parseInt($('#count_new_authors').text(), 10)
		page_new_authors = $('.author_line').length;

	$('.new_authors .more_button').hide();

/*	console.log(count_new_authors);
	console.log(page_new_authors);*/

	if(count_new_authors > page_new_authors){
		$('.new_authors .more_button').show(1000);
	};

	$('.new_authors .more_button').on('click', function(event){
		event.preventDefault();

		page_new_authors = $('.author_line').length;

		//console.log(count_new_authors);
		//console.log(page_new_authors);

		$.ajax({
			url: "/new_authors/",
			type: 'POST',
			dataType:"json",
			data: {
				"page_new_authors": page_new_authors,
				"count_new_authors": count_new_authors,
				"csrfmiddlewaretoken": $.csrf_token
			},
			error: function() {
				//alert('Ошибка получения запроса');
			},			
			success: function(data) {	
				data = JSON.parse(data);

				$.each(data, function(){
					$('.new_authors .list_table tbody').append('<tr class="article author_line"> \
							<td class="cell_title"> \
								<a class="article_link" href="/profile/' + this.pk + '/"> <h3 class="h3"> ' + this.fields.nickname + '</h3> \
								</a> \
							</td> \
							<td class="cell_actions"> \
								<button type="button" class="btn btn-default btn-xs"><a class="glyphicon glyphicon-list-alt" href="/diary/' + this.pk + '/ ">Дневник</a></button> \
								<button type="button" class="btn btn-default btn-xs"><a class="glyphicon glyphicon-user" href="/profile/' + this.pk + '/ ">Профиль</a></button> \
							</td> \
						</tr>\
					');					
				});	
			},
			complete: function(){
				page_new_authors = $('.author_line').length;
				if(count_new_authors <= page_new_authors){
					//console.log('eq');
					$('.new_authors .more_button').hide();	
				};			
			}
		});			
	});	
		
	/*********************************************************************************************** ajax search author */
	$('#formSearchAuthorSubmit').on('click', function(event){
		var	block_search = $('.search_author .search_list'),
			block_search2 = $('.search_author .list_table tbody'),
			searchWord = $('#formSearchAuthorWord').val();

		event.preventDefault();

		$.ajax({
			url: "/search_author/",
			type: 'POST',
			dataType:"json",
			data: {
				"author": searchWord,
				"csrfmiddlewaretoken": $.csrf_token
			},
			beforeSend : function(jqXHR,data){
				block_search2.empty();

				if(!searchWord){
					return false;
				};
			},			
			success: function(data) {	
				try {
					//console.log('___' + data);

					for(var key in data[0]){
						//console.log( "key: " + key + ", value: " + data[0][key] );
						block_search2.append(' \
							<tr class="article"> \
								<td class="cell_title">' + data[0][key]  + '</td> \
								<td class="cell_actions"><button type="button" class="btn btn-default btn-xs"><a class="glyphicon glyphicon-list-alt" href="/diary/' + key + '/">Дневник</a> </button> \
								<button type="button" class="btn btn-default btn-xs"><a class="glyphicon glyphicon-user" href="/profile/' + key + '/">Профиль</a> </button> \
								<!--<button type="button" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-envelope">Написать письмо</span> </button></td>--> \
							</tr>');
					}					

					//window.location.replace('/search_author/');

				} catch(e) {
					$('#mySmallModalLabel').text('Не найдено совпадений');
					$('#infoModal').modal('show');

					setTimeout(function(){
						$('#infoModal').modal('hide');
					}, 2000);	
				}							
				
			}
		});				
	});

	/*********************************************************************************************** ajax activeRecord */
	$('.activeRecord').on('click', function(){
		$.ajax({
			url: "/active_record/",
			type: 'POST',
			dataType:"json",
			data: {
				"id_rec": $(this).attr('data-id-rec'),
				"csrfmiddlewaretoken": $.csrf_token
			},
			error: function() {
				//alert('Ошибка получения запроса');
			},
			success: function(data) {
				var	text;

				console.log(data.result);

				if(data.result == true){
					text = 'Доступ открыт';
				}
				else{
					text = 'Доступ закрыт';
				}
				
				$('#mySmallModalLabel').text(text);
				$('#infoModal').modal('show');

				setTimeout(function(){
					$('#infoModal').modal('hide');
					window.location.replace('/my_records/');
				}, 2000);				
			}
		});				
	});

	/*********************************************************************************************** ajax deleteRecord*/
	$('.deleteRecord').on('click', function(){
		$.ajax({
			url: "/delete_record/",
			type: 'POST',
			dataType:"json",
			data: {
				"id_delete": $(this).attr('data-id-delete'),
				"csrfmiddlewaretoken": $.csrf_token
			},
			error: function() {
				//alert('Ошибка получения запроса');
			},
			success: function(data) {
				if(data.result == true){
					
					$('#mySmallModalLabel').text('Запись удалена');
					$('#infoModal').modal('show');

					setTimeout(function(){
						$('#infoModal').modal('hide');
						window.location.replace('/my_records/');
					}, 2000);
				}
			}
		});				
	});

	/*********************************************************************************************** ajax form image load */
	var	form = $('#avatarForm');

	form.ajaxForm();

	$('#avaSubmit').on('click', function(){
		form.ajaxSubmit({
		    url: form.action,
		    type : form.method,
		    data: $(form).serialize(),
		    success: function (data) {
				window.location.replace('/change_avatar/');
		    }
		});
	});

	/*********************************************************************************************** delete_profile */
	$('#delete_profile').on('click', function(){
		$('#commonModalLabel').text('Удалить профиль?');
		$('#commonModal .modal-body').html('Возможность восстановить профиль будет доступна в течение двух недель. Для восстановления нужно отправить <a href="mailto:prozaik81-2@yandex.ru">администратору</a> ресурса письмо с почтового адреса, который был указан в профиле.');
		$('#commonModal').modal('show');	

		$('#commonModal .but_ok').on('click', function(){
			$.ajax({
				url: "/accounts/delete_profile/",
				type: 'POST',
				dataType:"json",
				data: {
					"csrfmiddlewaretoken": $.csrf_token
				},
				error: function() {
					//alert('Ошибка получения запроса');
				},
				success: function(data) {
					if(data.result == true){
						$('#mySmallModalLabel').text('Профиль удалён');
						$('#infoModal').modal('show');

						setTimeout(function(){
							$('#infoModal').modal('hide');
							location.href = '/';
						}, 2000);
					}
				}
			});				
		});
	});

	/*********************************************************************************************** form change profile */
	$(".profile_form .btn_submit").click(function(event){
		var	gender = $('#id_gender').val(),
			phone = $('#id_phone').val(),
			skype = $('#id_skype').val(),
			other = $('#id_other').val();
			nickname = $('#id_nickname').val();

		event.preventDefault();

		$.ajax({
			url: "/change_profile/",
			type: 'POST',
			dataType:"json",
			data: {
				"gender": gender,
				"phone": phone,
				"skype": skype,
				"nickname": nickname,
				"other": other,
				"csrfmiddlewaretoken": $('#profile_form input[name=csrfmiddlewaretoken]').val()
			},
			error: function() {
				//alert('Ошибка получения запроса');
			},
			success: function(data) {
				if(data.result){
					$('#mySmallModalLabel').text('Изменения сохранены');
					$('#infoModal').modal('show');

					setTimeout(function(){
						$('#infoModal').modal('hide');
					}, 2000);
				}
			}
		});		
	});

	/*********************************************************************************************** form login check */
/*	$("#login_submit").click(function(event){
		var	username = $('#id_username').val(),
			password = $('#id_password').val();

		event.preventDefault();

		$.ajax({
			url: "/accounts/ajax_login_check/",
			type: 'POST',
			dataType:"json",
			data: {
				"username": username,
				"password": password,
				"csrfmiddlewaretoken": $('#loginForm input[name=csrfmiddlewaretoken]').val()
			},
			error: function() {
				//alert('Ошибка получения запроса');
			},
			success: function(data) {
				var	error_list_login,
					error_list_pass,
					error_list_active;

				if(data.error_login == false){
					error_list_login = '';
				}

				if(data.error_pass == false){
					error_list_pass = '';
				}	

				if(data.error_active == false){
					error_list_active = '';
				}		

				console.log(data.error_list_active);		
				console.log(data.error_active);		

				if(data.error_login == false && data.error_pass == false && data.error_active == false){
					$('#mySmallModalLabel').text('Вы успешно авторизовались');
					$('#infoModal').modal('show');

					setTimeout(function(){
						$('#infoModal').modal('hide');
					}, 2000);					

					$('#infoModal').on('hidden.bs.modal', function (){
						$('#infoModal').modal('hide');
						$('#loginForm').submit();
					})	
				}			

				$('#error_list_login').text(data.error_message_login);
				//$('#error_list_login').text(data.error_message_active);
				$('#error_list_pass').text(data.error_message_pass);
			}
		});		
	});
*/

	/*********************************************************************************************** form registration check */
/*	$("#registration_submit").click(function(event){
		var	username = $('#id_username').val(),
			email = $('#id_email').val(),
			password1 = $('#id_password1').val(),
			password2 = $('#id_password2').val();

		event.preventDefault();

		$.ajax({
			url: "/accounts/ajax_registration_check/",
			type: 'POST',
			dataType:"json",
			data: {
				"username": username,
				"email": email,
				"password1": password1,
				"password2": password2,
				"csrfmiddlewaretoken": $('#registrationForm input[name=csrfmiddlewaretoken]').val()
			},
			error: function() {
				//alert('Ошибка получения запроса');
			},
			success: function(data) {
				var	error_list_login,
					error_list_email,
					error_list_password1,
					error_list_password2;

				if(data.error_login == false){
					error_list_login = '';
				}

				if(data.error_email == false){
					error_list_email = '';
				}	

				if(data.error_password1 == false){
					error_list_password1 = '';
				}		

				if(data.error_password2 == false){
					error_list_password2 = '';
				}														

				if(data.error_login == false && data.error_email == false && data.error_password1 == false && data.error_password2 == false){
					

					$('#mySmallModalLabel').text('Вы успешно зарегистрировались');
					$('#infoModal').modal('show');

					setTimeout(function(){
						$('#infoModal').modal('hide');
					}, 2000);					

					$('#infoModal').on('hidden.bs.modal', function (){
						$('#infoModal').modal('hide');
						$('#registrationForm').submit();
					})						
				}			

				$('#error_list_login').text(data.error_message_login);
				$('#error_list_email').text(data.error_message_email);
				$('#error_list_password1').text(data.error_message_password1);
				$('#error_list_password2').text(data.error_message_password2);
			}
		});		
	});	*/
	

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