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
		if($rootScope.getMenu() == 'widgets'){
				$http.get('/widgets').then(function(response){
					$scope.widgets = response.data;
					$timeout($scope.getWidgets, 1500);
				}, function(){$timeout($scope.getWidgets, 1500);});	
		}else{
			$timeout($scope.getWidgets, 1500);
		}
	
		
		
    };
	
	$scope.getWidgets();
});
ifctt.controller('ConfigsCtrl', function($scope, $rootScope, $http, $timeout){
	$scope.configs = []
	$scope.lastConfigs = []

	$scope.compare = function(newC, old){
	  equals = true;
	  if(old == undefined || old.length == 0){
        return false
	  }
	  for(var i=0; i<old.length; i++){
	    config = old[i];
	    console.log(config.value, newC[i].value, config.value != newC[i].value)
	    if(config.value != newC[i].value){
	      equals = false;
	    }
	  }
	  console.log(equals)
	  return equals;
	}
	$scope.getConfigs = function(){
		if($rootScope.getMenu() == 'configs'){
				$http.get('/configs').then(function(response){
				    if(!$scope.compare(response.data, $scope.lastConfigs)){
				      $scope.configs = response.data;
					  $scope.lastConfigs = response.data;
				    }
					$timeout($scope.getConfigs, 1500);
				}, function(){$timeout($scope.getConfigs, 1500);});
		}else{
			$timeout($scope.getConfigs, 1500);
		}
    };
    
    $scope.saveConfigs = function(){
		if($rootScope.getMenu() == 'configs' && !$scope.compare($scope.configs, $scope.lastConfigs)){
				$http.post('/configs', $scope.configs).then(function(response){
				    $scope.lastConfigs = $scope.configs
					$timeout($scope.saveConfigs, 10000);
				}, function(){$timeout($scope.saveConfigs, 10000);});
		}else{
			$timeout($scope.saveConfigs, 10000);
		}
	};

	$scope.getConfigs();
	$scope.saveConfigs();
});
ifctt.controller('RecipesCtrl', function($scope, $rootScope, $http, $timeout){
	$scope.recipes = []
	$scope.getRecipes = function(){
		if($rootScope.getMenu() == 'recipes'){
			$http.get('/recipe').then(function(response){
				$scope.recipes = response.data;
				$timeout($scope.getRecipes, 1500);
			}, function(){$timeout($scope.getWidgets, 1500);});	
		}else{
			$timeout($scope.getRecipes, 1500);
		}
		
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
    if($scope.current.type == 'action'){
		$scope.action.recipe = $scope.current.recipe;
	}else{
		$scope.context.recipe = $scope.current.recipe;
	}
  }


  $scope.deleteItem = function(index) {
    $scope.current.recipe.splice(index, 1);
    $scope.reorganize();
  }

  $scope.toVariableStr = function(str){
    /*var items = $scope.action.recipe.concat($scope.context.recipe);
     console.log(items)
    for(var i=0; i<items.length; i++){
        var item = items[i];
        console.log(item.option)
        if(item.option){
            for(var j=0; item.option.variables.length; j++){
                var variable = item.option.variables[j];
                console.log(variable)
                if(variable){
                    console.log(variable)
                    str = str.replace(variable.name, "<span class='label label-default'>" + variable.name + "</span>"); 
                }
            }
        }
    }*/
    return str;
  }
  
  
  $scope.save = function(){
	if(!$scope.saving){
		$scope.saving = true;
		var variables = []
		var items = $scope.action.recipe;
		for(var i=0; i<items.length; i++){
			var item = items[i]
			if(item.type!="placeholder"){
				for(var j=0; j<item.option.variables.length; j++){
					var v = item.option.variables[j]
					variables.push({"name": v['name'], "value": v['default']})
				}
			}
		}
	    $http.post('/recipe', {"name": $scope.current.name, "context": $scope.consolidateRecipe($scope.context.recipe), "action": $scope.consolidateRecipe($scope.action.recipe), "variables": variables}).then(function(){
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
