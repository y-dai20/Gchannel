$(function(){
	$('.modal-open').each(function(){
		$(this).on('click', function(){
			var target = $(this).data('target');
			var modal = document.getElementById(target);
			$(modal).addClass('active');
			return false;
		});
	});

	$('.modal-close').on('click',function(){	
		$('.modal-container').removeClass('active');
		return false;
	});

	// $(document).on('click',function(e) {
	// 	if(!$(e.target).closest('.modal-body').length) {
	// 		$('.modal-container').removeClass('active');
	// 	}
	// });

	$('.reply-button').on('click', function(){
		var id = $(this).attr('data-catid');
		$("form[name='reply-form-" + id + "']").validate({
			rules:{
				text:{
					required:true,
					maxlength:255,
				},
				url:{
					maxlength:255,
				},
				img:{
					extension: "jpg|jpeg|png|ico|bmp"
				}
			},
	
			messages:{
				text:{
					required:"本文を入力してください．",
					maxlength:"255字以内で入力してください．",
				},
				url:{
					maxlength:"255字以内で入力してください．"
				},
				img:{
					extension:"拡張子が[jpg，jpeg，png，ico，bmp]のものだけアップロードできます．",
				}
			},
	
			submitHandler: function(form) {
				form.submit();
			},
		});
	});

	$("form[name='post-form']").validate({
		rules:{
			title:{
				required:true,
				maxlength:50,
			},
			text:{
				required:true,
				maxlength:255,
			},
			img:{
				extension: "jpg|jpeg|png|ico|bmp"
			}
		},

		messages:{
			title:{
				required:"タイトルを入力してください．",
				maxlength:"50字以内で入力してください．",
			},
			text:{
				required:"本文を入力してください．",
				maxlength:"255字以内で入力してください．",
			},
			img:{
				extension:"拡張子が[jpg，jpeg，png，ico，bmp]のものだけアップロードできます．",
			}
		},

		submitHandler: function(form) {
			form.submit();
		},
	});
});