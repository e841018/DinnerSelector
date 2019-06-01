// save as file
var download = function(data, filename){
	var file = new Blob([data], {type: 'application/json'});
	var temp = document.createElement('a');
	temp.download = filename;
	temp.href = URL.createObjectURL(file);
	temp.click();
	URL.revokeObjectURL(temp.href);
	temp.remove();
}

function resolveAfter(t){
	return new Promise(func => {setTimeout(func, t);});
}

// collect data
var collect_data = function(frame){
	var data = [];
	var guideList = frame.childNodes[frame.childElementCount-2].querySelectorAll('div.section-review > div > div.section-review-content > div.section-review-line > div');
	guideList.forEach((item) => {
		var guide = {};
		try{
			guide.ID = item.querySelector('div > a').href.match(/contrib\/(\d*)/)[1];
			guide.nReview = Number(item.querySelector('div > a > div.section-review-subtitle > span:nth-child(2)').textContent.match(/(\d+)/)[1]);
			if(guide.nReview>=arguments.callee.thresh)
				data.push(guide);
		}
		catch(e){;}
	});
	return data;
}

// download collected data if finished loading
var save = function(frame){
	if(frame.childNodes[frame.childElementCount-1].className===''){
		var data = collect_data(frame);
		var placeName = decodeURI(window.location.href.match(/place\/(.+)\/@/)[1])
		download(JSON.stringify(data), 'length='+data.length+' place='+placeName+' thresh='+collect_data.thresh);
	}
}

// scroll to buttom and call save() 1 second later
var scrollToButtom = function(){
	var frame = this.parentElement;
	frame.scroll(0, frame.scrollHeight);
	clearTimeout(this.timerID);
	this.timerID = setTimeout(save, 1000, frame);
};

// add listener and start by an initial scrollToButtom()
var start = async function(thresh){
	collect_data.thresh = thresh; // store thresh attribute in function object
	document.querySelector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-listbox.section-listbox-space-between.section-listbox-vertically-center-content.section-listbox-flex-vertical.section-listbox-flex-horizontal > div:nth-child(2) > div > button').click();
	var frame_selector = '#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-listbox.section-scrollbox.scrollable-y.scrollable-show';
	while(document.querySelector(frame_selector)===null)
		await resolveAfter(10);
	var frame = document.querySelector(frame_selector);
	var reviews = frame.childNodes[frame.childElementCount-2];
	reviews.addEventListener('DOMNodeInserted', scrollToButtom);
	scrollToButtom.call(reviews);
};

start(100);