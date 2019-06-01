# DinnerSelector

## Usage

### crawler/get_reviews.js

1. Load a webpage of a local guide in Chrome.

E.g. https://www.google.com/maps/contrib/108994155436866578572/reviews

2. Paste the script into console.

3. Wait until the reviews are loaded and a file (length=<list.length> guideID=<ID>) will be saved. **Keep the browser window active.**

### crawler/get_guideIDs.js

1. Load a webpage of a local guide in Chrome.

E.g. https://www.google.com/maps/place/%E5%A5%B3%E4%B9%9D%E9%A4%90%E5%BB%B3/@25.0195299,121.5372919,17z/data=!3m1!4b1!4m13!1m7!3m6!1s0x0:0x0!2s2G9Q%2BRQ!3b1!8m2!3d25.0195625!4d121.5394375!3m4!1s0x3442aa27ae7387a7:0x99735a76e6b5dc2f!8m2!3d25.0195299!4d121.5394752?hl=zh-TW

2. Paste the script into console.

3. Wait until the reviews are loaded and a file (length=<list.length> place=<name> thresh=<num>) will be saved. **Keep the browser window active.**

* Only reviewers with number of reviews > <thresh> are fetched. It is specified in the last line: ```start(<thresh>);```
