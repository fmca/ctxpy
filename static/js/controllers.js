ifctt.controller('NavCtrl', function($scope, $rootScope){
	$scope.menu = {
		current: 'home' //home, widgets, recipes
	}
	$rootScope.getMenu = function(){
		return $scope.menu.current;
	}
});
ifctt.controller('WidgetCtrl', function($scope, $rootScope, $http, $timeout){
	$scope.widgets = []	
	$scope.getWidgets = function(){
		$http.get('/widgets', {ignoreLoadingBar: true}).then(function(response){
			$scope.widgets = response.data;
			$timeout($scope.getWidgets, 1500);
		}, function(){});	
		
    };
	
	$scope.getWidgets();
});
ifctt.controller('RecipesCtrl', function($scope, $http, $timeout){
	$scope.recipes = []
	$scope.getRecipes = function(){
		$http.get('/recipe', {ignoreLoadingBar: true}).then(function(response){
			$scope.recipes = response.data;
			$timeout($scope.getRecipes, 1500);
		}, function(){});	
    };
	
	$scope.remove = function(title){
		$http.delete('/recipe/'+title).then(function(){});
	}
	$scope.getRecipes();
});
ifctt.controller('ContextCtrl', function($scope, $rootScope, $http, contextIngredients, actionIngredients) {

  $scope.init = function(){
	$scope.context = {}
    $scope.action = {}
    $scope.context.recipe = [{type: "placeholder"}];
    $scope.action.recipe = [{type: "placeholder"}];
  
    $scope.modal = {}
    $scope.modal.item = {}
    $scope.current = {};
    $scope.current.name = "Sem título";
    $scope.current.ingredients = [];

    $scope.current.recipe = [{type: "placeholder"}];
	$scope.toggle('context');
  }
  
  $scope.toggle = function(type){
	  $scope.current.type = type;
	  if(type == 'context'){
		  $scope.action.recipe = $scope.current.recipe;
		  $scope.current.ingredients = contextIngredients;
		  $scope.current.recipe = $scope.context.recipe;
	  }else if(type == 'action'){
		  $scope.context.recipe = $scope.current.recipe;
		  $scope.current.ingredients = actionIngredients;
		  $scope.current.recipe = $scope.action.recipe;
	  }
  }
  
  $scope.init();

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
	if(!$scope.saving){
		$scope.saving = true;
		if($scope.current.type == 'action'){
			$scope.action.recipe = $scope.current.recipe;
		}else{
			$scope.context.recipe = $scope.current.recipe;
		}
	    $http.post('/recipe', {"name": $scope.current.name, "context": $scope.consolidateRecipe($scope.context.recipe), "action": $scope.consolidateRecipe($scope.action.recipe)}).then(function(){
			console.log("success")
			$scope.init();
			$scope.saving = false;
		}, function(){console.log("error"); $scope.saving = false;});
	}
	
  }
  
  $scope.consolidateRecipe = function(recipe){
	  console.log(recipe)
	  var answer = [];
	  for(var i=0; i<recipe.length; i++){
		  var recipeItem = recipe[i];
		  if(recipeItem.type != "placeholder"){
			answer.push({"id": recipeItem.id, "category": recipeItem.option.categories[recipeItem.option.now.category], "value": recipeItem.option.now.value});
		  }
		  
	  }
	  return answer;
  }

});
