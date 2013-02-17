function check_file(form){
	if($("#uploading").val()){
		return true;
	}else{
		alert("ファイルが選択されていません");
		return false;
	}
}

var dnd = {
	//-----------------------------------------
	// 設定値
	//-----------------------------------------
	config : {
		outputId : 'outputImages'
	},
	//-----------------------------------------
	// 初期処理
	//-----------------------------------------
	initialize : function() {
		// イベント登録
		dnd.addEvent( window, 'dragenter', dnd.dragenter );
		dnd.addEvent( window, 'dragleave', dnd.dragleave );
		dnd.addEvent( window, 'dragover', dnd.dragover );
		dnd.addEvent( window, 'drop', dnd.drop );
	},
	//-----------------------------------------
	// dragenter
	//-----------------------------------------
	dragenter : function(e) {
		
	},
	//-----------------------------------------
	// dragleave
	//-----------------------------------------
	dragleave : function(e) {
		
	},
	//-----------------------------------------
	// dragover
	//-----------------------------------------
	dragover : function(e) {
		// イベント伝播キャンセル
		e.preventDefault();
	},
	//-----------------------------------------
	// drop
	//-----------------------------------------
	drop : function(e) {
		// ファイルハンドラを取得
		var dt = e.dataTransfer;
		var files = dt.files;
		// イベント伝播キャンセル
		e.preventDefault();
		// データそのものの場合
		if (files.length == 0) {
			dnd.handleData(dt);
			return;
		}
		// ファイルの場合
		var len = files.length;
		for (var i = 0; i < len; i++) {
			var file = files[i];
			dnd.handleFile(file);
		}
	},
	//-----------------------------------------
	// handleData
	//-----------------------------------------
	handleData : function(dt) {
		// TODO いったん未対応
		return false;
	},
	//-----------------------------------------
	// handleFile
	//-----------------------------------------
	handleFile : function(file) {
		var imageType = /image.*/;
		var output = document.getElementById(dnd.config.outputId);
		// Fileインターフェイスでファイルの種別を判定
		if ( !file.type.match(imageType) ) {
			return false;
		}
		// ファイルを読み込みimg要素にセット
		var img = document.createElement('img');
		var reader = new FileReader();
		reader.onloadend = function() {
			img.src = reader.result;
		}
		reader.readAsDataURL(file);
		// TODO その他情報（いったんtitle属性に書き出し）
		img.setAttribute('title', file.name + '（size:' + file.size + '／type:' + file.type + '）');
		// 出力エリアにimg要素を追加
		output.insertBefore(img, output.firstChild);
		$("div#dad").hide();
		$("#outputImages").show();
		// $("#uploading").val(file)
		return true;
	},
	//-----------------------------------------
	// イベントに関数を付加する
	//-----------------------------------------
	addEvent : function( target, event, func ) {
		try {
			target.addEventListener(event, func, false);
		} catch (e) {
			target.attachEvent('on' + event, (function(el){return function(){func.call(el);};})(target));
		}
	}
}
// 実行
dnd.addEvent( window, 'load', dnd.initialize );