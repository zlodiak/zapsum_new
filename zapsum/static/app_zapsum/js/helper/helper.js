$(document).ready(function(){	
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
				alert('Ошибка получения запроса');
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
					console.log(data);

					for(var key in data[0]){
						console.log( "key: " + key + ", value: " + data[0][key] );
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
});