function menu() {
	
	if (localStorage.menu) {
		
		if(localStorage.menu == "big")
		{
			var men = document.getElementById("menu");
			men.classList.add("hide-menu");
			var content = document.getElementById("content");
			content.classList.add("change-margin");
			var content = document.getElementById("logo");
			content.classList.add("change-width");
			var profile = document.getElementById("profile");
			profile.classList.add("hide");
			var smallhide1 = document.getElementById("smallhide1");
			smallhide1.classList.add("hide");
			var smallhide2 = document.getElementById("smallhide2");
			smallhide2.classList.add("hide");
			var smallhide3 = document.getElementById("smallhide3");
			smallhide3.classList.add("hide");
			var smallhide4 = document.getElementById("smallhide4");
			smallhide4.classList.add("hide");
			var smallhide5 = document.getElementById("smallhide5");
			smallhide5.classList.add("hide");
			
			var logo1 = document.getElementById("logo1");
			logo1.classList.add("hide");
			var logo2 = document.getElementById("logo2");
			logo2.classList.remove("hide");
			
			
			localStorage.setItem("menu", "small");
		}
		else
		{
			var men = document.getElementById("menu");
			men.classList.remove("hide-menu");
			var content = document.getElementById("content");
			content.classList.remove("change-margin");
			var content = document.getElementById("logo");
			content.classList.remove("change-width");
			var profile = document.getElementById("profile");
			profile.classList.remove("hide");
			var smallhide1 = document.getElementById("smallhide1");
			smallhide1.classList.remove("hide");
			var smallhide2 = document.getElementById("smallhide2");
			smallhide2.classList.remove("hide");
			var smallhide3 = document.getElementById("smallhide3");
			smallhide3.classList.remove("hide");
			var smallhide4 = document.getElementById("smallhide4");
			smallhide4.classList.remove("hide");
			var smallhide5 = document.getElementById("smallhide5");
			smallhide5.classList.remove("hide");
			
			var logo1 = document.getElementById("logo1");
			logo1.classList.remove("hide");
			var logo2 = document.getElementById("logo2");
			logo2.classList.add("hide");
			
			localStorage.setItem("menu", "big");
		}
	
	
	}
	else
	{
		var men = document.getElementById("menu");
		men.classList.add("hide-menu");
		var content = document.getElementById("content");
		content.classList.add("change-margin");
		var content = document.getElementById("logo");
		content.classList.add("change-width");
		var profile = document.getElementById("profile");
		profile.classList.add("hide");
		var smallhide1 = document.getElementById("smallhide1");
		smallhide1.classList.add("hide");
		var smallhide2 = document.getElementById("smallhide2");
		smallhide2.classList.add("hide");
		var smallhide3 = document.getElementById("smallhide3");
		smallhide3.classList.add("hide");
		var smallhide4 = document.getElementById("smallhide4");
		smallhide4.classList.add("hide");
		var smallhide5 = document.getElementById("smallhide5");
		smallhide5.classList.add("hide");
		
		var logo1 = document.getElementById("logo1");
		logo1.classList.add("hide");
		var logo2 = document.getElementById("logo2");
		logo2.classList.remove("hide");
		
		localStorage.setItem("menu", "small");
	}
	
	
} 