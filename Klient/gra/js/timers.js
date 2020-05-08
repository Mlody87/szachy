class Timers {
	
	constructor (gameidp, timew, timeb) {
		this.gameid = gameidp;
		this.WhiteSeconds = timew;
		this.BlackSeconds = timeb;
	}		
	
	getWhiteTime() {
		return this.WhiteSeconds;
	}
	
	getBlackTime() {
		return this.BlackSeconds;
	}
	
	setWhiteTime() {
		document.getElementById('white').innerHTML = this.WhiteSeconds;
	}
	
	setBlackTime() {
		document.getElementById('black').innerHTML = this.BlackSeconds;		
	}
	
	startWhiteTimer() { 
		this.WhiteTime = setInterval(startWhite ,1000);
		this.WhiteSeconds = document.getElementById('white').innerHTML;
	}

	resumeWhiteTimer() {    
		this.WhiteTime = setInterval(startWhite ,1000);
	}

	startWhite() {
		this.WhiteSeconds--;
		document.getElementById('white').innerHTML = this.WhiteSeconds;
	}

	stopWhiteTimer() {
		clearInterval(WhiteTime)
	}

	startBlackTimer() { 
		this.BlackTime = setInterval(startBlack ,1000);
		this.BlackSeconds = document.getElementById('black').innerHTML;
	}

	resumeBlackTimer() {    
		this.BlackTime = setInterval(startBlack ,1000);
	}

	startBlack() {
		this.BlackSeconds--;
		document.getElementById('black').innerHTML = this.BlackSeconds;
	}

	stopBlackTimer() {
		clearInterval(BlackTime)
	}
	
	

}	