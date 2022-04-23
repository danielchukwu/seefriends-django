//JS - javascript
// purpose - to implement a like and dislike logic
console.log('liketell.js live')

const tcon = document.querySelectorAll('.tcon')
for(let i=0; i<tcon.length; i++){
   let thb = tcon[i].querySelector('.theartb')
   let thr = tcon[i].querySelector('.theartr')
   let lcount = tcon[i].querySelector('.lcount')
   console.log(thb)
   console.log(thr)
   
   thb.addEventListener('click', ()=> {
      thb.classList.add('none')
      thr.classList.remove('none')
      lcount.classList.add('text-pink')
   })
   thr.addEventListener('click', ()=> {
      thr.classList.add('none')
      thb.classList.remove('none')
      lcount.classList.remove('text-pink')
   })
}