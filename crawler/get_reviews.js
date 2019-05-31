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

// collect data
var collect_data = function(frame){
	var data = [];
	var reviewList = frame.querySelectorAll('div.section-listbox > div.section-review > div > div.section-review-content > div.section-review-line > div');
	reviewList.forEach((item) => {
		var review = {};
		review.title = item.querySelector('div.section-review-titles > div > div.section-review-title > span').textContent;
		review.address = item.querySelector('div.section-review-titles > div > div.section-review-subtitle > span').textContent;
		review.stars = Number(item.querySelector('div:nth-child(3) > div.section-review-metadata > span.section-review-stars').getAttribute('aria-label')[1]);
		review.content = item.querySelector('div:nth-child(3) > div.section-review-review-content > span.section-review-text').textContent;
		data.push(review);
	});
	return data;
}

// download collected data if finished loading
var save = function(frame){
	if(frame.children[2].className===''){
		var data = collect_data(frame);
		var guideID = window.location.href.match(/contrib\/(\d*)/)[1];
		download(JSON.stringify(data), 'length='+String(data.length)+' guideID='+guideID);
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
var start = function(){
	var reviews = document.querySelector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-listbox.section-scrollbox.scrollable-y.scrollable-show > div.section-listbox');
	reviews.addEventListener('DOMNodeInserted', scrollToButtom);
	scrollToButtom.call(reviews);
}

start();