$(document).ready(function(){		
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
					alert('Ошибка получения запроса');
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

		event.preventDefault();

		$.ajax({
			url: "/change_profile/",
			type: 'POST',
			dataType:"json",
			data: {
				"gender": gender,
				"phone": phone,
				"skype": skype,
				"other": other,
				"csrfmiddlewaretoken": $('#profile_form input[name=csrfmiddlewaretoken]').val()
			},
			error: function() {
				//alert('Ошибка получения запроса');
			},
			success: function(data) {
				$('#mySmallModalLabel').text('Изменения сохранены');
				$('#infoModal').modal('show');

				setTimeout(function(){
					$('#infoModal').modal('hide');
				}, 2000);
			}
		});		
	});

	/*********************************************************************************************** form login check */
	$("#login_submit").click(function(event){
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


	/*********************************************************************************************** form registration check */
	$("#registration_submit").click(function(event){
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
	});	
	

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