# DinnerSelector

This is a final project of Web Retrieval and Mining, Spring 2019

## Usage

### crawler/get_guides.js
1. Load a webpage of a place in Chrome.  
E.g. https://www.google.com/maps/place/%E5%A5%B3%E4%B9%9D%E9%A4%90%E5%BB%B3/@25.0195299,121.5372919,17z/data=!3m1!4b1!4m13!1m7!3m6!1s0x0:0x0!2s2G9Q%2BRQ!3b1!8m2!3d25.0195625!4d121.5394375!3m4!1s0x3442aa27ae7387a7:0x99735a76e6b5dc2f!8m2!3d25.0195299!4d121.5394752
2. Paste the script into console and wait until the reviews are loaded. A file will be saved. **Keep the tab active!**
* Only reviewers with number of reviews >= \<thresh> are fetched. It is specified in the last line: `start(<thresh>);`

data structure of `local_guides length=<list.length> place=<name> thresh=<num>.json`:
```
[
    {
        "ID": "108994155436866578572",
        "nReview": 300
    },
    ...
]
```

### crawler/get_reviews_from_guide.js
1. Load a webpage of a reviewer in Chrome.  
E.g. https://www.google.com/maps/contrib/108994155436866578572/reviews
2. Paste the script into console and wait until the reviews are loaded. A file will be saved. **Keep the tab active!**

data structure of `reviews_guide length=<list.length> guideID=<ID>.json`:
```
[
    {
        "place": "高和食堂",
        "address": "106台北市大安區和平東路二段118巷60號",
        "stars": 2,
        "content": "價格小貴，份量偏少，口味一般。"
    },
    ...
]
```

### crawler/auto_crawl.js
This script automates `crawler/get_reviews_from_guide.js`.
1. Install `Node.js` and `Puppeteer`
2. `node auto_crawl.js`
3. Try to keep all the tabs active
4. Change the index of the for loop in line 10 and repeat

### crawler/get_reviews_from_place.js
1. Load a webpage of a place in Chrome.  
E.g. https://www.google.com/maps/place/%E5%A5%B3%E4%B9%9D%E9%A4%90%E5%BB%B3/@25.0195299,121.5372919,17z/data=!3m1!4b1!4m13!1m7!3m6!1s0x0:0x0!2s2G9Q%2BRQ!3b1!8m2!3d25.0195625!4d121.5394375!3m4!1s0x3442aa27ae7387a7:0x99735a76e6b5dc2f!8m2!3d25.0195299!4d121.5394752
2. Paste the script into console and wait until the reviews are loaded. A file will be saved. **Keep the tab active!**

data structure of `reviews_place length=<list.length> place=<name>.json`:
```
[
    {
        "reviewer": {
            "ID": "108994155436866578572",
            "nReview": 300
        },
        "stars": 5,
        "content": "好吃便宜尤其是菜類的不錯\n肉類的好像炸類的比較優 滷肉很硬"
    },
    ...
]
```

### preprocessing/merge_guides.py
1. Collect guides from a number of places with `crawler/get_guides.js` and save them in `data/local_guides`.
2. Run.
3. `guides.txt` will be generated, containing guides who reviewed over `5` places in Step 1.

### preprocessing/select_places.py
1. Collect reviews of the guides in `guides.txt` with `crawler/get_reviews_from_guide.js` and save them in `data/reviews_guide`.
2. Run.
3. `places.json` will be generated, containing places reviewed by over `10` guides in `guides.txt`.

### preprocessing/LSI.py
1. Run. It may take some time if `len(places)` is large. 12000 places takes about 1 minute for X280, mainly spent on SVD.
2. `guides_normalized.npy` will be generated. The columns include normalized number of stars reviewed from guides.
3. Projection matrix `proj.npy` will be generated. Refer to `example_get_latent()` for usage.
4. `guides_latent.npy` will be generated. The columns are guide vectors. Refer to `example_visualize()` for usage.

## Git Branch
* https://hackmd.io/i0CooTWuSCi_Wc0d9wNB4A

## For VS Code users
* You may want to add this in `/.vscode/launch.json`
```
"cwd": "${fileDirname}"
```