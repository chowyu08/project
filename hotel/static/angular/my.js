var My = (function(){
		var app = angular.module('myApp', []);
		data = [{
				"Name" : "Alfreds Futterkiste",
				"City" : "Berlin",
				"Country" : "Germany"
				},
				{
				"Name" : "Berglunds snabbköp",
				"City" : "Luleå",
				"Country" : "Sweden"
				},
				{
				"Name" : "Centro comercial Moctezuma",
				"City" : "México D.F.",
				"Country" : "Mexico"
				},
				{
				"Name" : "Ernst Handel",
				"City" : "Graz",
				"Country" : "Austria"
				},
				{
				"Name" : "FISSA Fabrica Inter. Salchichas S.A.",
				"City" : "Madrid",
				"Country" : "Spain"
		}];
		app.controller('myCtrl', function($scope) {
		    //alert(response.records);
		    $scope.names = data;
		});
})();