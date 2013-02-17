var labelType, useGradients, nativeTextSupport, animate;

function dellevel_change(){
	network_delete_level = $("#del_level option:selected").val()
}
function laylevel_change(){
	network_layer_level = $("#layer_level option:selected").val()
}
function del_node(node){
	if(network_delete_level!=0){
		$.ajax({
			 type: "POST",
			 url: "/isreport/api/del_network",
			 data: "id="+node.name.split("_")[1]+"&view_level="+network_delete_level,
			 success: function(){
			},
			 complete: function(){	
		　　 },
		 });
	}else{
		alert("permission denied");
	}
}
(function() {
  var ua = navigator.userAgent,
      iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
      typeOfCanvas = typeof HTMLCanvasElement,
      nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
      textSupport = nativeCanvasSupport 
        && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
    if (!this.elem) 
      this.elem = document.getElementById('log');
    this.elem.innerHTML = text;
    this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};

function infovis_init(){
	infovis_init_local(network_target_id);
}

function infovis_init_local(network_target_id_local){
  // init data
	// show_save();
	var entry = $("img#ajax_load_network");
	entry.show();
	
  var json = []
  	$.ajax({
		 type: "GET",
		 url: "/isreport/api/network",
		 data: "id="+network_target_id_local+"&view_level="+network_view_level+"&layer="+network_layer_level,
		 success: function(json){
			// end
		  // init ForceDirected
		  var fd = new $jit.ForceDirected({
		    //id of the visualization container
		    injectInto: 'infovis',
		    //Enable zooming and panning
		    //with scrolling and DnD
		    Navigation: {
		      enable: true,
		      type: 'Native',
		      //Enable panning events only if we're dragging the empty
		      //canvas (and not a node).
		      panning: 'avoid nodes',
		      zooming: 10 //zoom speed. higher is more sensible
		    },
		    // Change node and edge styles such as
		    // color and width.
		    // These properties are also set per node
		    // with dollar prefixed data-properties in the
		    // JSON structure.
				// 		    Label: {
				// 		      	overridable: true,
				// type: 'Native',
				// 			    size: 11,  
				// 			    color: '#333'
				// 		    },
		    Node: {
		      overridable: true,
		      dim: 7
		    },
		    Edge: {
		      overridable: true,
		      color: '#23A4FF',
		      lineWidth: 0.4
		    },
		    // Add node events
		    Events: {
		      enable: true,
		      type: 'Native',
		      //Change cursor style when hovering a node
		      onMouseEnter: function() {
		        fd.canvas.getElement().style.cursor = 'move';
		      },
		      onMouseLeave: function() {
		        fd.canvas.getElement().style.cursor = '';
		      },
		      //Update node positions when dragged
		      onDragMove: function(node, eventInfo, e) {
		        var pos = eventInfo.getPos();
		        node.pos.setc(pos.x, pos.y);
		        fd.plot();
		      },
		      //Implement the same handler for touchscreens
		      onTouchMove: function(node, eventInfo, e) {
		        $jit.util.event.stop(e); //stop default touchmove event
		        this.onDragMove(node, eventInfo, e);
		      }
		    },
		    //Number of iterations for the FD algorithm
		    iterations: 200,
		    //Edge length
		    levelDistance: 200,
		    // This method is only triggered
		    // on label creation and only for DOM labels (not native canvas ones).
		    onCreateLabel: function(domElement, node){
		      // Create a 'name' and 'close' buttons and add them
		      // to the main node label
		      var nameContainer = document.createElement('span'),
		          closeButton = document.createElement('span'),
		          style = nameContainer.style;
		      nameContainer.className = 'name';
		      // nameContainer.innerHTML = node.name
		      nameContainer.innerHTML = node.name.split("_")[0];
		      closeButton.className = 'close';
		      closeButton.innerHTML = 'x';
				// node.get_edge = true;
		      domElement.appendChild(nameContainer);
		      domElement.appendChild(closeButton);
		      // style.fontSize = "0.8em";
		      // style.color = "#333";
		      //Fade the node and its connections when
		      //clicking the close button
		      closeButton.onclick = function() {
				if(network_delete_level!=0){
					if(window.confirm('really delete?\n'+node.name)){
			        	node.setData('alpha', 0, 'end');
			        	node.eachAdjacency(function(adj) {
			          		adj.setData('alpha', 0, 'end');
			        	});
			        	fd.fx.animate({
			          		modes: ['node-property:alpha',
			                  'edge-property:alpha'],
			          		duration: 500
			        	});
						del_node(node);
					}
					else{
					}
				}else{
		        	node.setData('alpha', 0, 'end');
		        	node.eachAdjacency(function(adj) {
		          		adj.setData('alpha', 0, 'end');
		        	});
		        	fd.fx.animate({
		          		modes: ['node-property:alpha',
		                  'edge-property:alpha'],
		          		duration: 500
		        	});
				}
		      };
		      //Toggle a node selection when clicking
		      //its name. This is done by animating some
		      //node styles like its dimension and the color
		      //and lineWidth of its adjacencies.
		      nameContainer.onclick = function() {
		        //set final styles
		        fd.graph.eachNode(function(n) {
		          if(n.id != node.id) delete n.selected;
		          n.setData('dim', 7, 'end');
		          n.eachAdjacency(function(adj) {
		            adj.setDataset('end', {
		              lineWidth: 0.4,
		              color: '#23a4ff'
		            });
		          });
		        });
		        if(!node.selected) {
		          node.selected = true;
		          node.setData('dim', 17, 'end');
		          node.eachAdjacency(function(adj) {
		            adj.setDataset('end', {
		              lineWidth: 3,
		              color: '#36acfb'
		            });
		          });
		        } else {
		          delete node.selected;
		        }
		        //trigger animation to final styles
		        fd.fx.animate({
		          modes: ['node-property:dim',
		                  'edge-property:lineWidth:color'],
		          duration: 500
		        });
		        // Build the right column relations list.
		        // This is done by traversing the clicked node connections.
		        var html = "<h4>" + node.name + "</h4><b> connections:</b><ul><li>",
		            list = [];
		        node.eachAdjacency(function(adj){
		          if(adj.getData('alpha')) list.push(adj.nodeTo.name);
		        });
		        //append connections information
		        $jit.id('inner-details').innerHTML = html + list.join("</li><li>") + "</li></ul>";
				// alert(node.name.split("_")[1]);
				// infovis_init_local(node.name.split("_")[1]);
				var json = []
				entry.show();
			  	$.ajax({
					 type: "GET",
					 url: "/isreport/api/network",
					 data: "id="+node.name.split("_")[1]+"&view_level="+network_view_level+"&layer=0",
					 success: function(json){
							// load JSON data.
					  		// fd.loadJSON(json);
							fd.op.sum(json, {
					          type: 'fade:seq',
					          duration: 1000,
					          hideLabels: false,
					          transition: $jit.Trans.Quart.easeOut
					        });
					  		// compute positions incrementally and animate.
					},
					 complete: function(){	
						entry.hide();
				　　 },
				 });
				
		      };
		    },
		    // Change node styles when DOM labels are placed
		    // or moved.
		    onPlaceLabel: function(domElement, node){
		      var style = domElement.style;
		      var left = parseInt(style.left);
		      var top = parseInt(style.top);
		      var w = domElement.offsetWidth;
		      style.left = (left - w / 2) + 'px';
		      style.top = (top + 10) + 'px';
		      style.display = '';
		    }
		  });
		  // load JSON data.
		  fd.loadJSON(json);
		  // compute positions incrementally and animate.
		  fd.computeIncremental({
		    iter: 40,
		    property: 'end',
		    onStep: function(perc){
		      Log.write(perc + '% loaded...');
		    },
		    onComplete: function(){
		      Log.write('');
		      fd.animate({
		        modes: ['linear'],
		        transition: $jit.Trans.Elastic.easeOut,
		        duration: 2500
		      });
		    }
		  });
		  // end
		 },
		 complete: function(){	
			entry.hide();
	　　 },
	 });
}
