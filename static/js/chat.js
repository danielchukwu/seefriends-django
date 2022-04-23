// javascript - This javascript handles our message page
// Section 1: 
// Scroll to the bottom of the page on load
// window.scrollTo(0, document.body.clientHeight);
window.scrollTo(0, document.body.scrollHeight);


console.log("Sanity Check: message js works!....")
let focus_on_input = document.querySelector("#message").focus()
let user = document.querySelector('.message-header')
let user_id = user.getAttribute('data-user')
console.log('user:', user_id)

let url = `ws://${window.location.host}/ws/message/${user_id}/`
const messageSocket = new WebSocket(url)

let get_time = function () {
   let current = new Date()
   let hour = null
   let minutes = null
   if (current.getHours() < 10){
      hour = `0${current.getHours()}`
   }
   else (
      hour = current.getHours()
   )
   if (current.getMinutes() < 10){
      minutes= `0${current.getMinutes()}`
   }
   else (
      minutes= current.getMinutes()
   )
   
   return `${hour}:${minutes}`
}

messageSocket.onmessage = function (e) {
   data = JSON.parse(e.data)
   console.log('Data:', data)

   if (data.type == 'chat' && data.message != ''){
      let main = document.getElementById('main')
      let current = new Date()
      if (messageSent == data.message){
         main.insertAdjacentHTML('beforeend', `
         <div class="msg-block-me">
            <div class="msg-box-me">
               <p class="no-margin">
                  <span>${messageSent}</span> 
                  <small class="msg-time grey">${get_time()}</small>
               </p>
            </div>
            <div class="msg-seen">
               <div class="c1"></div>
               <div class="c1"></div>
            </div>
         </div>
         `)
      } 
      else {
         main.insertAdjacentHTML('beforeend', `
         <div class="msg-block">
            <div class="msg-box">
               <p class="no-margin">
                  <span>${data.message}</span>
                  <small class="msg-time grey">${current.getHours()}:${current.getMinutes()}</small>
               </p>
            </div>
         </div>
         `)
      }
      window.scrollTo(0, document.body.clientHeight);
   }

   if (data.seen == true && data.other_id != user_id){
      unseens = document.querySelectorAll('.c1:not(.msg-blue)')
      unseens.forEach(div => {
         div.classList.add('msg-blue')
      });
}
}

messageSocket.onopen = function () {
   messageSocket.send(JSON.stringify({
      'message': ''
   }))
}


let form = document.getElementById('form')
let messageSent = ''
form.addEventListener('submit', (e) => {
   e.preventDefault()
   let message = e.target.body.value
   console.log('Message:', message)
   messageSocket.send(JSON.stringify({
      'message': message
   }))

   messageSent = message
   form.reset()
})