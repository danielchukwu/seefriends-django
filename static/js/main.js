// FLOATER JS .......................................................................
// part 1: floater remove - to remove the floater

console.log("Hello World")

const floater_exit = document.querySelector('.floater-exit')           
const floater_container = document.querySelector('.floater-container')
const floater_box = document.querySelector(".floater-box")       // purpose: for animation effect

removeFloater = function () {
   floater_container.classList.add("collapse")
   floater_box.classList.remove("floater-box")
}
floater_exit.addEventListener("click", removeFloater)




// FLOATER ADD....................
// part 2a:
// floater button: add
const post_button = document.querySelector(".post-button")
let options_div = document.querySelector(".options")
clicks = 0

// Purpose: when we refresh our page and click on the post button. The animation doesn't work, to fix this i added
//          the if statement
if (clicks === 0){
   floater_box.classList.remove("floater-box")
}

displayFloater = function () {
   floater_container.classList.remove("collapse")
   floater_box.classList.add("floater-box")
}

floaterEnable = function (event) {
   event.preventDefault()
   
   options_div.innerHTML = ""

   post_options = `
      <a href="/create-post/"><h3>Post</h3></a>
      <a href="/tell-form/"><h3>Tell</h3></a>
   `

   options_div.innerHTML += post_options
   displayFloater()
}

if (post_button){
   post_button.addEventListener("click", floaterEnable)
}

// Note: to syle the post_floater_box_indexpage you need to comment out the entire part 2



// part 2b
// flooter button: user profile
const user_button = document.querySelector(".user-button") 
// let options_div = declared already above
// displayFloater = function () {...} declared above and will be used to 

addUserOptions = function (event) {
   event.preventDefault()
   console.log("fired")

   options_div.innerHTML = ""

   user_options = `
      <a href="/users/update-profile/"><h3>Edit Profile</h3></a>
      <a href="tell-form.html"><h3>Settings</h3></a>
      <a href="/users/logout/"><h3>Logout</h3></a>
   `
   
   options_div.innerHTML += user_options
   displayFloater()
}
if (user_button !== null){
   user_button.addEventListener("click", addUserOptions)
}


// FLOATER Javascript logic Ends.........................................................




// POST PAGE
// objective 1: tap here to post disappears after 1 second of page load
const tapHeretopost = document.querySelector('#tapheretopost')

removeTapHereToPost = function () {
   tapHeretopost.toggleAttribute("hidden")
}

if (tapHeretopost !== null){
   setTimeout(removeTapHereToPost, 2000);
}

// objective 2: tap field to choose a file
const post_file_btn = document.querySelector("#post-file-btn")
// const default_post_btn = document.querySelectorAll("#post-file")

var loadFile = function(event) {
   var reader = new FileReader();
   reader.onload = function(){
      var output = document.getElementById('output');
      output.src = reader.result;
   };
   reader.readAsDataURL(event.target.files[0]);
};

if (post_file_btn !== null){
   post_file_btn.addEventListener('click', function() {
      console.log("image clicked on!")
   })
}



// COMMENT LOGIC
// Objective: double clicking on post to show like big-heart animation
const big_heart = document.querySelector(".big-heart")
// console.log(big_heart)

var heartPost = function () {
   big_heart.classList.remove("none")
   // console.log("double-clicked")
   if (!big_heart.classList.contains("none")){
      setTimeout(() => {
         big_heart.classList.add("none")
      }, 1000)
   }
}

// Objective: heart btn  click to like and click again to unlike
const heart_btn = document.querySelector("#heart-btn")
let heart_btn_parent = document.querySelector(".heart-p")
let like_status = true

likeOrUnlike = (event) => {
   
   if (event === false){
      console.log("like")
      like_status = true
      heart_btn_parent.innerHTML = ""
      
      like_heart = `
      <img src="images/icons/heart/heart-red.png" alt="" class="heart" id="heart-btn" onclick="likeOrUnlike(true)">
      `
      heart_btn_parent.innerHTML += like_heart
      
   }else {
      like_status = false
      console.log("unlike")
      heart_btn_parent.innerHTML = ""
      
      unlike_heart = `
      <img src="images/icons/heart/heart-white.png" alt="" class="heart" id="heart-btn" onclick="likeOrUnlike(false)">
      `
      heart_btn_parent.innerHTML += unlike_heart
   }
   return like_status
}


// if (heart_btn !== null){
//    heart_btn.addEventListener("click", likeOrUnlike)
// }



// EDIT PROFILE: show profile picture after selection logic