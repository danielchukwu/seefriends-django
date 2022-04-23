// JS - javascript
// purpose - to implement a like and dislike logic
// dones - 1. Big heart Like implementation |  2. Small heart like implementation
console.log('likepost.js live')

// 1
// Objective: double clicking on post to show like big-heart animation
const parent_container = document.querySelectorAll(".content-1")

var showBigHeart = function (bg) {
   bg.classList.remove("none")
   if (!bg.classList.contains("none")){
      setTimeout(() => {
         bg.classList.add("none")
      }, 1000)
   }
}

for (let i=0; i < parent_container.length; i++){
   parent_container[i].addEventListener('dblclick', (e)=> {
      let bg = parent_container[i].querySelector('.big-heart')
      showBigHeart(bg)
      let shr = parent_container[i].querySelector('.heartr')
      if (shr.classList.contains('none')) {shr.classList.remove('none')}
   })
}


// 2
// // Objective: heart btn click to like and click again to unlike
// update: 0.1
const heart_p = document.querySelectorAll('.content-box')

for (let i=0; i<heart_p.length; i++){
   let hw = heart_p[i].querySelector('.heartw')
   let hr = heart_p[i].querySelector('.heartr')

   hw.addEventListener('click', ()=> {
      hr.classList.remove('none')
   })
   hr.addEventListener('click', ()=> {
      hr.classList.add('none')
   })
}