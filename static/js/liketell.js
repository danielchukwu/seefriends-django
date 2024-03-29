//JS - javascript
// purpose - to implement a like and dislike logic
console.log('liketell.js live')

let returnLikeTellSocket = function (id) {
   let url_lp = `ws://${window.location.host}/ws/liketell/${id}/`
   return new WebSocket(url_lp)
}

const tcon = document.querySelectorAll('.tcon')
for(let i=0; i<tcon.length; i++){
   let thb = tcon[i].querySelector('.theartb') // console.log(thb)
   let thr = tcon[i].querySelector('.theartr') // console.log(thr)
   let lcount = tcon[i].querySelector('.lcount')
   let tid = tcon[i].dataset.tid

   
   thb.addEventListener('click', ()=> {
      thb.classList.add('none')
      thr.classList.remove('none')
      lcount.classList.add('text-pink')

      // like logic
      let likeTellSocket = returnLikeTellSocket(tid)
      likeTellSocket.onopen = function () {
         likeTellSocket.send(JSON.stringify({
            'type': 'like'
         }))
      }

      // Increment like count
      lcount.innerHTML = parseInt(lcount.innerHTML)+1
   })
   thr.addEventListener('click', ()=> {
      thr.classList.add('none')
      thb.classList.remove('none')
      lcount.classList.remove('text-pink')
      
      // like logic
      let likeTellSocket = returnLikeTellSocket(tid)
      likeTellSocket.onopen = function () {
         likeTellSocket.send(JSON.stringify({
            'type': 'dislike'
         }))
      }
      
      // Increment like count
      lcount.innerHTML = parseInt(lcount.innerHTML)-1
   })
}