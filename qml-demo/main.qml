import QtQuick 2.15 

import QtQuick.Controls 2.15 

import QtWebSockets 1.1 

 

ApplicationWindow { 

    visible: true 

    width: 500 

    height: 400 

    title: "Vosk Multi-Language Speech Recognition" 

 

    property string wsStatus: "Disconnected" 

    property string recognizedText: "" 

    property string selectedModel: "vosk-model-small-en-in-0.4" 

 

    WebSocket { 

        id: socket 

        url: "ws://127.0.0.1:8765" 

        active: true   // <-- Keeps connection alive automatically! 

 

        onStatusChanged: { 

            if (status === WebSocket.Open) { 

                wsStatus = "Connected" 

                console.log("qml: WS connected") 

            } else if (status === WebSocket.Closed) { 

                wsStatus = "Disconnected" 

                console.log("qml: WS closed — retrying in 2s") 

                // auto-reconnect after 2s 

                reconnectTimer.restart() 

            } else { 

                wsStatus = "Unknown" 

                console.log("qml: WS status:", status) 

            } 

        } 

 

        onTextMessageReceived: function(message) { 

            console.log("qml: Got message:", message) 

            var msg = JSON.parse(message) 

            if (msg.partial) recognizedText = "Partial: " + msg.partial 

            if (msg.final) recognizedText = "Final: " + msg.final 

            if (msg.status) recognizedText = msg.status 

        } 

    } 

 

    Timer { 

        id: reconnectTimer 

        interval: 2000; repeat: false 

        onTriggered: { 

            console.log("qml: Reconnecting WebSocket…") 

            socket.active = true 

        } 

    } 

 

    Column { 

        anchors.centerIn: parent 

        spacing: 12 

 

        Text { text: "WebSocket Status: " + wsStatus; font.pixelSize: 16 } 

                 

        ComboBox { 

            id: languageBox 

            width: parent.width - 40 

            model: [ 

                "vosk-model-small-en-in-0.4", 

                "vosk-model-small-hi-0.22", 

                "vosk-model-small-nl-0.22", 

                "vosk-model-small-es-0.42" 

            ] 

            onCurrentTextChanged: selectedModel = currentText 

        } 

      

        TextArea { 

            id: transcript 

            width: parent.width - 40 

            height: 150 

            wrapMode: TextArea.Wrap 

            text: recognizedText 

            readOnly: true 

        } 

      

        Button { 

            text: "Load Model" 

            onClicked: { 

                if (socket.status === WebSocket.Open) { 

                    console.log("qml: Sending load for", selectedModel) 

                    socket.sendTextMessage(JSON.stringify({ cmd: "load", model: selectedModel })) 

                } else { 

                    console.log("qml: WS not open") 

                } 

            } 

        } 

                 

        Button { 

            text: "Start Recording" 

            onClicked: { 

                if (socket.status === WebSocket.Open) { 

                    socket.sendTextMessage(JSON.stringify({ cmd: "start" })) 

                } else { 

                    console.log("qml: WS not open") 

                }  

            } 

        } 

             

        Button { 

            text: "Stop Recording" 

            onClicked: {   

                if (socket.status === WebSocket.Open) { 

                    socket.sendTextMessage(JSON.stringify({ cmd: "stop" })) 

                } else { 

                    console.log("qml: WS not open") 

                } 

            } 

        } 

    } 

} 
