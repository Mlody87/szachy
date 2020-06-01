<html>

<?php
	$link = $_GET['a'];

	switch (true){
		case stristr($link,'register'):
			$incl = 'register/index.html';
			$title = "Zarejestruj się";
			break;
		case stristr($link,'login'):
			$incl = 'login.html';
			$title = "Zaloguj się";
			break;
		default:
			$incl = 'main.html';
			$title = 'Witaj na Chess Stars!';
			break;
}
?>

<head>
	<!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> -->
	
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.0-2/css/all.min.css">

	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<link rel="stylesheet" href="style.css">
	<script src="menu.js"></script> 
	<script type="text/javascript" src="/js/connection_functions.js"></script>
</head>

<body>

<div class="top-header">

	<div class="top-container">

		<div id="logo" class="logo">
			<img id="logo1" src="logo.png" class="logo-image">
			<img id="logo2" src="logo2.png" class="logo-small hide">
		</div>
		<div class="top-menu">
		<div class="menu-icon"onclick="menu();">
			<i class="fa fa-bars fa-lg icon" style="opacity: 0.7;"></i>
		</div>
		<div class="top-icons">
			<!--
			<i class="far fa-bell fa-md"></i>
			<i class="far fa-envelope fa-md"></i>
			<i class="fas fa-sign-out-alt fa-md"></i>
			
			<img class="avatar smaller" src="https://www.w3schools.com/howto/img_avatar.png"> Paweł <i class="fa fa-angle-down"></i>
			-->
			<a href="/layout/?a=register"><div class="btn red"><strong>Zarejestruj</strong></div></a>
			<div class="btn green"><strong>Logowanie</strong></div>
			
		</div>
		</div>

	</div>

</div>

<div class="container">

	<div class="page-container">
		<div class="menu">
			
			<div id="menu" class="menu-container">
			
				<div id="profile" class="profile-container">
				<div class="row">
					<img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png">
				</div>
				<!-- <div class="row profile-username bold">
					Paweł Kabat
				</div>
				<div class="row profile-username">
					Mlody87
				</div>
				<div class="row">
					<div class="profile-icons">
						<i class="material-icons icon-size">person</i>
						<i class="material-icons icon-size">chat</i>
						<i class="material-icons icon-size">input</i>
					</div>
				</div>
				-->
				<div class="row">
					<div class="btn red"><strong>Zarejestruj</strong></div>
					<div class="btn green"><strong>Logowanie</strong></div>
				</div>
				<hr class="line">
				</div>
			
				<div class="menu-option" style="--color:cyan;"><div class="iconcol"><i class="far fa-newspaper fa-lg"></i></div><div id="smallhide1" class="col">Aktualności</div></div>
				<div class="menu-option" style="--color:red;"><div class="iconcol"><i class="fas fa-chess fa-lg"></i></div><div id="smallhide2" class="col">Zagraj</div></div>
				<div class="menu-option" style="--color:yellow;"><div class="iconcol"><i class="fas fa-chess-board fa-lg"></i></div><div id="smallhide3" class="col">Turnieje</div></div>
				<div class="menu-option" style="--color:green;"><div class="iconcol"><i class="fas fa-graduation-cap fa-lg"></i></div><div id="smallhide4" class="col">Nauka i analiza</div></div>
				<div class="menu-option" style="--color:coral;"><div class="iconcol"><i class="fas fa-user-friends fa-lg"></i></div><div id="smallhide5" class="col">Społeczność</div></div>
			
			</div>
			
		</div>
		
		<div class="content-container">
		
		
			<div id="content" class="content">
			
				<div class="content-card-full">
				
					<div class="card-header">
						<?php print $title; ?>
					</div>
					<div class="card-content">
					
					<?php include($incl); ?>
					
					</div>
				</div>
			
			</div>
		
		</div>
	
	
	</div>

</div>


</body>


</html>
