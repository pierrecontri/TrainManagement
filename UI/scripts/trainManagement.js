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
  setTimeout(fctGetSwitchValue, 300, this.id);
}

// ----- Main Init -----
function initApplication() {
  createSwitchBlockCommand();
  createSwitchElements();
  initSwitchs();
  console.log("Application initializing done");
}