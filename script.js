// Array for links to web pages with images
let linksArr = Array.from(document.querySelectorAll('.photo-card_cnt'));
// Array for scr links
let newArr = [];

// Pushing src links into array
linksArr.forEach((page) => {
  newArr.push(page.href);
})

console.log(newArr);