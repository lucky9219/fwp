function bookmark_edit(){
	var item=$(this).parent();
	var url=item.find(".title").attr("href")
	item.load("/save/?ajax&url="+escape(url),null,function(){
		$("#save-form").submit(bookmark_save),
	});
	return false;
}

$(document).ready(function()){
	$("ul.bookmarks.edit").click(bookmark_edit);
});
}

