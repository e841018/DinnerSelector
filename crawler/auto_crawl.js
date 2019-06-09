const puppeteer = require('puppeteer');
const fs = require('fs');
var get_reviews_from_guides = fs.readFileSync('./get_reviews_from_guide.js', 'utf-8');
var guide_list = fs.readFileSync('./guides.txt', 'utf-8').split('\n');
guide_list.pop();
nGuide = guide_list.length;

(async () => {
	const browser = await puppeteer.launch({headless:false});
	for(i=1; i<2; i++){
		const page = await browser.newPage();
		await page.exposeFunction('closeTab', async () => {await page.close();});
		await page.goto('https://www.google.com/maps/contrib/' + guide_list[i] + '/reviews');
		await page.waitForSelector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-listbox.section-scrollbox.scrollable-y.scrollable-show > div.section-listbox');
		await page.evaluate(get_reviews_from_guides);
	}
	// await browser.close();
})();