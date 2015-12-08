ifctt.controller('ContextCtrl', function ($scope, $rootScope){


  $scope.lists = {};
  $scope.lists.context = [
    {
      name: "Contexto 1"
    },
    {
      name: "Contexto 2"
    },
    {
      name: "Contexto 3"
    },
    {
      name: "Contexto 4"
    }
  ]

  $scope.lists.recipe = [{type: "placeholder"}];

  $scope.sortableOptions = {
        allowDuplicates: false,
        containment: '#sortable-container',
        containerPositioning: 'relative',
        orderChanged: function(obj){
          $scope.reorganize();
        }
    };
    $scope.sortableCloneOptions = {
      containment: '#sortable-container',
      containerPositioning: 'relative',
        clone: true,
        itemMoved: function(obj){
          $scope.reorganize();
        }
    };

    $scope.reorganize = function(){
      var copy = $scope.lists.recipe;
      var newList = [];
      for(var i in copy){
        var it = copy[i];
        if(it.type != 'placeholder'){
            newList.push(it);
            newList.push({type: "placeholder"})
        }
      }
      $scope.lists.recipe = newList;
    }
})


.controller('ActionCtrl', function ($scope, $rootScope){


  $scope.lists = {};
  $scope.lists.actions = [
    {
      name: "Ação 1"
    },
    {
      name: "Ação 2"
    },
    {
      name: "Ação 3"
    }
  ]

  $scope.lists.recipe = [{type: "placeholder"}];

  $scope.sortableOptions = {
        allowDuplicates: false,
        containment: '#sortable-container',
        containerPositioning: 'relative',
        orderChanged: function(obj){
          $scope.reorganize();
        }
    };
    $scope.sortableCloneOptions = {
      containment: '#sortable-container',
      containerPositioning: 'relative',
        clone: true,
        itemMoved: function(obj){
          $scope.reorganize();
        }
    };

    $scope.reorganize = function(){
      var copy = $scope.lists.recipe;
      var newList = [];
      for(var i in copy){
        var it = copy[i];
        if(it.type != 'placeholder'){
            newList.push(it);
            newList.push({type: "placeholder"})
        }
      }
      $scope.lists.recipe = newList;
    }
});
