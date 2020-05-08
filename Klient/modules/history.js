 HISTORY_MODULE = (function () {
 var boardID;
 var historyID;
 var gameHistory = {};
 var movesNr = 0;
 var moveCursor = 0;
 var game = new Chess()
 var variableName;
 var boardHandler;
 var whiteCell = 'white';
 var blackCell = '#F0F8FF';
 var cell = 'black';
 
 var setBoardID = function(id) {
	boardID = id;	
}

var setBoard = function(b) {
	boardHandler = b;
}

 var setHistoryID = function(id) {
	historyID = id;
	
	var move = new Object();
	move.pos = game.fen();
	gameHistory[0] = move;
}

var setVariableName = function(name) {
	variableName = name; //gowno straszne ale potrzebne do zbudowanie onclick dynamicznie
}

var showHistory = function() {
	var node= document.getElementById(historyID);
	while (node.firstChild) {    
	node.removeChild(node.firstChild);
	}
	
	cell = 'black';
	
	for (key in gameHistory) {
		if(key != 0)
		{
			addCell(key, gameHistory[key].from, gameHistory[key].to, gameHistory[key].promotion);
		}
	}
	
	
}

var loadHistory = function(data) {
	
	if(!data.hasOwnProperty('history')) { return; }
	
	gameHistory = {}
	
	var countKeys = Object.keys(data.history).length;
	movesNr = countKeys;
	
	var move = new Object();
	move.pos = game.fen();
	
	gameHistory[0] = move;

	
	for (var key in data.history){
	var obj = data.history[key];
	
	console.log(obj);
    
		var m = game.move({
		from: obj.from,
		to: obj.to,
		promotion: obj.promotion 
	})
	
		var pos = game.fen();
	
		var move = new Object();
		move.from = obj.from;
		move.to = obj.to;
		move.promotion = obj.promotion;
		move.pos = pos;
		
		gameHistory[parseInt(key)] = move;
	
	}
	
	
	console.log(gameHistory);
	
	showHistory();
	
}

var addCell = function(key, from, to, promotion) {
	var historyDiv = document.getElementById(historyID);
	
	if(cell=='white')
	{
		background=blackCell;
		cell='black';
	}
	else
	{
		background=whiteCell;
		cell='white';
	}
	
	var newDiv = document.createElement('div');
	newDiv.className = "gamehistorycell";
	newDiv.id="move"+key;
	newDiv.style="background-color:"+background+";";
	var tmp = variableName;
	tmp += ".fromMove("+key+");";
	newDiv.setAttribute("onclick", tmp);	
	newDiv.innerHTML = from+"-"+to+" "+promotion;
	
	historyDiv.appendChild(newDiv);
	historyDiv.scrollTop = historyDiv.scrollHeight;
}

var addMove = function(from, to, promotion) {
	var move = new Object();
	move.from = from;
	move.to = to;
	move.promotion = promotion;
	
	movesNr += 1;
	
	var m = game.move({
		from: from,
		to: to,
		promotion: promotion 
	})
					
	var pos = game.fen();
	
	move.pos = pos;
	
	gameHistory[movesNr] = move;
	
	console.log(gameHistory[movesNr]);
	
	addCell(movesNr, from, to, promotion);
	
	if(moveCursor != movesNr-1) {
		showHistory();
	}
	
	moveCursor = movesNr;
	
 }

var nextMove = function() {
	fromMove(moveCursor+1);
}

var previousMove = function() {
	fromMove(moveCursor-1);
}

var live = function() {
	fromMove(movesNr);
}

var fromStart = function() {
	fromMove(0);
}

var fromMove = function(move) {
	if(!(move in gameHistory))
	{
		return;
	}
	
	var fen = gameHistory[move].pos;
	boardHandler.setHistoryFen(fen);
	
	if((boardHandler.getMyColor()==boardHandler.getMoveColor()) && (move == movesNr)) {
		boardHandler.draggable(true);
	}
	moveCursor = move;
}

var isOdd = function isOdd(num) {  //czy nieparzysta
	if(num % 2 == 1)
	{
		return true;
	}
	else
	{
		return false;
	}
}
 
 
 return {
	setBoardID: setBoardID,
	setHistoryID:setHistoryID,
	loadHistory: loadHistory,
	setHistoryID:setHistoryID,
	addMove:addMove,
	setVariableName:setVariableName,
	fromMove: fromMove,
	setBoard:setBoard,
	previousMove:previousMove,
	fromStart:fromStart,
	live:live,
	nextMove:nextMove
	
  };
})();
