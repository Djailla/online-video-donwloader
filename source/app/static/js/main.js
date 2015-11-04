var current_folder = null;

var displayTheme = null;

var mainWindow = null;

/*var results = {
	"folder": {
		"name": "folder",
		"isDir": true,
		"subFolder": {
			"newFolder":{
				"name": "newFolder",
				"isDir": true,
				"subFolder": []
			},
		}
	},
	"file":{
		"name": "file",
		"isDir": false,
		"url": "http://monurl"
	}

};*/
var results = null;

function setPopup(popup){
	mainWindow.innerHTML = "";
	mainWindow.appendChild(popup);
}

function init(){
	displayTheme = new WualaDisplay();
	mainWindow = document.getElementById("window_popup_id");
	browse('/');

	//$.ajax({
	//url: "browse",
	//method: 'post',
	//data: {path: '/Users/bvallet/Desktop'},
	//success: function(result){
	//	console.log("Got some things...");
	//	current_folder = "/";
	//	results = result;
	//	display("/");
	//},
	//dataType: 'json',
	//});
}

function browse(path){
	$.ajax({
		url: "browse",
		method: 'post',
		data: {path: path},
		success: function(result){
			current_folder = path;
			results = result;
			display(path);
		},
		dataType: 'json',
	});
	console.log("Browsing " + path);
}

function display(path){
	if ("/" != path.charAt(path.length - 1)){
		path = path + "/";
	}
	displayTheme.GetBrowsingPathElement(path, display);
	var elementListObject = displayTheme.GetFilesListElement(path);

	if ("/" != path){
		displayTheme.AddElement(elementListObject, null, "..",
			function(event){
				var path = this;
				if ("/" == path.charAt(path.length - 1)){
					path = path.substr(0, path.length - 1);
				}
				var split = path.split("/");
				path = split.slice(0, split.length - 1).join("/");
				if (path === "")
				{
					path = "/";
				}
				browse(path);
			}.bind(path)
		);
	}
	for(var element_key in results){
		var element = results[element_key];
		element_path = path + element.name;
		var downloadCB = null;
		var browseCB = null;
		var deleteCB = function(path, event){
			event.stopPropagation();
			setPopup(deletePopup(path));
		}.bind(element, element_path);

		if (element.isDir){
			browseCB = function(path, event){
				// TODO USE BROWSE COMMAND
				console.log("Try to browse "+path);
				browse(path);
			}.bind(element, element_path);
		}else{
			downloadCB = function(path, event){
				event.stopPropagation();
				console.log(this.url);
				window.open(this.url);
			}.bind(element, element_path);
		}
		displayTheme.AddElement(elementListObject, element, element.name, browseCB, downloadCB, deleteCB);
	}
	//browse_div.appendChild(ul);
	var mainDisplay = document.getElementById("browsing");
	mainDisplay.innerHTML = "";
	mainDisplay.appendChild(displayTheme.GetListDisplayComponent(elementListObject));
}

function downloadPopup(path, download_link){
	var window_div = document.createElement("div");
	window_div.className = "window shadow";
	window_div.id = "download_link_popup";
	var caption_div = Caption("Download " + path);
	//End of Caption defintion
	window_div.appendChild(caption_div);
	var content_div = document.createElement("div");
	content_div.className = "content";
	content_div.id = "download_link_content";
	var display_content_div = document.createElement("div");
	var url_div = document.createElement("div");
	url_div.className = "input-control text";
	var download_link_input = document.createElement("input");
	download_link_input.type = "text";
	var dlink = location.protocol + "//" + location.host + "/downloads/" + download_link;
	download_link_input.value = dlink;
	url_div.appendChild(download_link_input);
	url_div.appendChild(document.createTextNode('\u00A0'));
	var download_link_download_button = document.createElement("span");
	//download_link_download_button.type = "button";
	download_link_download_button.className = "icon icon-download";
	download_link_download_button.onclick = function(){
		window.open(dlink);
	};
	url_div.appendChild(download_link_download_button);
	display_content_div.appendChild(url_div);
	content_div.appendChild(display_content_div);
	window_div.appendChild(content_div);
	return window_div;
}

function Caption(text){
	var caption_div = document.createElement("div");
	caption_div.className = "caption";
	//Caption definition
	var caption_span = document.createElement("span");
	caption_span.className = "icon icon-windows";
	caption_div.appendChild(caption_span);
	var caption_title = document.createElement("div");
	caption_title.className = "title";
	caption_title.innerHTML = text;
	caption_div.appendChild(caption_title);
	var caption_close_button = document.createElement("a");
	caption_close_button.className = "button small";
	var i =document.createElement("i");
	i.className = "icon-remove";
	caption_close_button.appendChild(i);
	caption_div.appendChild(caption_close_button);
	caption_close_button.onclick = function(){
		caption_div.parentNode.parentNode.removeChild(caption_div.parentNode);
	};
	return caption_div;
}
