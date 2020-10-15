$(".delete").click(function(e) {
	var id = this.id;
	var href = this.href;
	e.preventDefault();

	$.ajax({
		url:href,
		data:{},
	});
	$("#"+id).fadeOut(1000);
});