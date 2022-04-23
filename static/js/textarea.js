// JS: Javascript
// Obj: 1. make text area grow  2. submit form

//1.
const textarea = document.getElementById('text-area')
textarea.focus()
textarea.addEventListener("keyup", e=> {
   textarea.style.height = '10px';
   let schieght = e.target.scrollHeight
   textarea.style.height = `${schieght -28}px`;
   window.scrollTo(0, document.body.scrollHeight);
} );

//2.
const done = document.getElementById('done')   // console.log(done)
const pt_form = document.getElementById('form')   // console.log(pt_form)

const post_img = document.getElementById('output')
textarea.addEventListener('keyup', e=> {  // purpose: text eventlistner -> changes the done from black to blue if you are good to submit and back to black if you aren't
   let capvalue = e.target.value
   if (post_img){
      if (capvalue.length > 5 && post_img.src != ''){
         done.src = 'images/icons/done/check-markbl-32.png'
      } else (
         done.src = 'images/icons/done/check-markb-32.png'
      )
   } else {
      if (capvalue.length > 5){
         done.src = 'images/icons/done/check-markbl-32.png'
      } else (
         done.src = 'images/icons/done/check-markb-32.png'
      )
   }
})


done.addEventListener('click', e=> {
   e.preventDefault()
   
   let value = pt_form.caption.value
   if (post_img){
      if (value.length > 5 & post_img.src != ''){
         pt_form.submit()
      }
   }else {
      if (value.length > 5){
         pt_form.submit()
      }
   }
})