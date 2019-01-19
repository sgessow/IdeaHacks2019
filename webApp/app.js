var config = {
  'text_channel': 'ideahacks2019_200_text',
  //'text_channel': '172.30.47.196',
  'image_channel': 'ideahacks2019_200_images',
  'qos': 2
}

var counter = 1

class mqtt_guy {
	constructor(topic) {
    this.channel = topic
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
    this.client.onMessageArrived = function (message) {
        //Do something with the push message you received
        console.log("recieved ", message.payloadString, " from ", message.destinationName)
        $(`#messages_${this.clientId}`).append('<p clas="hidden">' + message.payloadString + '</p>');
        let speed = 666/message.payloadString.length
        typeEffect($(`#messages_${this.clientId} p`).last(), speed)
    };
    //Connect Options
    this.options = {
        timeout: 3,
        //Gets Called if the connection has sucessfully been established
        onSuccess: function () {
            console.log("Connected");
        },
        //Gets Called if the connection could not be established
        onFailure: function (message) {
            alert("Connection failed: " + message.errorMessage);
        }
    };
    this.connect()
  }

  connect() {
    this.client.connect(this.options)
  }

  subscribe() {
    this.client.subscribe(this.channel, {qos: config.qos});
    console.log('Subscribed');
  }

  //Creates a new Messaging.Message Object and sends it to the HiveMQ MQTT Broker
  publish(evt) {
    let payload = (evt.target.innerHTML)
    //Send your message (also possible to serialize it as JSON or protobuf or just use a string, no limitations)
    var message = new Messaging.Message(payload);
    message.destinationName = this.channel;
    message.qos = config.qos;
    this.client.send(message);
    $(`#input_${this.id}`).val('')
  }

  makeInterface() {
    if(this.channel == config.text_channel){
      $('#text-container').append(`<div class="messages-wrapper"><h3>Messages:</h3><div class="messages" id="messages_${this.id}"></div></div>`)
      $('#publishers').append(`<div class='button' id="text-1">I'LL FIGHT YOU</div>
        <div class='button' id="text-2">ONE DOES NOT SIMPLY SEND DATA OVER WIFI</div>`)
      document.getElementById("text-1").addEventListener('click', this.publish)
      document.getElementById("text-2").addEventListener('click', this.publish)
    }
    else {
      $('#image-container').append(`<div class="messages-wrapper"><h3>Messages:</h3><div class="messages" id="messages_${this.id}"></div></div>`)
      $('#publishers').append(`<div class='button' id="image-1"">THE ONE PERCENT HOLD 99% AND THE 99% HOLD ONE PERCENT </div>
        <div class='button' id="image-2"">MAKE AMERICA GREAT AGAIN</div>`)
      document.getElementById("image-1").addEventListener('click', this.publish)
      document.getElementById("image-2").addEventListener('click', this.publish)
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
    }, 1000)
}

$(document).ready(function() {
  var textListener = new mqtt_guy(config.text_channel)
  counter += 1;
  var imageListener = new mqtt_guy(config.image_channel)
  textListener.makeInterface();
  imageListener.makeInterface();

  document.getElementById('subscribe').addEventListener('click',function() {
    textListener.subscribe();
    imageListener.subscribe();
  })
})

function reconstructBase64String(chunk) {
    pChunk = JSON.parse(chunk["d"]);

    //creates a new picture object if receiving a new picture, else adds incoming strings to an existing picture
    if (pictures[pChunk["pic_id"]]==null) {
        pictures[pChunk["pic_id"]] = {"count":0, "total":pChunk["size"], pieces: {}, "pic_id": pChunk["pic_id"]};

        pictures[pChunk["pic_id"]].pieces[pChunk["pos"]] = pChunk["data"];

    }

    else {
        pictures[pChunk["pic_id"]].pieces[pChunk["pos"]] = pChunk["data"];
        pictures[pChunk["pic_id"]].count += 1;


        if (pictures[pChunk["pic_id"]].count == pictures[pChunk["pic_id"]].total) {
        console.log("Image reception compelete");
        var str_image="";

        for (var i = 0; i <= pictures[pChunk["pic_id"]].total; i++)
            str_image = str_image + pictures[pChunk["pic_id"]].pieces[i];

        //displays image
        var source = 'data:image/jpeg;base64,'+str_image;
        var myImageElement = document.getElementById("picture_to_show");
        myImageElement.href = source;
        }

    }

}
