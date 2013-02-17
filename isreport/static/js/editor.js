var edit, preview, preview_html, source, sel;
var hatena;
var realtime = true;
var title, abstract, number, authors, publish_at;
var is_pre = true;
function execute(targets) {
  MathJax.Hub.Queue(["Typeset", MathJax.Hub,targets]);
}
jQuery.fn.center = function () { // 680 250 536
		var tops = 100 //($(window).height() - this.height() ) / 2+$(window).scrollTop()-150;
		if(tops>$(window).height()){tops=0;}
		this.css("top",	tops + "px");
		this.css("left", ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px");
		return this;
}
jQuery.fn.set_pos = function(xx,yy){
	this.css("position","absolute");
	this.css("top", yy + "px");
	this.css("left", xx + "px");
	this.css("z-index","1000");
	return this;
}
jQuery.fn.set_center = function(){
	var wx = $(window).width();
	var wy = $(window).height();
	this.css("position","absolute");
	// this.css("margin","10px auto");
	this.css("top", wx/2+100 + "px");
	this.css("left", wy/2+100 + "px");
	this.css("z-index","1000");
	return this;
}
function set_full_editor(){
	// create_curtain();
	$("#entry_editor_wrap").toggleClass("white_curtain");
	$("#entry_editor_wrap").toggleClass("full_editor");
}
function hide_curtain(){
	$("#curtain").remove();
}
function create_curtain(){
	var frame_tmp = "<div class='curtain' id='curtain'></div>";
	var windows = $("#wrapper");
	windows.append(frame_tmp);
	// $('.curtain').click(function(){
	// 	hide_curtain();
	// });
}
function create_frame(frame_id,types){
	var windows = $("#curtain");
	if(windows){
		hide_curtain()
	}
	create_curtain();
	var frame_tmp = "";
	var urls = "/static/html/inner_"+types+".html";
	if(types=="img"){
		urls = "/isreport/ajax/img?id="+$("input#entry_ids")[0].value;
	}
	else if(types=="nume"){
		urls = "/isreport/ajax/nume?id="+$("input#entry_ids")[0].value;
	}
	$.ajax({
		type: "get",
		url: urls,
		success: function(text){
			frame_tmp = "<div class='movable'><a class='hide_button' href='#' onclick='hide_curtain()'>×</a>"+text+"</div>";
			windows = $("#curtain");
			windows.append(frame_tmp);
		}
	});
}
function init(){
	edit = document.getElementById("soup_text");
	preview = document.getElementById("preview");
	preview_html = preview_frame.document.getElementById("content");
	dirpath=document.getElementById("dirpath").value;
	hatena = new Hatena();
	edit.onkeyup = function(){if(realtime) convert();};
	convert();
}
function init_content(){
	preview = document.getElementById("report_html");
	edit = document.getElementById("report_org_html");
	dirpath=document.getElementById("dirpath").value;
	var texts = String._unescapeHTML(edit.value);
	is_pre = true;
	hatena = new Hatena();
	hatena.parse(texts,false);
	var hh = hatena.html();
	if(hh){
		preview.innerHTML = hh;
	}
	// execute(preview);
}
function is_preview(elem){
	is_pre = elem.checked;
}
function saveNow(id){
	is_pre = true;
	convert();
	// imageタグが絶対パスなので無理矢理相対パスに書き換え．運用ドメインによっては正しく動作しないかも
	$('iframe#preview').contents().find("img").each(function (index, domEle){
		doms = []
		doms = domEle.src.split("/")
		// domEle.src = doms[8]+"/"+doms[9]
		if(doms[10]){
			domEle.src = doms[9]+"/"+doms[10]
		}else{
			domEle.src = doms[8]+"/"+doms[9]
		}
	});
	var htmls = $('iframe#preview').contents().find("body").html();
	var soups = $("#soup_text").val();
	show_save();
	var data = {id:id,html_body:htmls,soups:soups};
	$.ajax({
		 type: "POST",
		 url: "/isreport/ajax_save",
		 data: data,
		 success: function(html){
			setTimeout("hide_save()",1500);
		},
		complete: function(){	
		},
		error: function(){
			hide_save();
			alert("サーバエラー\nネットワークへの接続を確認してください\nもしくは一度下書き保存を行って下さい．新規登録状態のレポートはこちらからセーブできません．");
		},
	});
}
function show_save() {
	var entry = $("img#ajax_load");
	entry.center();
	entry.show();
}

function hide_save() {
	var entry = $("img#ajax_load");
	entry.hide();
}
function setfunc(func){
	var results = "";
	switch(func){
		case "save":
			var id = $("input#entry_ids")[0].value;
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
		case "link":
			results = "<a href='hoge'>hoge</a>";
			break;
		case "backcolor":
			results = "<span style=\"background-color:#CCCCFC;\"></span>";
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
			results = "{{"+(fig_num+1)+"}}を参照\n>?\nblock\n?<\n$% caption\n";
			break;
		case "blockquote":
			results = "\n<blockquote>\nblockquate\n</blockquote>\n";
			break;
		case "image":
			// results = '<img alt="" src="image/open.png" width="50%"></img>\n';
			var id = $("input#entry_ids")[0].value
			// alert(id)
			create_frame("wrapper","img");
			break;
		case "numeric":
			// results = '<img alt="" src="image/open.png" width="50%"></img>\n';
			var id = $("input#entry_ids")[0].value
			// alert(id)
			//create_frame("wrapper","nume");
			results = "$Q_0=t$\n";
			break;
		case "hr":
			results = "<hr />\n";
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
			edit.value += '\n# reference<br />http://is.doshisha.ac.jp/isreport/';
			break;
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
}
function setdraft(){
	document.getElementById("entry_isdraft").value = "True";
}
function setlang(){
	document.getElementById("entry_istranslate").value = "True";
}
function convert(){
	if(edit == null || preview == null) return;
	if(is_pre){
		var texts = ""
		texts = String._unescapeHTML(edit.value);
		hatena.parse(texts,false);
		preview_html.innerHTML = hatena.html();
		// execute(preview_html);
	}
}
var tag_num=1;
function paste_img(){
	var image = $('div#book_entry iframe:first').contents().find('div.fignum:last').html();
	if(image){
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
		hide_curtain();
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
function setNumeric(){
	var tmp = "http://chart.apis.google.com/chart?cht=tx&chs=1x0&chl="
	var srcs = $('input#numeric')
	$('#num_prev').remove()
	var vals = srcs.val();
	vals = vals.replace(/\+/g,"%2B")
	$('#images_preview').append('<img id="num_prev" alt="numeric" src="http://chart.apis.google.com/chart?cht=tx&chs=1x0&amp;chl='+ vals +' "/>')
}
function paste_nume(nume,num,is_nume){
	if(nume){
		if(is_nume){
			var nu = parseInt(num)+1
			var results = '<img class="inner_nume" alt="'+nume+'" src="/report/'+dirpath+'/images/'+nume+'" />'
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
		hide_curtain();
	}else{
		alert("ファイルが選択されていません")
	}
}
function post_numeric(id){
	show_save();
	$("img#loading").show();
	var srcs = $('input#numeric')
	var vals = srcs.val();
	vals = vals.replace(/\+/g,"%2B")
	$.ajax({
		 type: "POST",
		 url: "/isreport/ajax/upload_numeric",
		 data: "id="+id+"&numeric="+vals,
		 success: function(html){
		document.getElementById("book_entry").innerHTML = html;
			setTimeout("hide_save()",1500);
		 },
		 complete: function(){
	　　 },
	 });
	
}
function show_img(id){
	show_save();
	var entry = $("div#book_entry");
	$.ajax({
		 type: "GET",
		 url: "/isreport/ajax/image_list",
		 data: "id="+id,
		 success: function(html){
			document.getElementById("book_entry").innerHTML = html;
			// entry.screen();
			// entry.center();
			// entry.show();
			hide_save();
		 },
		 complete: function(){
	　　 },
	 });
	hide_save();
}
function delete_img(nume,id){
	if(nume){
		$("img#loading").show();
		var entry = $("div#book_entry");
		$.ajax({
			 type: "POST",
			 url: "/isreport/delete_img",
			 data: "id="+id+"&img="+nume,
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
$(document).ready(function(){
	$(".utils").hover(
		function(){
			$("#hov_text").text($(this).attr("title"));
		}
	);
})