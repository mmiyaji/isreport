// hatena.js 改変
// 2010/08/13


var section_num;
var subsection_num;
var subsubsection_num;
var fig_num;
var tb_num;
var nume_num;
var fig_nums = Array()
var dirpath = "";
var def_url = "http://is.doshisha.ac.jp";
var aparse_flg = false;
// from prototype.js
Object.extend = function(destination, source) {
  for (property in source) {
	destination[property] = source[property];
  }
  return destination;
}

String.times = function(str, time){
	var s = "";
	for(var i = 0; i < time; i++)s += "\t";
	return s;
}

String._escapeHTML = function(s){
	s = s.replace(/\&/g, "&amp;");
	s = s.replace(/</g, "&lt;");
	s = s.replace(/>/g, "&gt;");
	s = s.replace(/"/g, "&quot;");
	s = s.replace(/\'/g, "&#39");
	s = s.replace(/\\/g, "&#92");
	return s;
}
String._unescapeHTML = function(s){
	s = s.replace(/&amp;/g, "&");
	s = s.replace(/&lt;/g, "<");
	s = s.replace(/&gt;/g, ">");
	s = s.replace(/&quot;/g, "\"");
	return s;
}
// Hatena::Hatena_HTMLFilter
Hatena_HTMLFilter = function(args){
	this.self = {
		context : args["context"],
		html : '',
	};
	this.init();
}
Hatena_HTMLFilter.prototype = {
	init :function(){
		// HTML::Parser を利用すべきなんだけど JavaScript ではなんとも...
	},

	parse : function(html){
		var c = this.self.context;
		this.self.html = c.self.texthandler(html, c);
	},
	html : function(){
		return this.self.html;
	}
}

// Hatena
Hatena = function(args){
	if(args == null) args = {};
	this.self = {
		html : '',
		baseuri : args["baseuri"],
		permalink : args["permalink"] || "",
		ilevel : args["ilevel"] || 0,
		invalidnode : args["invalidnode"] || [],
		sectionanchor : args["sectionanchor"] || '',
		texthandler : args["texthandler"] || function(text, c){
			// footnote
			var p = c.self.permalink;
			var html = "";
			var foot = text.split("((");
			for(var i = 0; i < foot.length; i++){
				if(i == 0){
					html += foot[i];
					continue;
				}
				var s = foot[i].split("))", 2);
				if(s.length != 2){
					html += "((" + foot[i];
					continue;
				}
				var pre = foot[i - i];
				var note = s[0];
				var post = foot[i].substr(s[0].length + 2);
				if(pre.match(/\)$/) && post.match(/^\(/)){
					html += "((" + post;
				} else {
					var notes = c.footnotes(note);
					var num = notes.length;
					note = note.replace(/<.*?>/g, "");
					note = note.replace(/&/g, "&amp;");
					html += '<span class="footnote"><a href="' + p + '#f' + num + '" title="' + note + '" name="fn' + num + '">*' + num + '</a></span>' + post;
				}
			}
			// figure
			var fig = html.split("{{");
			// alert(fig[1])
			html = "";
			for(var i = 0; i < fig.length; i++){
				if(i == 0){
					html += fig[i];
					continue;
				}
				var s = fig[i].split("}}", 2);
				if(s.length != 2){
					html += "{{" + fig[i];
					continue;
				}
				var pre = fig[i - i];
				var note = s[0];
				var post = fig[i].substr(s[0].length + 2);
				if(pre.match(/\}$/) && post.match(/^\{/)){
					html += "{{" + post;
				} else {
					note = note.replace(/<.*?>/g, "");
					note = note.replace(/&/g, "&amp;");
					html += '<span class="figures"><a href="#figure' + note + '" title="figure' + note + '" name="fig' + note + '">Fig.' + note + '</a></span>' + post;
				}
			}
			// table
			var tb = html.split("[[");
			// alert(fig[1])
			html = "";
			for(var i = 0; i < tb.length; i++){
				if(i == 0){
					html += tb[i];
					continue;
				}
				var s = tb[i].split("]]", 2);
				if(s.length != 2){
					html += "[[" + tb[i];
					continue;
				}
				var pre = tb[i - i];
				var note = s[0];
				var post = tb[i].substr(s[0].length + 2);
				if(pre.match(/\]$/) && post.match(/^\[/)){
					html += "[[" + post;
				} else {
					note = note.replace(/<.*?>/g, "");
					note = note.replace(/&/g, "&amp;");
					html += '<span class="tables"><a href="#table' + note + '" title="table' + note + '" name="tb' + note + '">Table.' + note + '</a></span>' + post;
				}
			}
			// numerical
			var tb = html.split("(=");
			// alert(fig[1])
			html = "";
			for(var i = 0; i < tb.length; i++){
				if(i == 0){
					html += tb[i];
					continue;
				}
				var s = tb[i].split("=)", 2);
				if(s.length != 2){
					html += "(=" + tb[i];
					continue;
				}
				var pre = tb[i - i];
				var note = s[0];
				var post = tb[i].substr(s[0].length + 2);
					note = note.replace(/<.*?>/g, "");
					note = note.replace(/&/g, "&amp;");
					html += '<span class="numeric"><a href="#numeric' + note + '" title="numeric' + note + '" name="nume' + note + '">式(' + note + ')</a></span>' + post;
			}
			// references
			var ref = html.split("{=");
			html = "";
			for(var i = 0; i < ref.length; i++){
				if(i == 0){
					html += ref[i];
					continue;
				}
				var s = ref[i].split("=}", 2);
				if(s.length != 2){
					html += "{=" + ref[i];
					continue;
				}
				var pre = ref[i - i];
				var note = s[0];
				var post = ref[i].substr(s[0].length + 2);
				// var notes = c.references(note);
				// var num = notes.length;
					note = note.replace(/<.*?>/g, "");
					note = note.replace(/&/g, "&amp;");
					// html += '<span class="numeric"><a href="#numeric' + note + '" title="numeric' + note + '" name="nume' + note + '">式(' + note + ')</a></span>' + post;
					html += '<span class="reference"><a href="' + p + '#r' + note + '" title="' + note + '" name="ref' + note + '">[' + note + ']</a></span>' + post;
			}
			return html;
		}
	};
}
Hatena.prototype = {
	parse : function(text,aparse){
		aparse_flg = aparse;
		this.self.context = new Hatena_Context({
			text : text || "",
			baseuri : this.self.baseuri,
			permalink : this.self.permalink,
			invalidnode : this.self.invalidnode,
			sectionanchor : this.self.sectionanchor,
			texthandler : this.self.texthandler
		});
		var c = this.self.context;
		var node = new Hatena_BodyNode();
		node._new({
			context : c,
			ilevel : this.self.ilevel
		});
		node.parse();
		var parser = new Hatena_HTMLFilter({
			context : c
		});
		parser.parse(c.html());
		this.self.html = parser.html();

		if (this.self.context.footnotes().length != 0) {
			var node = new Hatena_FootnoteNode();
			node._new({
				context : this.self.context,
				ilevel : this.self.ilevel
			});
			node.parse();
			this.self.html += "\n";
			this.self.html += node.self.html;
		}
		if (this.self.context.references().length != 0) {
			var node = new Hatena_ReferenceNode();
			node._new({
				context : this.self.context,
				ilevel : this.self.ilevel
			});
			node.parse();
			this.self.html += "\n";
			this.self.html += node.self.html;
		}
		
	}, 

	html : function(){
		return this.self.html;
	}
}


// Hatena::Context
Hatena_Context = function(args){
	this.self = {
		text : args["text"],
		baseuri : args["baseuri"],
		permalink : args["permalink"],
		invalidnode : args["invalidnode"],
		sectionanchor : args["sectionanchor"],
		texthandler : args["texthandler"],
		_htmllines : [],
		footnotes : Array(),
		references : Array(),
		sectioncount : 0,
		syntaxrefs : [],
		noparagraph : 0
	};
	this.init();
}
Hatena_Context.prototype = {
	init : function() {
		section_num=0;
		subsection_num=0;
		subsubsection_num=0;
		fig_num = 0;
		tb_num =0;
		nume_num =0;
		fig_nums = []
		this.self.text = this.self.text.replace(/\r/g, "");
		this.self.lines = this.self.text.split('\n');
		this.self.index = -1;
	},

	hasnext : function() {
		return (this.self.lines != null && this.self.lines.length - 1 > this.self.index);
	},

	nextline : function() {
		return this.self.lines[this.self.index + 1];
	},

	shiftline : function() {
		return this.self.lines[++this.self.index];
	},

	currentline : function() {
		return this.self.lines[this.self.index];
	},

	html : function() {
		return this.self._htmllines.join ("\n");
	},

	htmllines : function(line) {
		if(line != null) this.self._htmllines.push(line);
		return this.self._htmllines;
	},

	lasthtmlline : function() {return this.self._htmllines[this.self._htmllines.length - 1]; },

	footnotes : function(line) {
		if(line != null) this.self.footnotes.push(line);
		return this.self.footnotes;
	},
	references : function(line) {
		if(line != null) this.self.references.push(line);
		return this.self.references;
	},

	syntaxrefs : function(line) {
		if(line != null) this.self.syntaxrefs.push(line);
		return this.self.syntaxrefs;
	},

	syntaxpattern : function(pattern) {
		if(pattern != null) this.self.syntaxpattern = pattern;
		return this.self.syntaxpattern;
	},

	noparagraph : function(noparagraph) {
		if(noparagraph != null) this.self.noparagraph = noparagraph;
		return this.self.noparagraph;
	},

	incrementsection : function() {
		return this.self.sectioncount++;
	}
}


// Hatena::Node
Hatena_Node = function(){}
Hatena_Node.prototype = {
	html : "", 
	pattern : "",

	_new : function(args){
		if(args == null) args = Array();
		this.self = {
			context : args["context"],
			ilevel : args["ilevel"],
			html : ''
		};
		this.init();
	},
	init : function(){
		this.self.pattern = '';
	},

	parse : function(){ alert('die'); },

	context : function(v){
		this.self.context = v;
	}
};


// Hatena::BodyNode
Hatena_BodyNode = function(){};
Hatena_BodyNode.prototype = Object.extend(new Hatena_Node(), {
	parse : function(){
		var c = this.self.context;
		while (this.self.context.hasnext()) {
			var node = new Hatena_SectionNode();
			node._new({
				context : c,
				ilevel : this.self.ilevel
			});
			node.parse();
		}
	}
})


// Hatena::BrNode
Hatena_BrNode = function(){};
Hatena_BrNode.prototype = Object.extend(new Hatena_Node(), {
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l.length != 0) return;
		var t = String.times("\t", this.self.ilevel);
		if (c.lasthtmlline() == t + "<br />" || c.lasthtmlline() == t) {
			c.htmllines(t + "<br />");
		} else {
			c.htmllines(t);
		}
	}
})


// Hatena::CDataNode
Hatena_CDataNode = function(){};
Hatena_CDataNode.prototype = Object.extend(new Hatena_Node(), {
	parse : function(){
		var c = this.self.context;
		var t = String.times("\t", this.self.ilevel);
		var l = c.shiftline();
		var text = new Hatena_Text();
		text._new({context : c});
		text.parse(l);
		l = text.html();
		c.htmllines(t + l);
	}
})


// Hatena::DlNode
Hatena_DlNode = function(){};
Hatena_DlNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\:((?:<[^>]+>|\[\].+?\[\]|\[[^\]]+\]|\[\]|[^\:<\[]+)+)\:(.+)$/;
	},

	parse : function(){
		var c = this.self.context;
		var l = c.nextline();
		if(!l.match(this.self.pattern)) return;
		this.self.llevel = RegExp.$1.length;
		var t = String.times("\t", this.self.ilevel);

		c.htmllines(t + "<dl>");
		while (l = c.nextline()) {
			if(!l.match(this.self.pattern)) break;
			c.shiftline();
			c.htmllines(t + "\t<dt>" + RegExp.$1 + "</dt>");
			c.htmllines(t + "\t<dd>" + RegExp.$2 + "</dd>");
		}
		c.htmllines(t + "</dl>");
	}
})


// Hatena::FootnoteNode
Hatena_FootnoteNode = function(){};
Hatena_FootnoteNode.prototype = Object.extend(new Hatena_Node(), {
	html : "",

	parse : function(){
		var c = this.self["context"];
		if(c.self.footnotes == null || c.self.footnotes.length == 0) return;
		var t = String.times("\t", this.self["ilevel"]);
		var p = c.self.permalink;
		this.self["html"] = '';

		// this.self.html += t + '</div><div class="footnote"><h3 class="section"><a href="#ref" name="ref"><span class="sanchor"></span></a>References</h3>' + '<div class="reference_content">';
		// this.self.html += t + '</div><div class="footnote"><h3 class="section">References</h3>' + '<div class="reference_content">';
		// this.self.html += t + '</div><div class="footnote"><h3 class="section">Footnote</h3>' + '<div class="footnote_content">';
		this.self.html += t + '</div><div class="footnote"><h3 class="section">注)</h3>' + '<div class="footnote_content">';
		// this.self.html += t + '</div><div class="footnote">';
		var num = 0;
		var text = new Hatena_Text();
		text._new({context : c});
		for(var i = 0; i < c.self.footnotes.length; i++) {
			var note = c.self.footnotes[i];
			num++;
			text.parse(note);
			var l = t + '\t<p class="footnote"><a href="' + p + '#fn' + num + '" name="f' + num + '">*' + num + '</a>: '
				+ text.html() + '</p>';
			this.self["html"] += l + "\n";
		}
		this.self["html"] += t + '</div></div>\n';
	}
})
// Hatena::ReferenceNode
Hatena_ReferenceNode = function(){};
Hatena_ReferenceNode.prototype = Object.extend(new Hatena_Node(), {
	html : "",

	parse : function(){
		var c = this.self["context"];
		if(c.self.references == null || c.self.references.length == 0) return;
		var t = String.times("\t", this.self["ilevel"]);
		var p = c.self.permalink;
		this.self["html"] = '';

		// this.self.html += t + '</div><div class="footnote"><h3 class="section"><a href="#ref" name="ref"><span class="sanchor"></span></a>References</h3>' + '<div class="reference_content">';
		this.self.html += t + '</div><div class="reference"><h3 class="section">References</h3>' + '<div class="reference_content"><ul id="reference_list">';
		// this.self.html += t + '</div><div class="footnote">';
		var num = 0;
		var text = new Hatena_Text();
		text._new({context : c});
		for(var i = 0; i < c.self.references.length; i++) {
			var note = c.self.references[i];
			num++;
			text.parse(note);
			var l = t + '\t<li><a href="' + p + '#ref' + num + '" name="r' + num + '">[' + num + ']</a> '
				+ text.html() + '</li>';
			this.self["html"] += l + "\n";
		}
		this.self["html"] += t + '</ul></div></div>\n';
	}
})

// Hatena::H3Node
Hatena_H3Node = function(){};
Hatena_H3Node.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\*(?:(\d{9,10}|[a-zA-Z]\w*)\*)?((?:\[[^\:\[\]]+\])+)?(.*)$/;
	},
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var name = RegExp.$1;
		var cat = RegExp.$2;
		var title = RegExp.$3;
		var b = c.self.baseuri;
		var p = c.self.permalink;
		var t = String.times("\t", this.self.ilevel);
		var sa = c.self.sectionanchor;

		/* TODO: カテゴリは未対応
		if (cat) {
			if(cat.match(/\[([^\:\[\]]+)\]/)){ // 繰り返しできないなぁ...
				var w = RegExp.$1;
				var ew = escape(RegExp.$1);
				cat = cat.replace(/\[([^\:\[\]]+)\]/, '[<a class="sectioncategory" href="' + b + '?word=' + ew + '">' + w + '</a>]');
			}
		}*/
		var extra = '';
		var ret = this._formatname(name);
		var name = (ret[0] != undefined ? ret[0] : ""); extra = (ret[1] != undefined ? ret[1] : "");
		section_num+=1;
		subsection_num=0;
		subsubsection_num=0;
		div = "";
		if(section_num!=1){
			div = '</div>';
		}
		// c.htmllines(t + '<h3><a href="' + p + '#' + name + '" name="' + name + '"><span class="sanchor">' + sa + '</span></a> ' + cat + title + '</h3>' + extra);
		// c.htmllines(t + '<h3 class="section">'+section_num+' <a href="' + p + '#' + name + '" name="' + name + '"><span class="sanchor">' + sa + '</span></a> ' + cat + title + '</h3>' + extra);
		// c.htmllines(div + t + '<h3 class="section">'+section_num+'&nbsp;&nbsp;<a href="' + p + '#' + name + '" name="' + name + '"><span class="sanchor">' + sa + '</span></a> ' + cat + title + '</h3>' + extra + '<div class="section_content">');
		c.htmllines(div + t + '<h3 class="section" name="section'+section_num+'">'+section_num+'&nbsp;&nbsp;' + title + '</h3>' + extra + '<div class="section_content">');
	},

	_formatname : function(name){
		/* TODO: 時間も未対応。表示時の時間が表示されてしまう...
		if (name && name.match(/^\d{9,10}$/)) {
			var m = sprintf('%02d', (localtime($name))[1]);
			var h = sprintf('%02d', (localtime($name))[2]);
			return (
				$name,
				qq| <span class="timestamp">$h:$m</span>|,
			);
		} elsif ($name) {*/
		if(name != ""){
			return [name];
		} else {
			this.self.context.incrementsection();
			name = 'p' + this.self.context.self.sectioncount;
			return [name];
		}
	}
})


// Hatena::H4Node
Hatena_H4Node = function(){};
Hatena_H4Node.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\*\*((?:[^\*]).*)$/;
	},

	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		subsection_num+=1;
		subsubsection_num=0;
		c.htmllines("</div>" + t + "<h4 class='subsection' name='subsection"+section_num+"."+subsection_num+"'>"+section_num+"."+subsection_num+"&nbsp;&nbsp;"+ RegExp.$1 + "</h4>" + '<div class="subsection_content">');
	}
})


// Hatena::H5Node
Hatena_H5Node = function(){};
Hatena_H5Node.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\*\*\*((?:[^\*]).*)$/;
	},

	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		subsubsection_num+=1;
		c.htmllines("</div>" + t + "<h5 class='subsubsection' name='subsubsection"+section_num+"."+subsection_num+"."+subsubsection_num+"'>" +section_num+"."+subsection_num+"."+subsubsection_num+"&nbsp;&nbsp;"+ RegExp.$1 + "</h5>" + '<div class="subsubsection_content">');
	}
})

// IMG node
// Hatena::H6Node
Hatena_H6Node = function(){};
Hatena_H6Node.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\%\%((?:[^\*]).*)$/;
	},
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		var content = String(RegExp.$1).split("/")
		// fig_nums.push(content[1])
		// c.htmllines("<h4 class='subsection'>"+section_num+"."+subsection_num+"&nbsp;&nbsp;"+ RegExp.$1 + "</h4>" + '<div class="subsection_content">');
		// c.htmllines('<div class="img_div"><img alt="'+content[0]+'" src="images/'+content[0]+'" width="'+content[2]+'" />\n<p><label><a href="#fig' + content[1] + '" name="figure' + content[1] + '">Fig.' + fig_num + '</a>&nbsp;'+content[3]+'</label></p>\n</div>\n');
		var urls = "";
		if(aparse_flg){
			urls = def_url;
		}
		c.htmllines('<div class="img_div"><img alt="'+content[0]+'" src="'+urls+'/report/'+dirpath+'/images/'+content[0]+'" width="'+content[1]+'" />\n</div>\n');
	}
})
// IMG node
// Hatena::ImgNode
Hatena_ImgNode = function(){};
Hatena_ImgNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\\img{((?:[^\*]).*)}$/;
	},
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		var content = String(RegExp.$1).split("/")
		// fig_nums.push(content[1])
		// c.htmllines("<h4 class='subsection'>"+section_num+"."+subsection_num+"&nbsp;&nbsp;"+ RegExp.$1 + "</h4>" + '<div class="subsection_content">');
		// c.htmllines('<div class="img_div"><img alt="'+content[0]+'" src="images/'+content[0]+'" width="'+content[2]+'" />\n<p><label><a href="#fig' + content[1] + '" name="figure' + content[1] + '">Fig.' + fig_num + '</a>&nbsp;'+content[3]+'</label></p>\n</div>\n');
		var urls = "";
		if(aparse_flg){
			urls = def_url;
		}
		c.htmllines('<div class="img_div"><img alt="'+content[0]+'" src="'+urls+'/report/'+dirpath+'/images/'+content[0]+'" width="'+content[1]+'" />\n</div>\n');
	}
})
// Hatena::RefNode
Hatena_RefNode = function(){};
Hatena_RefNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\#((?:[^\*]).*)$/;
	},
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		var content = String(RegExp.$1)
		// c.htmllines("</div>" + t + "<h3 class='section' name='reference'>References</h3><div class='reference_content'>");
		c.references(content);
	}
})
// Fcapnode
// Hatena::FcapNode
Hatena_FcapNode = function(){};
Hatena_FcapNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\$\%((?:[^\*]).*)$/;
	},
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		var content = String(RegExp.$1)
		fig_num +=1;
		c.htmllines('<div class="centers figs"><a href="#fig' + fig_num + '" name="figure' + fig_num + '">Fig.' + fig_num + '</a>&nbsp;'+content+'</div>\n');
	}
})
// Tcapnode
// Hatena::TcapNode
Hatena_TcapNode = function(){};
Hatena_TcapNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\$\|((?:[^\*]).*)$/;
	},
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		var content = String(RegExp.$1)
		tb_num +=1;
		c.htmllines('<div class="centers tbs"><a href="#tb' + tb_num + '" name="table' + tb_num + '">Table.' + tb_num + '</a>&nbsp;'+content+'</div>\n');
	}
})

// Numenode
// Hatena::NumeNode
Hatena_NumeNode = function(){};
Hatena_NumeNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\&\&((?:[^\*]).*)$/;
	},
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		var content = String(RegExp.$1).split("/")
		nume_num +=1;
		var urls = "";
		if(aparse_flg){
			urls = def_url;
		}
		c.htmllines('<div class="img_div"><table><tr><td><img alt="'+content[0]+'" src="'+urls+'/report/'+dirpath+'/images/'+content[0]+'" width="'+content[1]+'" /></td><td><a href="#nume' + nume_num + '" name="numeric' + nume_num + '">('+nume_num+')</a></td></tr></table>\n</div>\n');
	}
})
// Mathnode
// Hatena::MathNode
Hatena_MathNode = function(){};
Hatena_MathNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\$((?:[^\*]).*)\$$/;
	},
	parse : function(){
		var c = this.self.context;
		var l = c.shiftline();
		if(l == null) return;
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);
		var content = String(RegExp.$1).split("/")
		nume_num +=1;
		var urls = "";
		if(aparse_flg){
			urls = def_url;
		}
		c.htmllines('<div class="img_div"><table><tr><td>$'+content[0]+'$</td><td><a href="#nume' + nume_num + '" name="numeric' + nume_num + '">('+nume_num+')</a></td></tr></table>\n</div>\n');
	}
})


// Hatena::ListNode
Hatena_ListNode = function(){};
Hatena_ListNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^([\-\+]+)([^>\-\+].*)$/;
	},

	parse : function(){
		var c = this.self.context;
		var l = c.nextline();
		if(!l.match(this.self.pattern)) return;
		this.self.llevel = RegExp.$1.length;
		var t = String.times("\t", this.self.ilevel + this.self.llevel - 1);
		this.self.type = RegExp.$1.substr(0, 1) == '-' ? 'ul' : 'ol';

		c.htmllines(t + "<" + this.self.type + ">");
		while (l = c.nextline()) {
			if(!l.match(this.self.pattern)) break;
			if (RegExp.$1.length > this.self.llevel) {
				//c.htmllines(t + "\t<li>"); bug??
				var node = new Hatena_ListNode();
				node._new({
					context : this.self.context,
					ilevel : this.self.ilevel
				});
				node.parse();
				//c.htmllines(t + "\t</li>"); bug??
			} else if(RegExp.$1.length < this.self.llevel) {
				break;
			} else {
				l = c.shiftline();
				c.htmllines(t + "\t<li>" + RegExp.$2 + "</li>");
			}
		}
		c.htmllines(t + "</" + this.self.type + ">");
	}
})


// Hatena::PNode
Hatena_PNode = function(){};
Hatena_PNode.prototype = Object.extend(new Hatena_Node(), {
	parse :function(){
		var c = this.self.context;
		var t = String.times("\t", this.self.ilevel);
		var l = c.shiftline();
		var text = new Hatena_Text();
		text._new({context : c});
		text.parse(l);
		l = text.html();
		c.htmllines(t + "<p>" + l + "</p>");
	}
});

// Hatena::BlockNode
Hatena_BlockNode = function(){};
Hatena_BlockNode.prototype = Object.extend(new Hatena_Node(), {
	init :function(){
		this.self.pattern = /^>\?$/;
		this.self.endpattern = /(.*)\?<$/;
		this.self.startstring = "<div class='block'><pre>";
		this.self.endstring = "</pre></div>";
		// this.self.startstring = "<blockquote>";
		// this.self.endstring = "</blockquote>";
	},

	parse : function(){
		c = this.self.context;
		if(!c.nextline().match(this.self.pattern)) return;
		c.shiftline();
		var t = String.times("\t", this.self.ilevel);
		c.htmllines(t + this.self.startstring);
		var x = '';
		while (c.hasnext()) {
			var l = c.nextline();
			if (l.match(this.self.endpattern)) {
				var x = RegExp.$1;
				c.shiftline();
				break;
			}
			c.htmllines(this.escape_pre(c.shiftline()));
		}
		c.htmllines(x + this.self.endstring);
	},

	escape_pre : function(text){ return text; }
})


// Hatena::PreNode
Hatena_PreNode = function(){};
Hatena_PreNode.prototype = Object.extend(new Hatena_Node(), {
	init :function(){
		this.self.pattern = /^>\|$/;
		this.self.endpattern = /(.*)\|<$/;
		this.self.startstring = "<pre>";
		this.self.endstring = "</pre>";
	},

	parse : function(){
		c = this.self.context;
		if(!c.nextline().match(this.self.pattern)) return;
		c.shiftline();
		var t = String.times("\t", this.self.ilevel);
		c.htmllines(t + this.self.startstring);
		var x = '';
		while (c.hasnext()) {
			var l = c.nextline();
			if (l.match(this.self.endpattern)) {
				var x = RegExp.$1;
				c.shiftline();
				break;
			}
			c.htmllines(this.escape_pre(c.shiftline()));
		}
		c.htmllines(x + this.self.endstring);
	},

	escape_pre : function(text){ return text; }
})

// // Hatena::ImgNode
// Hatena_ImgNode = function(){};
// Hatena_ImgNode.prototype = Object.extend(new Hatena_Node(), {
// 	init : function(){
// 		this.self.pattern = /^\%\%((?:[^\*]).*)$/;
// 	},
// 	
// 	parse : function(){
// 		var c = this.self.context;
// 		var l = c.shiftline();
// 		if(l == null) return;
// 		if(!l.match(this.self.pattern)) return;
// 		var t = String.times("\t", this.self.ilevel);
// 		subsection_num+=1;
// 		subsubsection_num=0;
// 		c.htmllines("</div>" + t + "<h4 class='subsection'>"+section_num+"."+subsection_num+"&nbsp;&nbsp;"+ RegExp.$1 + "</h4>" + '<div class="subsection_content">');
// 	}
// })



// Hatena::SuperpreNode
Hatena_SuperpreNode = function(){};
Hatena_SuperpreNode.prototype = Object.extend(new Hatena_PreNode(), {
	init : function(){
		this.self.pattern = /^>\|\|$/;
		this.self.endpattern = /^\|\|<$/;
		this.self.startstring = "<pre>";
		this.self.endstring = "</pre>";
	},

	escape_pre : function(s){
		return String._escapeHTML(s);
	}
})


// Hatena::SuperpreNode
Hatena_TableNode = function(){};
Hatena_TableNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.pattern = /^\|([^\|]*\|(?:[^\|]*\|)+)$/;
	},

	parse : function(s){
		var c = this.self.context;
		var l = c.nextline();
		if(!l.match(this.self.pattern)) return;
		var t = String.times("\t", this.self.ilevel);

		c.htmllines(t + "<table class='tables'>");
		while (l = c.nextline()) {
			if(!l.match(this.self.pattern)) break;
			l = c.shiftline();
			c.htmllines(t + "\t<tr>");
			var td = l.split("|");
			td.pop(); td.shift();
			for (var i = 0; i < td.length; i++) {
				var item = td[i];
				if (item.match(/^\*(.*)/)) {
					c.htmllines(t + "\t\t<th>" + RegExp.$1 + "</th>");
				} else {
					c.htmllines(t + "\t\t<td>" + item + "</td>");
				}
			}
			c.htmllines(t + "\t</tr>");
		}
		c.htmllines(t + "</table>");
	}
})


// Hatena::Section
Hatena_SectionNode = function(){};
Hatena_SectionNode.prototype = Object.extend(new Hatena_Node(), {
	init : function(){
		this.self.childnode = ["nume","math","img", "tcap","fcap","ref","h6","h5", "h4", "h3", "blockquote", "dl", "list", "block", "pre", "superpre", "table", "tagline", "tag"];
		this.self.startstring = '<div class="section">';
		this.self.endstring = '';
		this.self.child_node_refs = Array();
	},

	parse : function(){
		var c = this.self.context;
		var t = String.times("\t", this.self.ilevel);
		this._set_child_node_refs();
		c.htmllines(t + this.self.startstring);
		while (c.hasnext()) {
			var l = c.nextline();
			var node = this._findnode(l);
			if(node == null) return;
			// TODO: ref == instanceof ???
			//if (ref(node) eq 'Hatena_H3Node') {
			//	if(this.self.started++) break;
			//}
			node.parse();
		}
		c.htmllines(t + this.self.endstring);
	},

	_set_child_node_refs : function(){
		var c = this.self.context;
		var nodeoption = {
			context : c,
			ilevel : this.self.ilevel + 1
		};
		var invalid = Array();
		if(c.self.invalidnode) invalid[c.self.invalidnode] = Array();
		for(var i = 0; i <  this.self.childnode.length; i++) {
			var node = this.self.childnode[i];
			if(invalid[node]) continue;
			var mod = 'Hatena_' + node.charAt(0).toUpperCase() + node.substr(1).toLowerCase() + 'Node';
			var n = eval("new "+ mod +"()");
			n._new(nodeoption);
			this.self.child_node_refs.push(n);
		}
	},

	_findnode : function(l){
		for(var i = 0; i < this.self.child_node_refs.length; i++) {
			var node = this.self.child_node_refs[i];
			var pat = node.self.pattern;
			if(pat == null) continue;
			// alert(pat)
			if (l.match(pat)) {
				return node;
			}
		}
		var nodeoption = {
			context : this.self.context,
			ilevel : this.self.ilevel + 1
		};
		if (l.length == 0) {
			var node = new Hatena_BrNode(nodeoption);
			node._new(nodeoption);
			return node;
		} else if (this.self.context.noparagraph()) {
			var node = new Hatena_CDataNode();
			node._new(nodeoption);
			return node;
		} else {
			var node = new Hatena_PNode;
			node._new(nodeoption);
			return node;
		}
	}
})


// Hatena::BrockquoteNode
Hatena_BlockquoteNode = function(){};
Hatena_BlockquoteNode.prototype = Object.extend(new Hatena_SectionNode(), {
	init : function(){
		this.self.pattern = /^>¥$/;
		this.self.endpattern = /^¥<$/;
		this.self.childnode = ["h4", "h5","h6","ref","fcap","tcap","nume","math","img",  "blockquote", "dl", "list", "block", "pre", "superpre", "table"];//, "tagline", "tag"];
		this.self.startstring = "<blockquote>";
		this.self.endstring = "</blockquote>";
	},

	parse : function(){
		var c = this.self.context;
		if(!c.nextline().match(this.self.pattern)) return;
		c.shiftline();
		var t = String.times("\t", this.self.ilevel);
		this._set_child_node_refs();
		c.htmllines(t + this.self.startstring);
		while (c.hasnext()) {
			var l = c.nextline();
			if (l.match(this.self.endpattern)) {
				c.shiftline();
				break;
			}
			var node = this._findnode(l);
			if(node == null) break;
			node.parse();
		}
		c.htmllines(t + this.self.endstring);
	}
})


// Hatena::TagNode
Hatena_TagNode = function(){};
Hatena_TagNode.prototype = Object.extend(new Hatena_SectionNode(), {
	init : function(){
		this.self.pattern = /^>(<.*)$/;
		this.self.endpattern = /^(.*>)<$/;
		this.self.childnode = ["h4", "h5","h6","ref","fcap","tcap", "nume","math", "blockquote", "dl", "list","block", "pre", "superpre", "table"];
		this.self.child_node_refs = Array();
	},

	parse : function(){
		var c = this.self.context;
		var t = String.times("\t", this.self.ilevel);
		if(!c.nextline().match(this.self.pattern)) return;
		c.shiftline();
		c.noparagraph(1);
		this._set_child_node_refs();
		var x =this._parse_text(RegExp.$1);
		c.htmllines(t + x);
		while (c.hasnext()) {
			var l = c.nextline();
			if (l.match(this.self.endpattern)) {
				c.shiftline();
				x = this._parse_text(RegExp.$1);
				c.htmllines(t + x);
				break;
			}
			var node = this._findnode(l);
			if(node == null) break;
			node.parse();
		}
		c.noparagraph(0);
	},

	_parse_text : function(l){
		var text = new Hatena_Text();
		text._new({context : this.self.context});
		text.parse(l);
		return text.html();
	}
})


// Hatena::TaglineNode
Hatena_TaglineNode = function(){};
Hatena_TaglineNode.prototype = Object.extend(new Hatena_SectionNode(), {
	init : function(){
		this.self.pattern = /^>(<.*>)<$/;
		this.self.child_node_refs = Array();
	},

	parse : function(){
		var c = this.self.context;
		var t = String.times("\t", this.self.ilevel);
		if(!c.nextline().match(this.self.pattern)) return;
		c.shiftline();
		c.htmllines(t + RegExp.$1);
	}
})


// Hatena::Text
Hatena_Text = function(){}
Hatena_Text.prototype = {
	_new : function(args){
		this.self = {
			context : args["context"],
			html : ''
		};
	},
	parse : function(text){
		this.self.html = '';
		if(text == null) return;
		this.self.html = text;
	},

	html : function(){return this.self.html;}
}


/*var h = new Hatena();
h.parse("hoge((a))aaa))aaaa\n><a>hoge</a><aaa");
WScript.echo(h.html());
*/
