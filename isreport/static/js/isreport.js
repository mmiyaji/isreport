// authorの年度リスト
function select_author(){
	$.ajax({
		 type: "GET",
		 url: "/isreport/select_author",
		 success: function(html){
			$("a#add_author").before(html)
		 },
		 complete: function(){	
	　　 },
	 });
}
function show_org(){
	$("#report_org_html").toggle();
}
function delete_author(elem){
	elem.parentNode.parentNode.removeChild(elem.parentNode);
	// document.body.removeChild(elem.parentNode);
}
function author_change(elem){
	document.getElementById("setting_roman").value = $('select#'+elem.id+' option:selected')[0].title;
}
// アップロード時のauthor選択
function authors_change(elem){
	document.getElementById("entry_authors").innerHTML = "";
	document.getElementById("entry_authors").title = "";
	$("select#"+elem.id+" option:selected").each(function (index, domEle) {
		if(document.getElementById("entry_authors").innerHTML!=""){
			document.getElementById("entry_authors").innerHTML+="，"
		}
		var auths = domEle.title.split(",");
		document.getElementById("entry_authors").innerHTML += auths[0];
		if(auths.length>1){
			document.getElementById("entry_authors").title += auths[1]+",";
		}
	});
}
// アップロード時のgroup選択
function groups_change(elem){
	document.getElementById("entry_groups").innerHTML = "";
	document.getElementById("entry_groups").title = "";
	$("select#"+elem.id+" option:selected").each(function (index, domEle) {
		if(document.getElementById("entry_groups").innerHTML!=""){
			document.getElementById("entry_groups").innerHTML+="，"
		}
		var auths = domEle.title.split(",");
		document.getElementById("entry_groups").innerHTML += auths[0];
		if(auths.length>1){
			document.getElementById("entry_groups").title += auths[1]+",";
		}
	});
}
function tags_change(elem){
	document.getElementById("entry_tags").value = "";
	$("select#"+elem.id+" option:selected").each(function (index, domEle) {
		if(document.getElementById("entry_tags").value!=""){
			document.getElementById("entry_tags").value+=","
		}
		document.getElementById("entry_tags").value += domEle.title;
	});
}
function check_submit(event){
		is_pre = true;
		convert();
		var def_htmls = $('iframe#preview').contents().find("body").html();
		// imageタグが絶対パスなので無理矢理相対パスに書き換え．運用ドメインによっては正しく動作しないかも
		$('iframe#preview').contents().find("img").each(function (index, domEle){
			doms = [];
			// domEle.src = domEle.src.replace(">","/>");
			doms = domEle.src.split("/");
			if(doms[10]){
				domEle.src = doms[9]+"/"+doms[10];
			}else{
				domEle.src = doms[8]+"/"+doms[9];
			}
		});
		var htmls = $('iframe#preview').contents().find("body").html();
		$("input#html_body_def").val(def_htmls);
		$("input#html_body").val(htmls);
		return true;
}

function check_submit2(event){
	title = document.getElementById("p_title").value;
	number = document.getElementById("p_number").value;//number.value
	publish_at = document.getElementById("p_date").value;
	if(title && number && publish_at){
		return true;
	}else{
		alert("未入力の項目があります");
		return false;
	}
}
function fav_click(thisis){
	var $fav_target = $(thisis).attr("id").split("_")[1]
	if($(thisis).hasClass("star")){
		$.ajax({
			 type: "POST",
			 url: "/isreport/change_favorite",
			 data: "id="+$fav_target+"&reset=true",
			 success: function(){
				$("#fav_"+$fav_target).removeClass("star");
				// $("#fav_"+$fav_target).addClass("non_fav");
			 },
			 complete: function(){	
		　　 },
		 });
		
	}else{
		$.ajax({
			 type: "POST",
			 url: "/isreport/change_favorite",
			 data: "id="+$fav_target,
			 success: function(){
				// $("#fav_"+$fav_target).removeClass("non_fav");
				$("#fav_"+$fav_target).addClass("star");
			 },
			 complete: function(){
		　　 },
		 });
	}
}
function addbook(thisis){
	var $fav_target = $(thisis).attr("id").split("_")[1];
	$.ajax({
		 type: "GET",
		 url: "/isreport/ajax/book",
		 data: "id="+$fav_target+"&view_level="+network_delete_level,
		 success: function(html){
			var windows = $("#curtain");
			if(windows){
				hide_curtain()
			}
			create_curtain();
			windows = $("#curtain");
			frame_tmp = "<div class='movable' id='book_entry'><a class='hide_button' href='#' onclick='hide_curtain()'>×</a>"+html+"</div>";
			windows.append(frame_tmp);
		 },
		 complete: function(){
	　　 },
	 });
}
function book_change(){
	location.href="/isreport/epub?book="+$('select#select_book option:selected')[0].value;
}
function book_form_cancel(){
	hide_curtain();
}
function book_form_change(){
	if($('select#select_form_book option:selected')[0].value=="-1"){
		var sel = $("div#book_entry li.book_form_sel");
		sel.after('<li><input type="text" name="newbook" value="New Book" /></li>')
		sel.after('<label><input type="checkbox" name="isvalid" checked/>公開設定</label>')
	}
}

function remove_book(data){
	$.ajax({
		 type: "POST",
		 url: "/isreport/remove_book",
		 data: data,
		 success: function(){
			location.href="/isreport/setting";
		 },
		 complete: function(){
	　　 },
	 });
}
function load_recommend(ids){
	if(ids){
		// alert(ids);
		$.ajax({
			 type: "POST",
			 url: "/isreport/recommend/report",
			 data: "id="+ids,
			 success: function(html){
				// $("#recom_report").append(html);
				$("#recom_report img").replaceWith(html);
			 },
			 error: function(){
				$("#recom_report img").replaceWith("<p>ロードエラー</p>");
		　 	},
			 complete: function(){	
		　　 },
		 });
	}
}

function iFrameHeight() {
	$("#frameblock").exFitFrame();
	// var h = 0;
	// // Opera
	// if (window.opera)
	// {
	// 	h = document.getElementById('frameblock').contentDocument.body.offsetHeight + 20;
	// 	document.getElementById('frameblock').setAttribute("height",h);
	// }
	// // Safari ~ Chrome
	// else if (/WebKit/i.test(navigator.userAgent))
	// {
	// 	var posVersion = navigator.userAgent.indexOf("WebKit/");
	// 	var version = navigator.userAgent.substring(posVersion + 7, posVersion + 10);
	// 	if (parseInt(version) >= 523) // Safari 3+
	// 	{
	// 		document.getElementById('frameblock').style.height = '0px';
	// 	}
	// 	else // Safari 1+ or 2+
	// 	{
	// 		return document.getElementById('frameblock').style.height = '152px';
	// 	}
	// 	h = document.getElementById('frameblock').contentDocument.height;
	// 	document.getElementById('frameblock').style.height = h + 'px';
	// }
	// // FireFox
	// else if (navigator.userAgent.indexOf("Firefox") != -1)
	// {
	// 	h = document.getElementById('frameblock').contentDocument.body.offsetHeight + 20;
	// 	document.getElementById('frameblock').style.height = h + 'px';
	// }
	// // IE
	// else if (document.all)
	// {
	// 	h = document.frames('frameblock').document.body.scrollHeight;
	// 	document.all.blockrandom.style.height = h + 20 + 'px';
	// }
	// // Misc
	// else
	// {
	// 	h = document.getElementById('frameblock').contentDocument.height;
	// 	document.getElementById('frameblock').style.height = h + 60 + 'px';
	// }
}