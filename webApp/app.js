var config = {
  'accel_topic': 'ideahacks2019_200_accel',
  'rangefinder_topic': 'ideahacks2019_200_rangefinder',
  'image_topic': 'ideahacks2019_200_images',
  'qos': 2
}
var safeGreen = '#4BED81'
var dangerRed = '#ED6A5A'
var brightGreen = '#00FF00'
var counter = 1
var timeout = 2000
var listeners = []
var inDanger = false

class mqtt_guy {
	constructor(topic) {
    this.topic = topic
    this.connect = this.connect.bind(this)
    this.subscribe = this.subscribe.bind(this)
    this.publish = this.publish.bind(this)
    //Using the HiveMQ public Broker
    this.id = counter;
    this.client = new Messaging.Client("broker.mqttdashboard.com", 8000, `${this.id}`);
    //this.client = new Messaging.Client("172.30.47.196", 1883, `${this.id}`);
    this.client.id = this.id

    //Gets  called if the websocket/mqtt connection gets disconnected for any reason
    this.client.onConnectionLost = function (responseObject) {
        //Depending on your scenario you could implement a reconnect logic here
        //alert("connection lost: " + responseObject.errorMessage);
        this.connect()
    };
    //Gets called whenever you receive a message for your subscriptions
    this.client.onMessageArrived = this.on_message.bind(this)
    //Connect Options
    this.options = {
        timeout: 3,
        //Gets Called if the connection has sucessfully been established
        onSuccess: function () {
            console.log("Connected");
            return true
        },
        //Gets Called if the connection could not be established
        onFailure: function (message) {
            alert("Connection failed: " + message.errorMessage);
        }
    };
    //once initialized, connect to server/broker
    this.connect()
  }
  //connect to server/broker thing
  connect() {
    this.client.connect(this.options)
    setTimeout(this.subscribe, timeout)
  }
  //subscribe to topic, defined in constructor
  subscribe() {
    this.client.subscribe(this.topic, {qos: config.qos});
    console.log('Subscribed');
  }

  //Creates a new Messaging.Message Object and sends it to the HiveMQ MQTT Broker
  publish(evt) {
    let payload = (evt.target.innerHTML)
    //Send your message (also possible to serialize it as JSON or protobuf or just use a string, no limitations)
    var message = new Messaging.Message(payload);
    message.destinationName = this.topic;
    message.qos = config.qos;
    this.client.send(message);
    //$(`#input_${this.id}`).val('')
  }

  on_message(message) {
      //Do something with the push message you received
      console.log("recieved ", message.payloadString, " from ", message.destinationName)
      var status = ''
      if(message.payloadString == 0){
        if(inDanger){
          danger(false)
        }
        status = 'No sweat champ'
      }
      else if (message.payloadString == 1){
        if(!inDanger){
          danger(true)
        }
        status = "Aw Geez Rick.. Someone's stealing our stuff!"
      }
      $(`#messages_${this.id}`).append('<p clas="hidden">' + status + '</p>');
      let speed = 100/message.payloadString.length
      typeEffect($(`#messages_${this.id} p`).last(), speed)

      try {
        //console.log(JSON.parse(message.payloadString))
        reconstructBase64String(JSON.parse(message.payloadString))
      } catch (e) {
        //console.log(e)
      }
  };

  makeInterface() {
    if(this.topic != config.image_topic){
      $('#status-boxes').append(`<div class="messages-wrapper"><h3>${this.topic}:</h3><div class="messages" id="messages_${this.id}"></div></div>`)
      // $('#publishers').append(`<div class='button' id="text-1">I'LL FIGHT YOU</div>
      //   <div class='button' id="text-2">ONE DOES NOT SIMPLY SEND DATA OVER WIFI</div>`)
      // document.getElementById("text-1").addEventListener('click', this.publish)
      // document.getElementById("text-2").addEventListener('click', this.publish)
    }
    else {
      //$('#image-container').append(`<div class="messages-wrapper"><h3>Messages:</h3><div class="messages" id="messages_${this.id}"></div></div>`)
      // $('#publishers').append(`<div class='button' id="image-1"">THE ONE PERCENT HOLD 99% AND THE 99% HOLD ONE PERCENT </div>
      //   <div class='button' id="image-2"">MAKE AMERICA GREAT AGAIN</div>`)
      // document.getElementById("image-1").addEventListener('click', this.publish)
      // document.getElementById("image-2").addEventListener('click', this.publish)
    }
  }
}


function typeEffect(element, speed) {
	var text = $(element).text();
	$(element).html('');
  $(element).removeClass('hidden')

  var i = 0;
	var timer = setInterval(function() {
					if (i < text.length) {
						$(element).append(text.charAt(i));
						i++;
					} else {
						clearInterval(timer);
          }
				}, speed);
  $(element).parent().animate({
      scrollTop: $(element).parent()[0].scrollHeight
    }, 400)
}

$(document).ready(function() {
  var accelListener = new mqtt_guy(config.accel_topic)
  counter += 1;
  var rangefinderListener = new mqtt_guy(config.rangefinder_topic)
  counter += 1;
  var imageListener = new mqtt_guy(config.image_topic)
  listeners = [accelListener, rangefinderListener, imageListener]
  accelListener.makeInterface();
  rangefinderListener.makeInterface();
  imageListener.makeInterface();
  document.getElementById('reconnect').addEventListener('click', reconnect)
})

function reconnect() {
  for (var index in listeners) {
    console.log(listeners[index])
    listeners[index].connect()
  }
}
var pictures = []

function reconstructBase64String(pChunk) {
    //creates a new picture object if receiving a new picture, else adds incoming strings to an existing picture
    if (pictures[pChunk["pic_id"]]==null) {
        pictures[pChunk["pic_id"]] = {"count":0, "total":pChunk["size"], pieces: {}, "pic_id": pChunk["pic_id"]};

        pictures[pChunk["pic_id"]].pieces[pChunk["pos"]] = pChunk["data"];

    }

    else {
        pictures[pChunk["pic_id"]].pieces[pChunk["pos"]] = pChunk["data"];
        let pieces =  Object.keys(pictures[pChunk["pic_id"]].pieces).length
        if (pieces == pictures[pChunk["pic_id"]].total) {
          console.log("Image reception compelete");
          var str_image="";

          for (var i = 1; i <= pictures[pChunk["pic_id"]].total; i++)
              str_image = str_image + pictures[pChunk["pic_id"]].pieces[i];

          //displays image
          //imagebytes = atob(str_image)
          var source = 'data:image/jpg;base64,'+str_image;
          console.log(source)
          var myImageElement = document.getElementById("picture_to_show");
          myImageElement.setAttribute('class', "thing")
          myImageElement.setAttribute('src', source)
        }
    }
}

function danger(status) {
  element = document.getElementById('status')
  inDanger = status
  if(status == true){
    element.innerHTML = "DANGER WILL ROBINSON"
    $('header').css('backgroundColor', dangerRed)
    $('.messages-wrapper').css('color', dangerRed)
  }
  else {
    element.innerHTML = "Safe and Sound"
    $('header').css('backgroundColor', safeGreen)
    $('.messages-wrapper').css('color', brightGreen)
  }
}
