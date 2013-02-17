// 使ってないよ ->　isreport.jsへ
dragObj = new Object();
dragObj.dragFlag = false;
dragObj.offsetX = dragObj.offsetY = 0;
dragObj.mouseX = dragObj.mouseY = 0;
dragObj.target = null;
dragObj.zIndex = 1;	// 最初のZ-Index
dragObj.maxLayer = 10;	// 最大レイヤー枚数
window.document.onmousemove = dragProc;
window.document.onmouseup = dragEnd;

function hand_list(elem){
	// alert(elem.id);
	// document.getElementById("debb").innerHTML("OO");
	// elem.onmousedown = dragStart;
	// elem.style.zIndex = 10;
	// var off = getElemPos(document.getElementById("thr_"));
	// $("#thr_").center4(off.x,off.y);
	// alert(off.x);
	// document.getElementById("thr_").onmousedown = dragStart;
	// document.getElementById("debb").innerHTML=elem.innerHTML;
	// $("#report_content").after("<div class='report_item item_lists' id='empty'>"+elem.innerHTML+"</div>")
	document.getElementById("empty").innerHTML = elem.innerHTML;
	// $("#"+elem.id).addClass("empt");
	$("#"+elem.id).addClass("empt");
	dragStart(document.getElementById("empty"));
	// alert("OK");
	// document.getElementById("debb").innerHTML(off.x);
	old_hover = elem.id;
}
function getElemPos(elem){
	var elemPos = new Object();
	elemPos.x = 0;
	elemPos.y = 0;
	while(elem){
		elemPos.x += elem.offsetLeft;
		elemPos.y += elem.offsetTop;
		elem = elem.offsetParent;
	}
	if (navigator.userAgent.indexOf('Mac') != -1 && typeof document.body.leftMargin != "undefined") {
		elemPos.x += document.body.leftMargin;
		elemPos.y += document.body.topMargin;
	}
	return elemPos;
}

jQuery.fn.center = function () { // 680 250 536
		var tops = 100 //($(window).height() - this.height() ) / 2+$(window).scrollTop()-150;
		// alert($(window).height()+":"+this.height()+":"+$(window).scrollTop()+":")
		// if(tops<0){tops=0;}
		if(tops>$(window).height()){tops=0;}
		this.css("top",	tops + "px");
		this.css("left", ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px");
		return this;
	}
jQuery.fn.center4 = function(xx,yy){
		this.css("position","absolute");
		this.css("top", yy + "px");
		this.css("left", xx + "px");
		this.css("z-index","10");
		return this;
	}
jQuery.fn.screen = function () { // 680 250 536
		this.css("width","80%");
		this.css("height","70%");
		this.css("max-height","400px");
		return this;
	}


// ドラッグ開始処理
function dragStart(targetElement)
{	
	// if(window.addEventListener)
	// {
	// 	// targetElement = document.getElementById(id);
	// 	// alert("k");
	// }else{
	// 	// targetElement = event.srcElement;
	// }
	dragObj.dragFlag = true;
	dragObj.targetObj = targetElement;
	// alert(parseInt(targetElement.style.left));
	// if(targetElement.style.left){
		dragObj.offsetX = dragObj.mouseX - parseInt(targetElement.style.left);
		dragObj.offsetY = dragObj.mouseY - parseInt(targetElement.style.top);
	// }else{
	// 	dragObj.offsetX = dragObj.mouseX - parseInt(getElemPos(targetElement).x);
	// 	dragObj.offsetY = dragObj.mouseY - parseInt(getElemPos(targetElement).y);
	// }
	// document.getElementById("debb").innerHTML=parseInt(targetElement.style.left);
	// dragObj.zIndex += dragObj.maxLayer;
	// dragObj.targetObj.style.zIndex = dragObj.zIndex;
	
	// alert( - parseInt(getElemPos(targetElement).y));
	$("#"+targetElement.id).center4(dragObj.mouseX,dragObj.mouseY);
	return false;
}
// ドラッグ終了処理
function dragEnd()
{	
	dragObj.dragFlag = false;
	$("#empty").hide();
	$("#emp").replaceWith($(".empt"));
	$(".empt").removeClass("empt");
	document.getElementById("empty").innerHTML ="";
	// dragObj.targetObj.style.left = "0px";
	// dragObj.targetObj.style.top = "0px";
	var pages = 0;
	$(".item_page").each(function (index, domEle){
			// // 0番目はドラッグダミーなので無視。やっぱやめた
			// if(index!=0){
				domEle.innerHTML = "p"+String(pages=pages+1)+"~p"+String(pages=pages+parseInt($(domEle).attr('title')));
			// }
		});
}
// ドラッグ中の処理
function dragProc(evt)
{	
	var mouseX,mouseY;
	if (document.all)
	{
		mouseX = event.x;
		mouseY = event.y;
	}else{
		mouseX = evt.pageX;
		mouseY = evt.pageY;
	}
	dragObj.mouseX = mouseX;
	dragObj.mouseY = mouseY;
	// alert(mouseX);
	if (!dragObj.dragFlag) return;
		if(dragObj.offsetX){
			dragObj.targetObj.style.left = mouseX - dragObj.offsetX+"px";
			dragObj.targetObj.style.top = mouseY - dragObj.offsetY+"px";
		}else{
			dragObj.targetObj.style.left = mouseX-170 +"px";
			dragObj.targetObj.style.top = mouseY+20 +"px";
		}
	$("#empty").show();
	// document.getElementById("debb").innerHTML=mouseX+":"+getElemPos(dragObj.targetObj).x+":"+dragObj.targetObj.id;
	
	return false;
}

var old_hover = "";
function dragHover(elem){
	
	if(old_hover!=elem.id && dragObj.dragFlag){
		// document.getElementById("debb").innerHTML=old_hover+":"+elem.id;
		// $("#"+elem.id).addClass("empt");
		// $("#"+old_hover).removeClass("empt");
		old_hover = elem.id;
		$("#emp").remove();
		$("#"+old_hover).after("<div class='report_item hovs item_lists' id='emp'></div>");
	}
}

function book_change(){
	location.href="/isreport/epub?book="+$('select#select_book option:selected')[0].value;
	// alert($("select#select_book option:selected")[0].value)
}
function book_form_cancel(){
	$('div#book_entry').hide();
	// alert($("select#select_book option:selected")[0].value)
}

function book_form_change(){
	// alert($('select#select_form_book option:selected')[0].value)
	if($('select#select_form_book option:selected')[0].value=="-1"){
		var sel = $("div#book_entry li.book_form_sel");
		sel.after('<li><input type="text" name="newbook" value="New Book" /></li>')
		sel.after('<label><input type="checkbox" name="isvalid" checked/>公開設定</label>')
	}
	// location.href="/epub?book="+$('select#select_book option:selected')[0].value;
	// alert($("select#select_book option:selected")[0].value)
}

function author_change(elem){
	// alert($("input#setting_roman").attr("value"))
	// $("input#setting_roman").attr("value")
	document.getElementById("setting_roman").value = $('select#'+elem.id+' option:selected')[0].title;
	// location.href="/epub?book="+$('select#select_book option:selected')[0].value;
	// alert($("select#select_book option:selected")[0].value)
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

// authorの年度リスト
function select_year(elem){
	var year = $('select#'+elem.id+' option:selected')[0].title
	
	$.ajax({
		 type: "GET",
		 url: "/isreport/select_yearth",
		 data: "year="+year,
		 success: function(html){
			$("select#authors").replaceWith(html)
		 },
		 complete: function(){	
	　　 },
	 });
	
	// document.getElementById("entry_authors").innerHTML = "";
	// document.getElementById("entry_authors").title = "";
	// $("select#"+elem.id+" option:selected").each(function (index, domEle) {
	// 	if(document.getElementById("entry_authors").innerHTML!=""){
	// 		document.getElementById("entry_authors").innerHTML+="，"
	// 	}
	// 	var auths = domEle.title.split(",");
	// 	document.getElementById("entry_authors").innerHTML += auths[0];
	// 	if(auths.length>1){
	// 		document.getElementById("entry_authors").title += auths[1]+",";
	// 	}
	// });
}
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
function delete_author(elem){
	elem.parentNode.parentNode.removeChild(elem.parentNode);
	// document.body.removeChild(elem.parentNode);
}

// 
function tags_change(elem){
	document.getElementById("entry_tags").value = "";
	$("select#"+elem.id+" option:selected").each(function (index, domEle) {
		if(document.getElementById("entry_tags").value!=""){
			document.getElementById("entry_tags").value+=","
		}
		document.getElementById("entry_tags").value += domEle.title;
	});
}

// authorの年度リスト変更
function select_yearth(elem){
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

var is_pre = true;
function is_preview(elem){
	// alert($("#"+elem.id).selected)
	// alert(elem.checked)
	// if(elem.checked){
	is_pre = elem.checked;
	// 	is_pre = true;
	// }else{
	// 	is_pre = false;
	// }
}
function convert_wiki(ev){
	if(is_pre){
		var formatter = new Wiki.Formatter();
		// alert($("#soup_text").val());
		var srcText = $("#soup_text").val();
		document.getElementById('wiki_preview').innerHTML = formatter.format(srcText);
	}
}


var edit, preview, preview_html, source, sel;
var hatena,repler;
var realtime = true;
var title, abstract, number, authors, publish_at;
function init(){
	edit = document.getElementById("soup_text");
	preview = document.getElementById("preview");
	// preview_html = document.getElementById("wiki_preview");
	preview_html = preview_frame.document.getElementById("content");
	// hatena = new Hatena({sectionanchor : "■"});
	dirpath=document.getElementById("dirpath").value;
	hatena = new Hatena();
	edit.onkeyup = function(){if(realtime) convert();};
	convert();
}
function preview_content(target,dir_path){
	preview = document.getElementById(target);
	hatena = new Hatena();
	var texts = String._unescapeHTML(preview.innerHTML);
	dirpath=dir_path;
	hatena.parse(texts,true);
	preview.innerHTML = hatena.html();
}

function set_title(ev){
	title = document.getElementById("p_title");
	preview_frame.document.getElementById("title").innerHTML = title.value;
}
function set_number(ev){
	number = document.getElementById("p_number");//number.value
	preview_frame.document.getElementById("report_num").innerHTML = number.value;
}
function set_author(ev){
	authors = document.getElementById("entry_authors");
	preview_frame.document.getElementById("authors").innerHTML = authors.innerHTML;
	// copy rightのauthorを書き換え
	var auths = document.getElementById("entry_authors").title.split(",");
	$('iframe:first').contents().find('pre.copyright span.copy_author').remove();
	// $('iframe:first').contents().find('copy_author').each(function (index, domEle) {
	// 	alert(domEle.innerHTML)
	// });
	// 著者欄とcopyrightの順を合わせる
	auths = auths.reverse();
	for(var i=0;i<auths.length;i++){
		if(auths[i]){
			$('iframe:first').contents().find('pre.copyright').prepend('<span class="copy_author">Copyright&nbsp;(C)&nbsp;<span class="copy_date">2010</span>&nbsp;'+auths[i]+',&nbsp;All&nbsp;rights&nbsp;reserved.<span>\n');
		}
	}
}

function setNumeric(){
	// var image = $('div#book_entry iframe:first').contents().find('p.imges:last').html();
	// var entry = $("div#book_entry");
	var tmp = "http://chart.apis.google.com/chart?cht=tx&chs=1x0&chl="
	var srcs = $('div#book_entry input#numeric')
	// var preview = document.getElementById("num_prev")
	// preview.src = tmp + srcs.val();
	// images_preview
	$('div#book_entry #num_prev').remove()
	// $('div#book_entry #images_preview').append("OK")
	var vals = srcs.val();
	vals = vals.replace(/\+/g,"%2B")
	$('div#book_entry #images_preview').append('<img id="num_prev" alt="numeric" src="http://chart.apis.google.com/chart?cht=tx&chs=1x0&amp;chl='+ vals +'"/>')
	// $('div#book_entry #num_prev').after('<img id="num_prev" alt="numeric" src="http://chart.apis.google.com/chart?cht=tx&amp;chs=1x0&amp;chl=x = \frac{-b \pm \sqrt {b^2-4ac}}{2a}">')
// 
	// alert(preview.src)
	// .each(function (index, domEle){
	// 	doms = []
	// 	doms = domEle.src.split("/")
	// 	// alert(doms[8]+":"+doms[9])
	// 	domEle.src = doms[8]+"/"+doms[9]
	// });}
}

function post_numeric(id){
	show_save();
	$("img#loading").show();
	// var entry = $("div#book_entry");
	var srcs = $('div#book_entry input#numeric')
	var vals = srcs.val();
	vals = vals.replace(/\+/g,"%2B")
	$.ajax({
		 type: "POST",
		 url: "/isreport/upload_numeric",
		 data: "entryid="+id+"&numeric="+vals,
		 success: function(html){
		document.getElementById("book_entry").innerHTML = html;
		// entry.center();
		// entry.show();
			setTimeout("hide_save()",1500);
		 },
		 complete: function(){
	　　 },
	 });
	
}

function set_abst(ev){
	abstract = document.getElementById("p_abstract");
	preview_frame.document.getElementById("abstract_content").innerHTML = abstract.value;
}
function set_date(ev){
	publish_at = document.getElementById("p_date");
	preview_frame.document.getElementById("date").innerHTML = publish_at.value;
	// copy rightの年を書き換え
	var year = publish_at.value.split("年")[0];
	$('iframe:first').contents().find('span.copy_date').html(year);
}
function setdraft(){
	document.getElementById("entry_isdraft").value = "True";
}
function convert(){
	if(edit == null || preview == null) return;
	
	if(is_pre){
		var texts = ""
		// wiki += "* "+title.value+"\n"
		// wiki += "* "+abstract.value+"\n"
		// wiki += "* "+number.value+"\n"
		// wiki += "* "+authors.innerHTML+"\n"
		// wiki += "* "+publish_at.value+"\n"
		texts = String._unescapeHTML(edit.value);
		
		hatena.parse(texts,false);
		preview_html.innerHTML = hatena.html();
	}
}

// $(function(){
//		 $('#conversion').click(function() {
// 	var formatter = new Wiki.Formatter();
// 	alert($("#soup_text").val());
// 	var srcText = ""
// 	srcText = $("#soup_text").val();
// 	document.getElementById('wiki_preview').innerHTML = formatter.format(srcText);
//		 });
// });


function resize_textarea(ev){
	//if (ev.keyCode != 13) return;
	var textarea = ev.target || ev.srcElement;
	var value = textarea.value;
	var lines = 1;
	for (var i = 0, l = value.length; i < l; i++){
		if (value.charAt(i) == '\n') lines++;
	}
	textarea.setAttribute("rows", lines);
	// window.status = lines;
}
// function autofit(el){
//	if(el.scrollHeight > el.offsetHeight){
//	 el.style.height = el.scrollHeight + 'px';
//	} else {
//	 while (el.scrollHeight - 50 < parseInt(el.style.height)){
//		el.style.height = parseInt(el.style.height) - 50 + 'px';
//	 }
//	 arguments.callee(el);
//	}
//	el.focus();
// }

// $('textarea.flexarea').autoResize({
//		 // On resize:
//		 onResize : function() {
//				 $(this).css({opacity:0.8});
//		 },
//		 // After resize:
//		 animateCallback : function() {
//				 $(this).css({opacity:1});
//		 },
//		 // Quite slow animation:
//		 animateDuration : 300,
//		 // More extra space:
//		 extraSpace : 20
// });


// function get_preview(){
// 	alert("A")
// }

// やっぱやめ
function setting_item(elem){
	$("#"+elem.id)
}

function check_submit(event){
	// if(title && abstract && number && authors && publish_at){
		// alert($('iframe:first').contents().find("body").html())
		is_pre = true;
		convert();
		// imageタグが絶対パスなので無理矢理相対パスに書き換え．運用ドメインによっては正しく動作しないかも
		$('iframe#preview').contents().find("img").each(function (index, domEle){
			doms = []
			doms = domEle.src.split("/")
			// alert(doms[8]+":"+doms[9])
			    //			domEle.src = doms[8]+"/"+doms[9]
			    if(doms[10]){
				domEle.src = doms[9]+"/"+doms[10]
			    }else{
				domEle.src = doms[8]+"/"+doms[9]
				    }
		});
		var htmls = $('iframe#preview').contents().find("body").html();
		// htmls.replace('src="/report/','')
		$("input#html_body").val(htmls);
		return true;
	// }else{
	// 	alert("未入力の項目があります");
	// 	return false;
	// }
}
function check_submit2(event){
	title = document.getElementById("p_title").value;
	number = document.getElementById("p_number").value;//number.value
	// authors = document.getElementById("entry_authors").value;
	// abstract = document.getElementById("p_abstract").innerHTML;
	publish_at = document.getElementById("p_date").value;
	// alert(title+":"+number+":"+authors+":"+abstract+":"+publish_at)
	// if(title && abstract && number && authors && publish_at){
	if(title && number && publish_at){
		return true;
	}else{
		alert("未入力の項目があります");
		return false;
	}
}

function saveNow(id){
	is_pre = true;
	convert();
	// imageタグが絶対パスなので無理矢理相対パスに書き換え．運用ドメインによっては正しく動作しないかも
	$('iframe#preview').contents().find("img").each(function (index, domEle){
		doms = []
		doms = domEle.src.split("/")
		// alert(doms[8]+":"+doms[9])
		domEle.src = doms[8]+"/"+doms[9]
	});
	var htmls = $('iframe#preview').contents().find("body").html();
	var soups = $("#soup_text").val();
	show_save();
	// htmls.replace('src="/report/','')
	// $("input#html_body").val(htmls);
	// alert(htmls);
	var data = {id:id,html_body:htmls,soups:soups};
	$.ajax({
		 type: "POST",
		 url: "/isreport/ajax_save",
		 data: data,
		 success: function(html){
			setTimeout("hide_save()",1500);
			// alert("save")
			// $("#fav_"+$fav_target).removeClass("star");
			// $("#fav_"+$fav_target).addClass("non_fav");
		 },
		 complete: function(){	
	　　 },
	 });
}
function show_save () {
	var entry = $("img#ajax_load");
	entry.center();
	entry.show();
}

function hide_save () {
	var entry = $("img#ajax_load");
	entry.hide();
}

function setfunc(func){
	var results = "";
	switch(func){
		case "save":
			var id = $("input#entry_ids")[0].value
			saveNow(id);
			break;
		case "table":
			results = "[["+(tb_num+1)+"]]を参照\n$| caption\n|*a|*b|\n|c|d|\n";
			break;
		case "bold":
			// results = "<span style='font-weight:bold;'></span>";
			results = "<b></b>";
			break;
		case "italic":
			// results = "<span style='font-style:italic;'></span>";
			results = "<i></i>";
			break;
		case "color":
			results = '<span style="color:#CC0000;"></span>';
			break;
		case "comment":
			results = "脚注((または註釈など))\n";
			break;
		case "del":
			results = "<del></del>";
			break;
		case "sup":
			results = "<sup></sup>";
			break;
		case "sub":
			results = "<sub></sub>";
			break;
		case "resize":
			results = '<span style="font-size:150%;"></span>';
			break;
		case "list":
			results = "+ list\n";
			break;
		case "olist":
			results = "- list\n";
			break;
		case "block":
			results = "{{"+(fig_num+1)+"}}を参照\n>?\nblockquate\n?<\n$% caption\n";
			break;
		case "image":
			// results = '<img alt="" src="image/open.png" width="50%"></img>\n';
			var id = $("input#entry_ids")[0].value
			// alert(id)
			inner_img(id);
			break;
		case "numeric":
			// results = '<img alt="" src="image/open.png" width="50%"></img>\n';
			var id = $("input#entry_ids")[0].value
			// alert(id)
			inner_numeric(id);
			break;
		case "h1":
			results = "* section\n";
			break;
		case "h2":
			results = "** sub section\n";
			break;
		case "h3":
			results = "*** subsub section\n";
			break;
		case "block":
			results = "{{}}\n";
			break;
		case "cite":
			// results = "citer((citee))\n";
			results = "{=1=}\n";
			edit.value += '\n# reference<br /><a href="http://is.doshisha.ac.jp/isreport/isdlstyle" target="_blank">http://is.doshisha.ac.jp/isreport/isdlstyle</a>';
			break;
	}
	// <a onClick="setfunc('table')">table</a>
	// <a onClick="setfunc('list')">list</a>
	// <a onClick="setfunc('image')">image</a>
	// <a onClick="setfunc('h1')">h1</a>
	// <a onClick="setfunc('h2')">h2</a>
	// <a onClick="setfunc('h3')">h3</a>
	// <a onClick="setfunc('block')">block</a>
	// <a onClick="setfunc('cite')">cite</a>
	// document.getElementById("debb").innerHTML = edit.value;
	
	// カーソル位置を取得して挿入
	edit.focus();
	if (jQuery.browser.msie) {
		var r = document.selection.createRange();
		r.text = results;
		r.select();
	} else {
		var s = edit.value;
		var p = edit.selectionStart;
		var np = p + results.length;
		edit.value = s.substr(0, p) + results + s.substr(p);
		edit.setSelectionRange(np, np);
	}
	// edit.value += results;
	convert();
}

function fav_click(thisis){
	var $fav_target = $(thisis).attr("id").split("_")[1]
	if($(thisis).hasClass("star")){
		// alert($fav_target)
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

var tag_num=1;
function paste_image(image,count){
	if(image){
		var results = '{{'+count+'}}を参照\n'
		results += '%%'+image+'/400\n$% caption\n'
		// カーソル位置を取得して挿入
		edit.focus();
		if (jQuery.browser.msie) {
			var r = document.selection.createRange();
			r.text = results;
			r.select();
		} else {
			var s = edit.value;
			var p = edit.selectionStart;
			var np = p + results.length;
			edit.value = s.substr(0, p) + results + s.substr(p);
			edit.setSelectionRange(np, np);
		}
		convert();
		book_form_cancel();
	}else{
		alert("ファイルが選択されていません")
	}
}function paste_img(){
	// alert($('div#book_entry iframe:first').contents().find('p.imges:last').html())
	// .find('pre.copyright').prepend('<span class="copy_author">Copyright&nbsp;(C)&nbsp;<span class="copy_date">2010</span>&nbsp;'+auths[i]+',&nbsp;All&nbsp;rights&nbsp;reserved.<span>\n');
	var image = $('div#book_entry iframe:first').contents().find('div.fignum:last').html();
	if(image){
		// edit.value += '<div class="img_div"><img alt="'+image+'" src="images/'+image+'" width="300" />\n<label>Fig.1 hoge</label>\n</div>\n';
		var results = '{{'+tag_num+'}}を参照\n'
		results += '%%'+image+'/400\n$% caption\n'
		tag_num +=1;
		// カーソル位置を取得して挿入
		edit.focus();
		if (jQuery.browser.msie) {
			var r = document.selection.createRange();
			r.text = results;
			r.select();
		} else {
			var s = edit.value;
			var p = edit.selectionStart;
			var np = p + results.length;
			edit.value = s.substr(0, p) + results + s.substr(p);
			edit.setSelectionRange(np, np);
		}
		// edit.value += results;
		convert();
		book_form_cancel();
	}else{
		alert("ファイルが選択されていません")
	}
}
function paste_figures(nume){
	var image = $('div#book_entry iframe:first').contents().find('div.fignum:last').html();
	if(image){
		paste_nume(image,1,nume)
	}else{
		alert("ファイルが選択されていません")
	}
}
function paste_nume(nume,num,is_nume){
	if(nume){
		if(is_nume){
			var nu = parseInt(num)+1
			var results = '<img class="inner_nume" alt="'+nume+'" src="/report/'+dirpath+'/images/'+nume+'"/>'
			// edit.value += '&&'+nume+'/200\n'
		}else{
			var nu = parseInt(num)+1
			var results = '(='+nu+'=)を参照\n'
			results += '&&'+nume+'/200\n'
		}
		// カーソル位置を取得して挿入
		edit.focus();
		if (jQuery.browser.msie) {
			var r = document.selection.createRange();
			r.text = results;
			r.select();
		} else {
			var s = edit.value;
			var p = edit.selectionStart;
			var np = p + results.length;
			edit.value = s.substr(0, p) + results + s.substr(p);
			edit.setSelectionRange(np, np);
		}
		convert();
		book_form_cancel();
	}else{
		alert("ファイルが選択されていません")
	}
}
function show_img(id){
	show_save();
	var entry = $("div#book_entry");
	$.ajax({
		 type: "GET",
		 url: "/isreport/image_list",
		 data: "entryid="+id,
		 success: function(html){
			document.getElementById("book_entry").innerHTML = html;
			entry.screen();
			entry.center();
			entry.show();
			hide_save();
		 },
		 complete: function(){
	　　 },
	 });
	hide_save();
	// $.ajax({
	//		type: "GET",
	//		url: "/isreport/get_books_form",
	//		data: "id="+$fav_target,
	//		success: function(html){
	// <p><input type="submit" value="式貼り付け" onClick='paste_nume("{{file}}","{{forloop.counter}}","")'><input type="submit" value="文中貼り付け" onClick='paste_nume("{{file}}","{{forloop.counter}}","True")'><input type="submit" value="削除" onClick='delete_img("{{file}}","{{entry.id}}")'></p>
	// html='<div class="frame_div"><a onclick="book_form_cancel()" href="#close" class="close_button">×</a><iframe name="upload_frame" id="upload_frame" src="/isreport/upload_img?entryid='+id+'">iframe対応環境でご覧頂けます</iframe></div><div class="frame_submit"><input type="submit" value="図として貼り付け" onClick="paste_img()" /><input type="submit" value="式として貼り付け" onClick="paste_figures(false)" /><input type="submit" value="文中貼り付け" onClick="paste_figures(true)" /><input type="submit" value="イメージ一覧表示" onClick="show_img('+id+')" /><input type="submit" value="閉じる" onClick="book_form_cancel()" /></div>'
	// document.getElementById("book_entry").innerHTML = html;
	// entry.screen();
	// entry.center();
	// entry.show();
}
function delete_img(nume,id){
	if(nume){
		$("img#loading").show();
		var entry = $("div#book_entry");
		$.ajax({
			 type: "POST",
			 url: "/isreport/delete_img",
			 data: "entryid="+id+"&img="+nume,
			 success: function(html){
			document.getElementById("book_entry").innerHTML = html;
			entry.center();
			entry.show();
			 },
			 complete: function(){
		　　 },
		 });
		
	}
}


function inner_img(id){
	show_save();
	var entry = $("div#book_entry");
	// $.ajax({
	//		type: "GET",
	//		url: "/isreport/get_books_form",
	//		data: "id="+$fav_target,
	//		success: function(html){
	// <p><input type="submit" value="式貼り付け" onClick='paste_nume("{{file}}","{{forloop.counter}}","")'><input type="submit" value="文中貼り付け" onClick='paste_nume("{{file}}","{{forloop.counter}}","True")'><input type="submit" value="削除" onClick='delete_img("{{file}}","{{entry.id}}")'></p>
	html='<div class="frame_div"><a onclick="book_form_cancel()" href="#close" class="close_button">×</a><iframe name="upload_frame" id="upload_frame" src="/isreport/upload_img?entryid='+id+'">iframe対応環境でご覧頂けます</iframe></div><div class="frame_submit"><input type="submit" value="図として貼り付け" onClick="paste_img()"><input type="submit" value="式として貼り付け" onClick="paste_figures(false)"><input type="submit" value="文中貼り付け" onClick="paste_figures(true)"><input type="submit" value="イメージ一覧表示" onClick="show_img('+id+')"><input type="submit" value="数式作成" onClick="setfunc(\'numeric\')"><input type="submit" value="閉じる" onClick="book_form_cancel()"></div>'
	document.getElementById("book_entry").innerHTML = html;
	entry.screen();
	entry.center();
	entry.show();
	hide_save();
	// setTimeout("hide_save()",1500);
	//		},
	//		complete: function(){
	// 　　 },
	//	});
}

function inner_numeric(id){
	var entry = $("div#book_entry");
	// html='<div class="frame_div"><iframe name="upload_frame" id="upload_frame" src="/isreport/upload_numeric?entryid='+id+'">iframe対応環境でご覧頂けます</iframe></div><div class="frame_submit"><input type="submit" value="貼り付ける" onClick="paste_img()"><input type="submit" value="閉じる" onClick="book_form_cancel()"></div>'
	// document.getElementById("book_entry").innerHTML = html;
	$.ajax({
		 type: "GET",
		 url: "/isreport/upload_numeric",
		 data: "entryid="+id,
		 success: function(html){
			document.getElementById("book_entry").innerHTML = html;
			entry.screen();
			entry.center();
			entry.show();
		 },
		 complete: function(){
	　　 },
	 });
}


// $("a.addbook").click(function () {
function addbook(thisis){
	var $fav_target = $(thisis).attr("id").split("_")[1];
	var entry = $("div#book_entry");
	$.ajax({
		 type: "GET",
		 url: "/isreport/get_books_form",
		 data: "id="+$fav_target,
		 success: function(html){
			document.getElementById("book_entry").innerHTML = html;
			entry.center();
			entry.show();
		 },
		 complete: function(){
	　　 },
	 });
	
}
// );

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

$("a.addtag").click(function () {
	// alert("OK")
	// var $target = $(this).closest('span').after("OK")
	// var $fav_target = $(this).attr("id").split("_")[1];
	// var entry = $("div#book_entry");
	// $.ajax({
	//		type: "GET",
	//		url: "/get_books_form",
	//		data: "id="+$fav_target,
	//		success: function(html){
	// 		document.getElementById("book_entry").innerHTML = html;
	// 		entry.center();
	// 		entry.show();
	//		},
	//		complete: function(){
	// 　　 },
	//	});
	
});