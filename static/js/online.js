// javascript - For maintaining the online status of a user
console.log('ONLINE JS LIVE')

let url_online = `ws://${window.location.host}/ws/online/`

const onlineSocket = new WebSocket(url_online)

onlineSocket.onmessage = function (e) {
   data = JSON.parse(e.data)
   console.log('Online:', data)
}