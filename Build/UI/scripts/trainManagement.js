/*

  Name: trainManagement.js
  Author: Pierre Contri
  Created: 22/06/2017

*/

function start_demo() {
  send_command('demo', 'start', { }, return_test_demo);
}

function stop_demo() {
  send_command('demo', 'stop', { }, return_test_demo);
}

function return_test_demo(jsonResponse) {
  var divReturnTestDemo = document.getElementById("test_demo_result");
  if(!divReturnTestDemo) return;

  divReturnTestDemo.innerHTML = jsonResponse.result;
}

function returnSwitch(jsonResponse) {
  if (jsonResponse != null && jsonResponse.result != null && jsonResponse.switchName != null && jsonResponse.switchValue != null) {
    var sw = document.getElementById(jsonResponse.switchName);
    if(sw != null) {
      var classWayResponse = (jsonResponse.result != "OK") ? "wayerror"
                             : ((jsonResponse.switchValue == 1) ? "wayon" : "wayoff");
      var re = /(wayerror)|(wayon)|(wayoff)|(wayclick)/i;
      sw.className = sw.className.replace(re, "") + " " + classWayResponse;
    }
    var tmpSwitchName = "Way_" + jsonResponse.switchName.split('_').pop();
    switchWayCache[tmpSwitchName] = jsonResponse.switchValue;
  }
}

function createSwitchBlockCommand() {
  console.log("createSwitchBlockCommand");

  // create bi states switch, and one state switch
  var lstStates = {
       'bistableSwitch' : 'twoWaysSwitch', // switchsContainer
       'monostableSwitch' : 'oneWaySwitch' // switchsContainer
  }

  var incSwitchBlocks = 0;

  for(var tmpState in lstStates) {

    var lstSwitchs = document.getElementsByClassName(tmpState);
  
    for (i = 0, nbSwitchsContainer = lstSwitchs.length; i < nbSwitchsContainer; i++) {
  
      var switchCmd  = document.createElement('div');
      switchCmd.className = lstStates[tmpState];
      switchCmd.id = "SwitchBlock_" + (incSwitchBlocks++).toString();
  
      lstSwitchs[i].appendChild(switchCmd);
    }

  }

}

var switchWayCache = {};

function createSwitchElements() {
  console.log("createSwitchElements");

    // <div id="switch_1" class="switch">
    //   <table class="switchComponent">
    //     <tbody>
    //       <tr><td id="way1" onclick="javascript:send_command('train_control', 'set_switch_value', { 'switchName': this.id, 'switchValue': 'on'}, returnSwitch);">Way 1</td></tr>
    //       <tr><td id="way2">Way 2</td></tr>
    //     </tbody>
    //   </table>
    // </div> <!-- switch1 -->

  // define id number for ways
  var wayIdNb = 0;

  // get all div switch class
  var lstSwitchs = document.getElementsByClassName("twoWaysSwitch");

  // create a table with 4 switchs railway foreach switch commands
  for (var i = 0, nbSwitchs = lstSwitchs.length; i < nbSwitchs; i++) {

    var switchId = lstSwitchs[i].id;
    var idScNb = switchId.split('_').pop();

    // by default, 4 switchs in 1 command block
    for (var k = 0; k < 4; k++) {
      var divSwitch = document.createElement('div');
      divSwitch.className = "divSwitchComponent";
      tableSwitch = document.createElement('table');
      tableSwitch.id = "sc_" + k.toString();
      tableSwitch.className = "switchComponent";
      tbodySwitch = document.createElement('tbody');
      tableSwitch.appendChild(tbodySwitch);
  
      // create a td for each way
      for(var j = 1; j < 3; j++) {
        var trElem = document.createElement('tr');
        tbodySwitch.appendChild(trElem);
        var tdElem = document.createElement('td');
        var idWay = wayIdNb++;
        tdElem.id = switchId + "_Switch_" + k.toString() + "_Way_" + idWay.toString();
        tdElem.className = "switchButton twoWays";
        tdElem.onclick = switch_click;
        tdElem.innerHTML = "Way&nbsp;" + (idWay + 1).toString();
        trElem.appendChild(tdElem);
      }
  
      // append the new child element
      divSwitch.appendChild(tableSwitch);
      lstSwitchs[i].appendChild(divSwitch);
    }
  }



  // get all div switch class
  var lstMonoSwitchs = document.getElementsByClassName("oneWaySwitch");

  // create a table with 4 switchs railway foreach switch commands
  for (var l = 0, nbMonoSwitchs = lstMonoSwitchs.length; l < nbMonoSwitchs; l++) {

    var switchId = lstMonoSwitchs[l].id;
    var idScNb = switchId.split('_').pop();

    // by default, 4 switchs in 1 command block
      var divSwitch = document.createElement('div');
      divSwitch.className = "divMonoSwitchComponent";
      var tableSwitch = document.createElement('table');
      tableSwitch.id = "sc_" + l.toString();
      tableSwitch.className = "monoSwitchComponent switchComponent";
      var tbodySwitch = document.createElement('tbody');
      tableSwitch.appendChild(tbodySwitch);

      // create a td for each way
      //for(var n = 1; n < 3; n++) {
        var trElem = document.createElement('tr');
        tbodySwitch.appendChild(trElem);

    for (var m = 0; m < 4; m++) {
  
        var tdElem = document.createElement('td');
        var idWay = wayIdNb++;
        tdElem.id = switchId + "_Switch_" + m.toString() + "_Way_" + idWay.toString();
        tdElem.className = "switchButton oneWay";
        tdElem.onclick = switch_click;
        tdElem.innerHTML = "Way&nbsp;" + (idWay + 1).toString();
        trElem.appendChild(tdElem);
      //}
    }

      // append the new child element
      divSwitch.appendChild(tableSwitch);
      lstMonoSwitchs[l].appendChild(divSwitch);
  

  }

}

function emergencyStop() {
  send_command('train_control', 'emergency_stop', { }, returnEmergencyStop);
}

function returnEmergencyStop() {

}

function initSwitchs() {
  console.log("initialize switchs buttons");
  var lstSwitchsButton = document.getElementsByClassName("switchButton");
  for (i = 0, nbSwitchs = lstSwitchsButton.length; i < nbSwitchs; i++) {

    var is_persist = isPermanentSwitch(lstSwitchsButton[i].id);

    setTimeout(fctBindSwitchValue, 500 * (i + 1), lstSwitchsButton[i].id, is_persist);
  }
  setTimeout(drawWayTracking, 9000);
}

function fctBindSwitchValue(swId, is_persist = false) {
  send_command('train_control', 'bind_switch', { 'switchName': swId, 'isPersistent': is_persist }, returnSwitch);
}

function fctGetSwitchValue(swId, is_persist = false) {
  send_command('train_control', 'get_switch_value', { 'switchName': swId, 'isPersistent': is_persist }, returnSwitch);
}

function fctSetSwitchValue(swId, is_persist = false) {
  send_command('train_control', 'switch_value', { 'switchName': swId, 'isPersistent': is_persist}, null);
}

function isPermanentSwitch(switchId) {
  // split id in two parts : id base & switch number
  var carSeparator = "_";
  var idArr = switchId.split(carSeparator);

  var switchBlockIdCalc = "switchsContainer_" + (parseInt(idArr[1]) + 1).toString();
  var switchContainer = document.getElementById(switchBlockIdCalc);

  return (switchContainer) ? switchContainer.className.split(' ').indexOf("permanentSwitch") > -1 : false;
}

function isBistableSwitch(switchId) {
  var sw = document.getElementById(switchId);
  return (sw) ? sw.className.split(' ').indexOf("twoWays") > -1 : false;
}

function switch_click() {

  var re = /(wayerror)|(wayon)|(wayoff)|(wayclick)/i;
  this.className = (this.className.replace(re, "") + " wayclick").replace("  ", " ");
  // split id in two parts : id base & switch number
  var carSeparator = "_";
  var idArr = this.id.split(carSeparator);
  // get last number from id (switch number)
  var switchNumber = parseInt(idArr.pop());
  var idBase = idArr.join(carSeparator);

  var switchNumberBinomial = ( (switchNumber & 0xFE) == switchNumber ) ? switchNumber + 1 : switchNumber & 0xFE ;
  var idBinomialSwitch = idBase + "_" + switchNumberBinomial.toString();

  // get information: is permanent switch
  var is_persist = isPermanentSwitch(this.id);

  // set information to press switch button
  sw_value = switchWayCache["Way_" + switchNumber];
  console.log(sw_value);
  fctSetSwitchValue(this.id, is_persist);
  setTimeout(fctGetSwitchValue, 400, this.id, is_persist);

  // get information about binomial switch
  if(isBistableSwitch(this.id)) {
    setTimeout(fctGetSwitchValue, 800, idBinomialSwitch, is_persist);
  }

  // colorize the way in function of switchs
  setTimeout(drawWayTracking, 950);
}

function drawWayTracking() {
  var canvas = document.getElementById('wayTracking');
  if (!canvas) return;

  var context = canvas.getContext('2d');
  var canvasW = canvas.width;
  var canvasH = canvas.height;
  var centerX = canvas.width / 2;
  var centerY = canvas.height / 2;
  var radius = 30;

  context.lineWidth = 2;

  // exterior rail hight
  context.beginPath();
  context.moveTo(80, 10);
  context.lineTo(100, 10);
  context.strokeStyle = 'black';
  context.stroke();

  context.beginPath();
  context.moveTo(100, 10);
  context.lineTo(canvasW - 160, 10);
  context.strokeStyle = (switchWayCache["Way_4"] == 1) ? 'black' : 'grey';
  context.stroke();

  // exterior right rail hight curve
  context.beginPath();
  context.arc(canvasW - 130, 80, 70, 1.50 * Math.PI, 0.00 * Math.PI, false);
  context.strokeStyle = 'black';
  context.stroke();
  context.beginPath();
  context.moveTo(canvasW - 160, 10);
  context.lineTo(canvasW - 130, 10);
  context.strokeStyle = 'black';
  context.stroke();

  // interior left rail hight curve
  context.beginPath();
  context.arc(100, 20, 10, 1.50 * Math.PI, 1.80 * Math.PI, false);
  context.arc(125, 20, 10, 0.80 * Math.PI, 0.50 * Math.PI, true);
  context.strokeStyle = (switchWayCache["Way_5"] == 1) ? 'black' : 'grey';
  context.stroke();

  // interior rail hight
  context.beginPath();
  context.moveTo(124, 30);
  context.lineTo(canvasW - 185, 30);
  context.strokeStyle = (switchWayCache["Way_5"] == 1) ? 'black' : 'grey';
  context.stroke();

  context.beginPath();
  context.moveTo(145, 30);
  context.lineTo(255, 30);
  context.strokeStyle = (switchWayCache["Way_19"] != 1) ? 'red' : (switchWayCache["Way_5"] == 1) ? 'black' : 'grey';
  context.stroke();

  // interior right rail down curve
  context.beginPath();
  context.arc(canvasW - 185, 20, 10, 0.50 * Math.PI, 0.20 * Math.PI, true);
  context.arc(canvasW - 160, 20, 10, 1.20 * Math.PI, 1.50 * Math.PI, false);
  context.strokeStyle = (switchWayCache["Way_5"] == 1) ? 'black' : 'grey';
  context.stroke();

  // park left rail hight curve
  context.beginPath();
  context.arc(250, 45, 15, 0.50 * Math.PI, 0.20 * Math.PI, true);
  context.lineTo(279, 35);
  context.strokeStyle = (switchWayCache["Way_11"] == 1) ? 'black' : 'grey';
  context.stroke();
  context.beginPath();
  context.arc(290, 45, 15, 1.20 * Math.PI, 1.50 * Math.PI, false);
  context.strokeStyle = (switchWayCache["Way_9"] == 1) ? 'black' : 'grey';
  context.stroke();

  // rail park left hight
  context.beginPath();
  context.moveTo(80, 60);
  context.lineTo(220, 60);
  context.strokeStyle = 'black';
  context.stroke();

  context.beginPath();
  context.moveTo(80, 60);
  context.lineTo(200, 60);
  context.strokeStyle = (switchWayCache["Way_16"] != 1) ? 'red' : 'black';
  context.stroke();

  context.beginPath();
  context.moveTo(220, 60);
  context.lineTo(250, 60);
  context.strokeStyle = (switchWayCache["Way_12"] == 1) ? 'black' : 'grey';;
  context.stroke();

  // park left rail hight curve
  context.beginPath();
  context.arc(220, 70, 10, 1.50 * Math.PI, 1.80 * Math.PI, false);
  context.arc(270, 20, 60, 0.70 * Math.PI, 0.50 * Math.PI, true);
  context.strokeStyle = (switchWayCache["Way_13"] == 1) ? 'black' : 'grey';
  context.stroke();

  // rail park right down
  context.beginPath();
  context.moveTo(270, 80);
  context.lineTo(canvasW - 120, 80);
  context.strokeStyle = (switchWayCache["Way_13"] == 1) ? 'black' : 'grey';
  context.stroke();

  context.beginPath();
  context.moveTo(290, 80);
  context.lineTo(canvasW - 120, 80);
  context.strokeStyle = (switchWayCache["Way_18"] != 1) ? 'red' : (switchWayCache["Way_13"] == 1) ? 'black' : 'grey';
  context.stroke();

  // rail park right selector
  context.beginPath();
  context.moveTo(260, 60);
  context.lineTo(300, 60);
  context.strokeStyle = (switchWayCache["Way_10"] == 1) ? 'black' : 'grey';
  context.stroke();

  // rail park right
  context.beginPath();
  context.moveTo(300, 60);
  context.lineTo(canvasW - 120, 60);
  context.strokeStyle = (switchWayCache["Way_10"] == 1) ? 'black' : 'grey';
  context.stroke();

  context.beginPath();
  context.moveTo(290, 60);
  context.lineTo(canvasW - 120, 60);
  context.strokeStyle = (switchWayCache["Way_17"] != 1) ? 'red' : (switchWayCache["Way_10"] == 1) ? 'black' : 'grey';
  context.stroke();

  // interior left rail down curve
  context.beginPath();
  context.arc(110, canvasH - 45, 15, 0.50 * Math.PI, 0.20 * Math.PI, true);
  context.arc(150, canvasH - 45, 15, 1.20 * Math.PI, 1.50 * Math.PI, false);
  context.strokeStyle = (switchWayCache["Way_1"] == 1 && switchWayCache["Way_3"] == 1) ? 'black' : 'grey';
  context.stroke();

  // interior rail down
  context.beginPath();
  context.moveTo(149, canvasH - 60);
  context.lineTo(canvasW - 200, canvasH - 60);
  context.strokeStyle = (switchWayCache["Way_1"] == 1 && switchWayCache["Way_3"] == 1) ? 'black' : 'grey';
  context.stroke();

  // interior right rail down curve
  context.beginPath();
  context.arc(canvasW - 200, canvasH - 45, 15, 1.50 * Math.PI, 1.80 * Math.PI, false);
  context.arc(canvasW - 160, canvasH - 45, 15, 0.80 * Math.PI, 0.50 * Math.PI, true);
  context.strokeStyle = (switchWayCache["Way_1"] == 1 && switchWayCache["Way_3"] == 1) ? 'black' : 'grey';
  context.stroke();

  // medium left rail down curve
  context.beginPath();
  context.arc(85, canvasH - 105, 75, 0.5 * Math.PI, Math.PI);
  context.strokeStyle = (switchWayCache["Way_1"] == 1) ? 'black' : 'grey';
  context.stroke();

  // medium rail down
  context.beginPath();
  context.moveTo(80, canvasH - 30);
  context.lineTo(114, canvasH - 30);
  context.strokeStyle = (switchWayCache["Way_1"] == 1) ? 'black' : 'grey';
  context.stroke();
  context.beginPath();
  context.moveTo(114, canvasH - 30);
  context.lineTo(canvasW - 150, canvasH - 30);
  context.strokeStyle = (switchWayCache["Way_1"] == 1 && switchWayCache["Way_2"] == 1) ? 'black' : 'grey';
  context.stroke();
  context.beginPath();
  context.moveTo(canvasW - 165, canvasH - 30);
  context.lineTo(canvasW - 134, canvasH - 30);
  context.strokeStyle = (switchWayCache["Way_1"] == 1) ? 'black' : 'grey';
  context.stroke();

  // medium right rail down curve
  context.beginPath();
  context.arc(canvasW - 135, canvasH - 105, 75, 0, 0.5 * Math.PI);
  context.strokeStyle = (switchWayCache["Way_1"] == 1) ? 'black' : 'grey';
  context.stroke();

  // exterior left rail hight curve
  context.beginPath();
  //context.moveTo(10, 80);
  context.arc(80, 80, 70, Math.PI, 1.5 * Math.PI);
  context.strokeStyle = 'black';
  context.stroke();


  // exterior left rail down curve
  context.beginPath();
  context.moveTo(10, canvasH - 100);
  context.arcTo(10, canvasH - 10, canvasW - 130, canvasH - 10, 70);
  context.strokeStyle = (switchWayCache["Way_0"] == 1) ? 'black' : 'grey';
  context.stroke();

  // exterior rail down
  context.beginPath();
  context.moveTo(80, canvas.height - 10);
  context.lineTo(canvasW - 130, canvasH - 10);
  context.strokeStyle = (switchWayCache["Way_0"] == 1) ? 'black' : 'grey';
  context.stroke();

  // exterior right rail down curve
  context.beginPath();
  context.moveTo(canvasW - 60, canvasH - 100);
  context.arcTo(canvasW - 60, canvasH - 10, canvasW - 130, canvasH - 10, 70);
  context.strokeStyle = (switchWayCache["Way_0"] == 1) ? 'black' : 'grey';
  context.stroke();

  //context.clear();
}

function createWithConfiguration() {
  if(!document.configuration) return;

  var divDashboardCommand = document.getElementById('dashboardCommand');
  if (!divDashboardCommand) return;

  for (objectConfig in document.configuration) {
    var divObj = document.createElement('div');
    divObj.id = objectConfig;
    divObj.className = document.configuration[objectConfig].type;
    var divTitle = document.createElement('div');
    divTitle.innerHTML = document.configuration[objectConfig].title;
    divObj.appendChild(divTitle);
    divDashboardCommand.appendChild(divObj);
  }

}

// ----- Main Init -----
function initApplication() {
  drawWayTracking();
  createWithConfiguration();
  createSwitchBlockCommand();
  createSwitchElements();
  console.log("initializing done");
}