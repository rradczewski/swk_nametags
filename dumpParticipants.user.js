(function() {
var members = [];
$.ajaxSetup({async: false});
$(".member a:first-child").each(function(i, link) { 
	$.get(link.href, function(userHtml) { 
		var dom = $(userHtml);
		var user = {};
		dom.find("p").each(function(i, el) {
			var parts = el.outerText.split(/:\s/);
			if(parts.length < 2) return;
			user[parts[0]] = parts[1];
		});
		members.push(user);
	});
});
console.log("Downloading Infos for "+members.length+" participants");
var a = document.createElement("a");
a.download = "participants.json";
a.href = "data:application/json;charset=UTF-8;base64,"+btoa(JSON.stringify(members));
a.click();
})();
