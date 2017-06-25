/*********************
 * Gestion Patienter *
 * Pierre Contri     *
 * le 14/12/2007     *
 *********************/

var ie = (document.all) ? 1 : 0;
var isIE6 = navigator.appVersion.indexOf("MSIE 6") > 0;
var p = (ie) ? "filter" : "MozOpacity";
var bAffichagePatienter = false;

//setTimeout('testAffichageDivPatienter()',2000);

function patiente()
{
  affichePatienter();
/*
// code wrote in 2003
// stop to run in 2012
// for new generation of navigator (smartphone, ...) it is so complex
  var divp = document.getElementById('divPatienter');
  if (divp != null) op(divp, 0);
  progressOpacity('divPatienter', 50, 0, 70);
*/
}

function progressOpacity(elementDivName, tpsTimeout, opacityStart, opacityEnd)
{
  var elementDiv = document.getElementById(elementDivName);
  if(elementDiv == null) return false;
  var testEnd = (ie) ? "alpha(opacity="+opacityEnd+")" : opacityEnd/100;
  if (elementDiv.style[p] < testEnd)
  {
    op(elementDiv,opacityStart);
    setTimeout("progressOpacity('" + elementDivName + "', " + tpsTimeout + ", " + eval(opacityStart + 5) + ", " + opacityEnd + ")", tpsTimeout);
  }
}

function op(n,v)
{
  v = (ie) ? "alpha(opacity=" + v + ")" : v / 100;
  n.style[p] = v;
}

function testAffichageDivPatienter()
{
  if (bAffichagePatienter)
     cachePatienter();
  setTimeout('testAffichageDivPatienter()', 2000);
}

function cachePatienter()
{
  var divpatientez = document.getElementById('divPatienter');
  if (divpatientez != null)
  {
    divpatientez.style.visibility = 'hidden';
    divpatientez.style.display = 'none';
    bAffichagePatienter = false;
  }
}

function affichePatienter()
{
  var divpatientez = document.getElementById('divPatienter');
  if (divpatientez == null)
	divpatientez = createPatienter();
  
  divpatientez.style.visibility = 'visible';
  divpatientez.style.display = 'block';
  bAffichagePatienter = true;
}

function createPatienter()
{
  var divpatientez = document.createElement('divPatienter');
  divpatientez.setAttribute("id", "divPatienter");
  divpatientez.setAttribute("name", "divPatienter");
  var contentPatienter = "<div id=\"divPatienterIntern\"><img src=\"./src/images/wait.gif\" alt=\"Please, wait ...\"/></div>";
  divpatientez.innerHTML = contentPatienter;
  document.body.appendChild(divpatientez);
  return divpatientez;
}