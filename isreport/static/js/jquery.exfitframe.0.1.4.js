/*
 * 	exFitFrame 0.1.4 - jQuery plugin
 *	written by Cyokodog	
 *
 *	Copyright (c) 2011 Cyokodog (http://d.hatena.ne.jp/cyokodog/)
 *	Dual licensed under the MIT (MIT-LICENSE.txt)
 *	and GPL (GPL-LICENSE.txt) licenses.
 *
 *	Built for jQuery library
 *	http://jquery.com
 *
 */
(function($){

	var isDisplayScrollBar = function(target, key){
		var val = target.css('overflow-' + key)
		if (val == 'scroll') return true;
		if (val == 'hidden') return false;
//		if (val == 'auto' || target.attr('tagName') == 'HTML') {
		if (val == 'auto' || target[0].tagName == 'HTML') {
			var method = (key == 'y' ? 'Height' : 'Width');
//			return target.attr('client' + method) < target.attr('scroll' + method);
			return target[0]['client' + method] < target[0]['scroll' + method];
		}
		return false
	}

	var API = function(api){
		var api = $(api),api0 = api[0];
		for(var name in api0)
			(function(name){
				if($.isFunction( api0[name] ))
					api[ name ] = (/^get[^a-z]/.test(name)) ?
						function(){
							return api0[name].apply(api0,arguments);
						} : 
						function(){
							var arg = arguments;
							api.each(function(idx){
								var apix = api[idx];
								apix[name].apply(apix,arg);
							})
							return api;
						}
			})(name);
		return api;
	}

	$.ex = $.ex || {};

	$.ex.fitFrame = function(idx , targets , option){
		var o = this,
		c = o.config = $.extend({} , $.ex.fitFrame.defaults , option);
		c.targets = targets;
		c.target = c.targets.eq(idx);
		c.index = idx;
		c.size = {};
//		c.target.css( c.css || {} ).attr('frameborder','0');
		c.target.css( c.css || {} )[0].frameborder = '0';
		if(o.getContents()){
			o.fit();
		}
		!c.loadFit || o.loadFit();
		!c.watchFit || o.watchFit();
	}
	$.extend($.ex.fitFrame.prototype, {
		_initBox : function( cn , name ){
			var o = this, c = o.config;
			var html = cn.find('html');
			html.css('overflow-' + (name == 'height' ? 'y' : 'x'),'hidden');
			html.css('border','none').find('body').css('margin',0);
			return o;
		},
		_fit : function( name , watch ){
			var o = this, c = o.config;
			var cn = o.getContents();
			if( !cn ) return o;
			var cr = o.getContainer(name);
			if( !cr ) return o;
			var now = c.target[name]();
			var size = cr[name]();
			if( name == 'height' && isDisplayScrollBar(cn.find('html'),'x')) size += 16;
			if( now == size){
				watch || o._initBox( cn , name );
				return o;
			}
			o._initBox( cn , name );
			c.target[name]( size );
			c.size[name] = cr[name]();
			return o;
		},
		fit : function(){
			var o = this, c = o.config;
			!c.widthFit || o.widthFit();
			!c.heightFit || o.heightFit();
			return o;
		},
		widthFit : function(){
			return this._fit('width');
		},
		heightFit : function(){
			return this._fit('height');
		},
		loadFit : function(){
			var o = this, c = o.config;
			c.target
				.unbind('load.ex-fit-frame')
				.bind('load.ex-fit-frame',function(){
					o.fit();					
					!c.load || c.load.apply(this,[o]);
				});
			return o;
		},
		watchFit : function( time ){
			var o = this, c = o.config;
			time = time || c.watchFit;
			if( c.watch ) clearTimeout( c.watch );
			c.watch = setTimeout(function(){
				try{
					o.fit();
				}
				finally{
					o.watchFit( time );
				}
			},time);
			return o;
		},
		getContents : function(){
			var o = this, c = o.config;
			var cn = c.target.contents();
//			if(!cn.find('body').attr('tagName')) return undefined;
			if(!cn.find('body').size() || !cn.find('body')[0].tagName) return undefined;
			return cn;
		},
		getContainer : function( name ){
			var o = this, c = o.config;
			var cn = o.getContents();
			return ( !cn || name == 'width' ) ? cn : cn.find('body') ;
		},
		getTargets : function(){
			return this.config.targets;
		},
		getTarget : function(){
			return this.config.target;
		}
	});
	$.ex.fitFrame.defaults = {
		widthFit : true,
		heightFit : true,
		loadFit : true,
		watchFit : 300,
		css : null,
		load : null
	}
	$.fn.exFitFrame = function(option){
		var targets = this,api = [];
		targets.each(function(idx) {
			var target = targets.eq(idx);
			var obj = target.data('ex-fitFrame') || new $.ex.fitFrame( idx , targets , option);
			api.push(obj);
			target.data('ex-fitFrame',obj);
		});
		return option && option.api ? API(api) : targets;
	}
})(jQuery);
