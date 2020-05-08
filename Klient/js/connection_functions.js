var adr;
var ws;
var connectionId;

function establish_connection()
{
	
	if(localStorage.getItem('connectionId') != null)
	{
		connectionId = localStorage.getItem('connectionId');
	}
	else
	{
		connectionId=0;
	}
	
	adr = "ws://127.0.0.1:8888/connection/"+connectionId;
	ws = new WebSocket(adr);
	
}

function sendPong()
{
	ws.send(JSON.stringify({
			'connectionId':connectionId,
			'type':'pong',
			}));			
}


function connected(id) {
	
	if(connectionId != id) {
		localStorage.setItem('connectionId', id);
		connectionId = id;
	}		
}