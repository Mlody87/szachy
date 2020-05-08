
CLOCKS_MODULE = (function () {
var _WhiteSeconds=0;
var _BlackSeconds=0;
var _timerinterval = 100;
var _timerexpected;
var _whiteactive = false;
var _blackactive = false;
var _WhiteCallback;

var _setWhiteCallback = function(call) {
	_WhiteCallback = call;
}

var _setWhiteTime = function(t) {
	_WhiteSeconds = t;
}

var _startWhiteTimer = function() {
	_whiteactive = true;
    _timerexpected = Date.now() + _timerinterval;
    _WhiteTime = setTimeout(_startWhite, _timerinterval);  
}

var _startWhite = function() {
	if(!_whiteactive){ return; }
//var countstart = Date.now();
var _dt = Date.now() - _timerexpected; // the drift (positive for overshooting)
    if (_dt > _timerinterval) {
		//zminimalizowana przegladarka
		//nie liczymy
	}
	else
	{

    _WhiteSeconds = _WhiteSeconds-0.1;

	if(_WhiteSeconds<=0)
	{
		_WhiteSeconds = 0.0;
	}
	
	var _timestr = _WhiteSeconds.toFixed(1)
    
	//document.getElementById("white").innerHTML = timestr;
	
	_WhiteCallback(_timestr);	

	//var countstop = Date.now();
	//var delay = countstop - countstart;
	
	
	}
	_timerexpected += _timerinterval;
	
	
	setTimeout(_startWhite, Math.max(0, _timerinterval - _dt));

} 

var _stopWhiteTime = function() {
    _whiteactive = false;
}

var _getWhiteTime = function() {
	var tmp = parseFloat(_WhiteSeconds);
	var _timestr = tmp.toFixed(1);
	return _timestr;
}

var _setBlackCallback = function(call) {
	_BlackCallback = call;
}

var _setBlackTime = function(t) {
	_BlackSeconds = t;
}

var _startBlackTimer = function() {
	_blackactive = true;
    _timerexpected = Date.now() + _timerinterval;
    _BlackTime = setTimeout(_startBlack, _timerinterval);  
}

var _startBlack = function() {
	if(!_blackactive){ return; }
//var countstart = Date.now();
var _dt = Date.now() - _timerexpected; // the drift (positive for overshooting)
    if (_dt > _timerinterval) {
		//zminimalizowana przegladarka
		//nic nie liczymy
	}
	else{

    _BlackSeconds = _BlackSeconds-0.1;

	if(_BlackSeconds<=0)
	{
		_BlackSeconds = 0.0;
	}
	
	var _timestr = _BlackSeconds.toFixed(1)
	
	
	_BlackCallback(_timestr);
	//var countstop = Date.now();
	//var delay = countstop - countstart;
	
	}
	
	_timerexpected += _timerinterval;
	

	
	setTimeout(_startBlack, Math.max(0, _timerinterval - _dt));

} 

var _stopBlackTime = function() {
    _blackactive = false;
}

var _getBlackTime = function() {
	var tmp = parseFloat(_BlackSeconds);
	var _timestr = tmp.toFixed(1);
	return _timestr;
}

 
 return {
   startWhiteTimer: _startWhiteTimer,
   startWhite: _startWhite,
   setWhiteTime: _setWhiteTime,
   stopWhiteTimer: _stopWhiteTime,
   setWhiteCallback: _setWhiteCallback,
   startBlackTimer: _startBlackTimer,
   startBlack: _startBlack,
   setBlackTime: _setBlackTime,
   stopBlackTimer: _stopBlackTime,
   setBlackCallback: _setBlackCallback,
   getWhiteTime: _getWhiteTime,
   getBlackTime: _getBlackTime
  };
})();
