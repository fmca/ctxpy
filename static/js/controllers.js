ifctt.controller('ContextCtrl', function($scope, $rootScope, $http, contextIngredients, actionIngredients) {

  $scope.context = {}
  $scope.action = {}
  $scope.context.recipe = [{type: "placeholder"}];
  $scope.action.recipe = [{type: "placeholder"}];
  
  $scope.modal = {}
  $scope.modal.item = {}
  $scope.current = {};
  $scope.current.ingredients = [];

  $scope.current.recipe = [{type: "placeholder"}];
  
  $scope.toggle = function(type){
	  if(type == 'context'){
		  $scope.action.recipe = $scope.current.recipe;
		  $scope.current.ingredients = contextIngredients;
		  $scope.current.recipe = $scope.context.recipe;
	  }else if(type == 'action'){
		  $scope.context.recipe = $scope.current.recipe;
		  $scope.current.ingredients = actionIngredients;
		  $scope.current.recipe = $scope.action.recipe;
	  }else{
		  console.log("checfoi foi nada");
	  }
  }
  
  $scope.toggle('context');

  $scope.sortableOptions = {
    allowDuplicates: false,
    containment: '#sortable-container',
    containerPositioning: 'relative',
    orderChanged: function(obj) {
      $scope.reorganize();
    }
  };
  $scope.sortableCloneOptions = {
    containment: '#sortable-container',
    containerPositioning: 'relative',
    clone: true,
    itemMoved: function(obj) {
      $scope.reorganize();
    }
  };

  $scope.reorganize = function() {
    var copy = $scope.current.recipe;
    var newList = [];
    for (var i in copy) {
      var it = copy[i];
      if (it.type != 'placeholder') {
        newList.push(it);
        newList.push({
          type: "placeholder"
        })
      }
    }
    if (newList.length == 0) newList.push({
      type: "placeholder"
    });
    $scope.current.recipe = newList;
  }


  $scope.deleteItem = function(index) {
    $scope.lists.recipe.splice(index, 1);
    $scope.reorganize();
  }
  
  
  $scope.save = function(){
	$http.post('/recipe', {"recipe": $scope.context.recipe}).then(function(){console.log("success")}, function(){console.log("error")});
  }

})