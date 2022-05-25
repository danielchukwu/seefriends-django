// JS - javascript
// purpose - to implement a like and dislike logic
// dones - 1. Big heart Like implementation |  2. Small heart like implementation
console.log('likepost.js live')

// connect: websocket connection

let returnLikeSocket = function (id) {
   let url_lp = `ws://${window.location.host}/ws/likepost/${id}/`
   let ls = new WebSocket(url_lp)
   return ls
}

// 1
// Objective: double clicking on post to show like big-heart animation
const pc = document.querySelectorAll(".content-box")

var showBigHeart = function (bg) {
   bg.classList.remove("none")
   if (!bg.classList.contains("none")){
      setTimeout(() => {
         bg.classList.add("none")
      }, 1000)
   }
}

for (let i=0; i < pc.length; i++){
   pc[i].addEventListener('dblclick', (e)=> {
      let bg = pc[i].querySelector('.big-heart')
      let pid = pc[i].dataset.pid  // console.log('Project id:', pid)
      let lp_count = heart_p[i].querySelector('.like_count')  // console.log('lp_count:', lp_count)
      
      let likeSocket = returnLikeSocket(pid)
      likeSocket.onopen = function () {
         likeSocket.send(JSON.stringify({'type': 'like'}))
      }
      showBigHeart(bg)
      let shr = pc[i].querySelector('.heartr')
      if (shr.classList.contains('none')) {
         shr.classList.remove('none')
         lp_count.innerHTML = parseInt(lp_count.innerHTML)+1
      }
   })
}


// 2
// // Objective: heart btn click to like and click again to unlike
// update: 0.1
const heart_p = document.querySelectorAll('.content-box')

for (let i=0; i<heart_p.length; i++){
   let hw = heart_p[i].querySelector('.heartw')
   let hr = heart_p[i].querySelector('.heartr')
   let lp_count = heart_p[i].querySelector('.like_count')  // console.log('lp_count:', lp_count)

   hw.addEventListener('click', ()=> {
      hr.classList.remove('none')

      let pid = hr.dataset.pid  // console.log('Project id:', pid)
      let likeSocket = returnLikeSocket(pid)
      likeSocket.onopen = function () {
         likeSocket.send(JSON.stringify({'type': 'like'}))
      }

      // Increment Like
      lp_count.innerHTML = parseInt(lp_count.innerHTML)+1
   })
   hr.addEventListener('click', ()=> {
      hr.classList.add('none')
      let pid = hr.dataset.pid  // console.log('Project id:', pid)
      let likeSocket = returnLikeSocket(pid)
      likeSocket.onopen = function () {
         likeSocket.send(JSON.stringify({'type': 'dislike'}))
      }

      // Decrement Like
      lp_count.innerHTML = parseInt(lp_count.innerHTML)-1
   })
}
console.log('DOWN')