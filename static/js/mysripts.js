function changeMode(id){
	if(document.getElementById(id).style.display == "none"){
		document.getElementById(id).style.display = "block"
	}else{
		document.getElementById(id).style.display = "none"
	}
}

angular.module("MyApp",[]).controller("RegCtrl", function($scope, $http, $location){
	//$scope.login_info = {};
	$scope.login_info = "";
	$scope.pass_info = ""; 
	var LoginVal = false;
	var PassVal = false;
	var CountryVal = false
	var CityVal = false


	$scope.LoginValid = function(){
		//$scope.login_info="writing";
		if($scope.login_value.length == 0){
			$scope.login_info = "empty field";
			$scope.changeLogin = {color: 'red'};
			LoginVal = false;
		}else{
			var url = "http://localhost:5000/login_validation/" + $scope.login_value;
		    console.log(url);
			$http.get(url).success(function(response){
				if(response.answer == 0){
					$scope.login_info = "OK";
					$scope.changeLogin = {color: 'green'};
					LoginVal = true;
				}else{
					$scope.login_info = "login already existed";
					$scope.changeLogin = {color: 'red'};
					LoginVal = false;
				}
			});
		}
	}

	$scope.PassValid = function(){
		if($scope.pass_value.length <= 5){
			$scope.pass_info = "short password";
			$scope.changePass = {color: 'red'};
			PassVal = false;
		}
		if(($scope.pass_value.length > 5) && ($scope.pass_value.length <= 8)){
			$scope.pass_info = "medium password";
			$scope.changePass = {color: 'orange'};
			PassVal = false;
		}
		if($scope.pass_value.length > 8){
			var regExp =  /\d/g;
			var res = $scope.pass_value.match(regExp);
			if(res == null){
				$scope.pass_info = "simple password";
				$scope.changePass = {color: 'red'};
				PassVal = false;			
			}else{
				if(res.length > 3){
					$scope.pass_info = "OK";
					$scope.changePass = {color: 'green'};
					PassVal = true;
				}
			}
		}
	}

	$scope.CountryTip = function(){

		if($scope.country_value.length == 0){
			$scope.country_info = "empty field";
			$scope.changeCountry = {color: 'red'};
			$scope.countryList = null;
			CountryVal = false;
		}else{
			var url = "http://localhost:5000/country_tip/" + $scope.country_value;
		    console.log(url);
			$http.get(url).success(function(response){
				
				console.log(response.c[0]);
				console.log(response.c[1]);
				console.log(response.c[2]);
				$scope.countryList = response.c;
				$scope.country_info = "OK";
				$scope.changeCountry = {color: 'green'};
				CountryVal = true;
			});
		}
	}

	$scope.CityTip = function(){

		if($scope.city_value.length == 0){
			$scope.city_info = "empty field";
			$scope.changeCity = {color: 'red'};
			$scope.cityList = null;
			CityVal = false;
		}else{
			var url = "http://localhost:5000/city_tip/" + $scope.city_value;
		    console.log(url);
			$http.get(url).success(function(response){
				
				$scope.cityList = response.c;
				$scope.city_info = "OK";
				$scope.changeCity = {color: 'green'};
				CityVal = true;
			});
		}
	}

	$scope.setValue = function(val){
		$scope.country_value = val;
		$scope.countryList = null;
	}

	$scope.setCityValue = function(val){
		console.log("city");
		$scope.city_value = val;
		$scope.cityList = null;
	}

	$scope.setRegData = function(){
		console.log("work");
		if((LoginVal == true) && (PassVal == true) && (CountryVal == true) && (CityVal) == true){
			var url = "http://localhost:5000/reg_worker";
		    console.log(url);
		    $scope.main_info = "";
		    var data = {    
                name: $scope.login_value,
                pass: $scope.pass_value,
                country : $scope.country_value,
                city: $scope.city_value
        	};
			$http.post(url,data).success(function(response){
				location.assign("http://localhost:5000/answer");
				//$location.path("/template/answer.html");
			}).error(function(response){
				location.assign("http://localhost:5000/error_reg");
			});

		}else{
			console.log("wrong fields");
			$scope.main_info = "Wrong fields";
			$scope.main_style = {color: 'red'};
		}
	}


});