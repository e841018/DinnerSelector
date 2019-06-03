# DinnerSelector

## Usage

### crawler/get_reviews_from_guide.js
1. Load a webpage of a reviewer in Chrome.  
E.g. https://www.google.com/maps/contrib/108994155436866578572/reviews
2. Paste the script into console and wait until the reviews are loaded. A file will be saved. **Keep the tab active!**

data structure of `reviews_guide length=<list.length> guideID=<ID>.json`:
```
[
    {
        "place": "創義面",
        "address": "10462, Taipei City, Zhongshan District, Lane 46, Dazhi Street, 34號",
        "stars": 3,
        "content": "一般般吧 價格跟份量還行而已"
    },
    ...
]
```

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

## Git Branch
* https://hackmd.io/i0CooTWuSCi_Wc0d9wNB4A