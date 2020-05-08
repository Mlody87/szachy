
BOARD_MODULE = (function () {
var board = null
var game = new Chess()
var whiteSquareGrey = '#a9a9a9'
var blackSquareGrey = '#696969'
var whiteSquare = '#9E7863'
var blackSquare = '#633526'
var _promote;
var boardID;
var movecolor = '';
var mycolor = 'red'; 
var sendMoveCallback;
var PromoCallback;
var orientation = 'white';
var historyHandler;

var createBoard = function() {
	board = ChessBoard(boardID, config);
}

var setHistory = function(his) { 
	historyHandler = his;
}

var setBoardID = function(id) {
	boardID = id;
}

var setMoveColor = function(color) {
	movecolor = color;
}

var setMyColor = function(color) {
	mycolor = color;
}

var getMyColor = function() {
	return mycolor;
}

var getMoveColor = function()
{
	return movecolor;
}

var setSendMoveCallback = function(call) {
	sendMoveCallback = call;
}

var setPromoCallback = function(call) {
	PromoCallback = call;
}

var setHistoryFen = function(fen) {
	config["position"] = fen;
	config["draggable"] = false;
	board = ChessBoard(boardID, config);	
}

var setFenPossition = function(fen) {
	//console.log(game.validate_fen(obj['fenposition']))
	if(game.load(fen)) {console.log("zaladowano do silnika");
	config["position"] = fen;
					
	board = ChessBoard(boardID, config);
	}	
}

var promote_piece = async function(source, target, piece) {
	var type;
	PromoCallback(mycolor);
	show_mpw(); /* show modal promotion window */
	var promise = new Promise((resolve) => { _promote = resolve });
	await promise.then((result) => { type = result });
	if (type === undefined) type = "Q";
	hide_mpw();
	MoveAfterDrop(source, target, piece, type)
	
	board.position(game.fen(), false);	

}

var reload = function() {
	board = ChessBoard(boardID, config);
}

var doMove = function(from, to, promotion) {
			
	var move = game.move({
		from: from,
		to: to,
		promotion: promotion 
	})
	
	//var move = from + "-" + to + promotion;
	//board.move(move);
					
	var pos = game.fen();
	config["position"] = pos;
	config["orientation"] = orientation;
					
	board = ChessBoard(boardID, config);
			
	if(movecolor=="white"){movecolor="black"; game.setTurn("b");}else{movecolor="white"; game.setTurn("w");}
	
	if(historyHandler) {
		historyHandler.addMove(from, to, promotion);
	}
	
}

var draggable = function(drag) {
		config["draggable"] = drag;
}

var changeOrientation = function(color='') {
	if(color!='') {
		orientation = color;
	}
	else
	{	
	
		if(orientation=='white'){
			orientation = 'black';
		}
		else
		{
			orientation = 'white';
		}
	}
	config["orientation"] = orientation;
	board = ChessBoard(boardID, config);
}

var show_mpw = function()
{
	document.getElementById("promotiontop").style.display = 'block';
}

var hide_mpw = function()
{
	document.getElementById("promotiontop").style.display = 'none';
}

var removeGreySquares = function() {
	
	/* var b = '#'+boardID;
	//$('#myBoard .square-55d63').css('background', '')
	  $(b+' .square-55d63').css('background', '')  */
	  
	var b = '#'+boardID;
	
	$(b+' .white-1e1d7').css('background-color', whiteSquare)
	$(b+' .black-3c85d').css('background-color', blackSquare)	
}

var greySquare = function(square) {
	var b = '#'+boardID;
	var $square = $(b+' .square-' + square)

	var background = whiteSquareGrey
	if ($square.hasClass('black-3c85d')) {
    background = blackSquareGrey
	}

	$square.css('background-color', background)
}

var MoveAfterDrop = function(source, target, piece, promotion)
{
var move = game.move({
    from: source,
    to: target,
    promotion: promotion // NOTE: always promote to a queen for example simplicity
  })

	// illegal move
	if (move === null) return 'snapback'
  

  
	sendMoveCallback(source, target, piece, promotion);
  
}


var onDragStart = function(source, piece) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  // or if it's not that side's turn
  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false
  }

  // get list of possible moves for this square
  var moves = game.moves({
    square: source,
    verbose: true
  })

  // exit if there are no moves available for this square
  if (moves.length === 0) return

  // highlight the square they moused over
   greySquare(source)

  // highlight the possible squares for this piece
  for (var i = 0; i < moves.length; i++) {
    greySquare(moves[i].to)
  } 

}

var onDrop = function(source, target, piece) {
  removeGreySquares()

    var source_rank = source.substring(2,1);
    var target_rank = target.substring(2,1);
    var piece = game.get(source).type;

          // check we are not trying to make an illegal pawn move to the 8th or 1st rank,
          // so the promotion dialog doesn't pop up unnecessarily
          // e.g. (p)d7-f8
          var move = game.move({
		    from: source,
            to: target,
            promotion: 'q'
		  });
          // illegal move
          if (move === null) {
            return 'snapback';
          } else {
            game.undo(); //move is ok, now we can go ahead and check for promotion
          }
	

          if (piece === 'p' &&
             ((source_rank === '7' && target_rank === '8') || (source_rank === '2' && target_rank === '1'))) {
               
			 
			
			promote_piece(source, target, piece);
			return;
			
			 
			}
			else
			{
				MoveAfterDrop(source, target, piece, '');
			}
  
}


var onMouseoutSquare = function(square, piece) {
  removeGreySquares()
}

var onMouseoverSquare = function(square, piece) {

}

var onSnapEnd = function() {
  board.position(game.fen())
}

var setPromote = function(promo) {
	_promote(promo);
}




var config = {
  pieceTheme: chess24_piece_theme,
  boardTheme: chess24_board_theme,
  orientation: 'white',
  draggable: false,
  appearSpeed: 0,
  moveSpeed: 0,
  snapbackSpeed: 0,
  snapSpeed: 0,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onMouseoverSquare: onMouseoverSquare,
  onMouseoutSquare: onMouseoutSquare,
  onSnapEnd: onSnapEnd
}
 
 return {
	createBoard: createBoard,
	setBoardID: setBoardID,
	changeOrientation: changeOrientation,
	setMoveColor: setMoveColor,
	setMyColor: setMyColor,
	getMyColor: getMyColor,
	getMoveColor: getMoveColor,
	doMove: doMove,
	draggable: draggable,
	setSendMoveCallback: setSendMoveCallback,
	setFenPossition: setFenPossition,
	setPromote: setPromote,
	setPromoCallback: setPromoCallback,
	reload:reload,
	setHistory: setHistory,
	setHistoryFen:setHistoryFen
  };
})();
