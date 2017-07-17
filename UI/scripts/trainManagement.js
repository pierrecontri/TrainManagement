/*

  Name: trainManagement.js
  Author: Pierre Contri
  Created: 22/06/2017

*/

function start_demo() {
  send_command('start_demo', { }, return_test_demo);
}

function stop_demo() {
  send_command('stop_demo', { }, return_test_demo);
}

function return_test_demo(jsonResponse) {
  var divReturnTestDemo = document.getElementById("test_demo_result");
  if(!divReturnTestDemo) return;

  divReturnTestDemo.innerHTML = jsonResponse.result;
}

function returnSwitch(jsonResponse) {
  if (jsonResponse != null && jsonResponse.result != null && jsonResponse.switchName != null && jsonResponse.switchValue != null) {
    var sw = document.getElementById(jsonResponse.switchName);
    if(sw != null)
    sw.className = (jsonResponse.result != "OK") ? "wayerror"
                   : ((jsonResponse.switchValue == 1) ? "wayon" : "wayoff");
  }
}

function createSwitchBlockCommand() {
  console.log("createSwitchBlockCommand");

  var lstSwitchs = document.getElementsByClassName("switchsContainer");

  for (i = 0, nbSwitchsContainer = lstSwitchs.length; i < nbSwitchsContainer; i++) {

    var switchCmd  = document.createElement('div');
    switchCmd.className = "switch";
    switchCmd.id = "SwitchBlock_" + i.toString();

    lstSwitchs[i].appendChild(switchCmd);
  }

}

function createSwitchElements() {
  console.log("createSwitchElements");

    // <div id="switch_1" class="switch">
    //   <table class="switchComponent">
    //     <tbody>
    //       <tr><td id="way1" onclick="javascript:send_command('set_switch_value', { 'switchName': this.id, 'switchValue': 'on'}, returnSwitch);">Way 1</td></tr>
    //       <tr><td id="way2">Way 2</td></tr>
    //     </tbody>
    //   </table>
    // </div> <!-- switch1 -->

  // define id number for ways
  var wayIdNb = 0;

  // get all div switch class
  var lstSwitchs = document.getElementsByClassName("switch");

  // create a table with 4 switchs railway foreach switch commands
  for (i = 0, nbSwitchs = lstSwitchs.length; i < nbSwitchs; i++) {

    var switchId = lstSwitchs[i].id;
    var idScNb = switchId.split('_').pop();

    // by default, 4 switchs in 1 command block
    for (k = 0; k < 4; k++) {
      tableSwitch = document.createElement('table');
      tableSwitch.id = "sc_" + k.toString();
      tableSwitch.className = "switchComponent";
      tbodySwitch = document.createElement('tbody');
      tableSwitch.appendChild(tbodySwitch);
  
      // create a td for each way
      for(j = 1; j < 3; j++) {
        trElem = document.createElement('tr');
        tbodySwitch.appendChild(trElem);
        tdElem = document.createElement('td');
        var idWay = wayIdNb++;
        tdElem.id = switchId + "_Switch_" + k.toString() + "_Way_" + idWay.toString();
        tdElem.className = "switchButton";
        tdElem.onclick = switch_click;
        tdElem.innerHTML = "Way&nbsp;" + (idWay + 1).toString();
        trElem.appendChild(tdElem);
      }
  
      // append the new child element
      lstSwitchs[i].appendChild(tableSwitch);
    }
  }
}

function initSwitchs() {
  console.log("initialize switchs buttons");
  var lstSwitchsButton = document.getElementsByClassName("switchButton");
  for (i = 0, nbSwitchs = lstSwitchsButton.length; i < nbSwitchs; i++) {
    setTimeout(fctGetSwitchValue, 500 * (i + 1), lstSwitchsButton[i].id);
  }
}

function fctGetSwitchValue(swId) {
  send_command('get_switch_value', { 'switchName': swId }, returnSwitch);
}

function fctSetSwitchValue(swId) {
  send_command('switch_value', { 'switchName': swId, 'switchValue': '1'}, null);
}

function switch_click() {
  this.className = "wayclick";
  // split id in two parts : id base & switch number
  var carSeparator = "_";
  var idArr = this.id.split(carSeparator);
  // get last number from id (switch number)
  var switchNumber = parseInt(idArr.pop());
  var idBase = idArr.join(carSeparator);

  var switchNumberBinomial = ( (switchNumber & 0xFE) == switchNumber ) ? switchNumber + 1 : switchNumber & 0xFE ;
  var idBinomialSwitch = idBase + "_" + switchNumberBinomial.toString();

  // set information to press switch button
  fctSetSwitchValue(this.id);
  // get information about binomial switch
  setTimeout(fctGetSwitchValue, 150, idBinomialSwitch);
  setTimeout(fctGetSwitchValue, 400, this.id);
}

function createWayTracking() {
  var canvas = document.getElementById('wayTracking');
  if (!canvas) return;

  var context = canvas.getContext('2d');
  var canvasW = canvas.width;
  var canvasH = canvas.height;
  var centerX = canvas.width / 2;
  var centerY = canvas.height / 2;
  var radius = 30;
  
  // context.beginPath();
  // context.arc(canvas.width - 100, 80, 70, 1.5 * Math.PI, 0, false);
  // context.lineWidth = 5;
  // context.strokeStyle = '#003300'; // blue or black
  // context.stroke();

  context.lineWidth = 2;


  // exterior rail hight
  context.beginPath();
  context.moveTo(80, 10);
  context.lineTo(canvasW - 130, 10);
  context.strokeStyle = 'black';
  context.stroke();

  // exterior right rail hight curve
  context.beginPath();
  //context.moveTo(canvasW - 200, canvasH - 250);
  context.arcTo(canvasW - 60, 10, canvasW - 60, 210, 70);
  context.strokeStyle = 'blue';
  context.stroke();

  // exterior right rail down curve
  context.beginPath();
  context.moveTo(canvasW - 60, canvasH - 100);
  context.arcTo(canvasW - 60, canvasH - 10, canvasW - 130, canvasH - 10, 70);
  context.strokeStyle = 'black';
  context.stroke();

  // interior left rail hight curve
  context.beginPath();
  context.arc(100, 20, 10, 1.5 * Math.PI, 0, false);
  context.arc(120, 20, 10, Math.PI, 0.5 * Math.PI, true);
  context.strokeStyle = 'yellow';
  context.stroke();

  // interior rail hight
  context.beginPath();
  context.moveTo(120, 30);
  context.lineTo(canvasW - 180, 30);
  context.strokeStyle = 'black';
  context.stroke();

  // interior right rail down curve
  context.beginPath();
  context.arc(canvasW - 180, 20, 10, 0.5 * Math.PI, 0, true);
  context.arc(canvasW - 160, 20, 10, Math.PI, 1.5 * Math.PI, false);
  context.strokeStyle = 'yellow';
  context.stroke();

  // park left rail hight curve
  context.beginPath();
  context.arc(250, 45, 15, 0.5 * Math.PI, 0, true);
  context.arc(280, 45, 15, Math.PI, 1.5 * Math.PI, false);
  context.strokeStyle = 'purple';
  context.stroke();

  // rail park left hight
  context.beginPath();
  context.moveTo(80, 60);
  context.lineTo(250, 60);
  context.strokeStyle = 'black';
  context.stroke();

  // park left rail hight curve
  context.beginPath();
  context.arc(220, 70, 10, 0.5 * Math.PI, 0, true);
  context.arc(240, 70, 10, Math.PI, 1.5 * Math.PI, false);
  context.strokeStyle = 'purple';
  context.stroke();

  // rail park left down
  context.beginPath();
  context.moveTo(80, 80);
  context.lineTo(220, 80);
  context.strokeStyle = 'black';
  context.stroke();

  // rail park right selector
  context.beginPath();
  context.moveTo(260, 60);
  context.lineTo(300, 60);
  context.strokeStyle = 'pink';
  context.stroke();

  // rail park right
  context.beginPath();
  context.moveTo(300, 60);
  context.lineTo(500, 60);
  context.strokeStyle = 'black';
  context.stroke();

  // interior left rail down curve
  context.beginPath();
  context.arc(110, canvasH - 45, 15, 0.5 * Math.PI, 0, true);
  context.arc(140, canvasH - 45, 15, Math.PI, 1.5 * Math.PI, false);
  context.strokeStyle = 'red';
  context.stroke();

  // interior rail down
  context.beginPath();
  context.moveTo(140, canvasH - 60);
  context.lineTo(canvasW - 190, canvasH - 60);
  context.strokeStyle = 'black';
  context.stroke();

  // interior right rail down curve
  context.beginPath();
  context.arc(canvasW - 190, canvasH - 45, 15, 1.5 * Math.PI, 0, false);
  context.arc(canvasW - 160, canvasH - 45, 15, Math.PI, 0.5 * Math.PI, true);
  context.strokeStyle = 'red';
  context.stroke();

  // medium left rail down curve
  context.beginPath();
  context.arc(85, canvasH - 105, 75, 0.5 * Math.PI, Math.PI);
  context.strokeStyle = 'green';
  context.stroke();

  // medium rail down
  context.beginPath();
  context.moveTo(80, canvasH - 30);
  context.lineTo(canvasW - 130, canvasH - 30);
  context.strokeStyle = 'black';
  context.stroke();

  // medium right rail down curve
  context.beginPath();
  context.arc(canvasW - 135, canvasH - 105, 75, 0, 0.5 * Math.PI);
  context.strokeStyle = 'green';
  context.stroke();

  // exterior rail down
  context.beginPath();
  context.moveTo(80, canvas.height - 10);
  context.lineTo(canvasW - 130, canvasH - 10);
  context.strokeStyle = 'black';
  context.stroke();

  // exterior left rail hight curve
  context.beginPath();
  //context.moveTo(10, 80);
  context.arc(80, 80, 70, Math.PI, 1.5 * Math.PI);
  context.strokeStyle = 'blue';
  context.stroke();

  // exterior left rail down curve
  context.beginPath();
  context.moveTo(10, canvasH - 100);
  context.arcTo(10, canvasH - 10, canvasW - 130, canvasH - 10, 70);
  context.strokeStyle = 'black';
  context.stroke();
}

// ----- Main Init -----
function initApplication() {
  createWayTracking();
  createSwitchBlockCommand();
  createSwitchElements();
  console.log("Application initializing done");
}