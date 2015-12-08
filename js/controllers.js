ifctt.controller('ActionCtrl', function ($scope, $rootScope){


  $scope.lists = {};
  $scope.lists.context = [
    {
      name: "Test"
    },
    {
      name: "Test 2"
    },
    {
      name: "Test 3"
    }
  ]

  $scope.lists.recipe = [{type: "placeholder"}];

  $scope.sortableOptions = {
        allowDuplicates: false,
        containment: '#sortable-container',
        containerPositioning: 'relative',
        dragEnd: function(obj){
          $scope.reorganize();
        }
    };
    $scope.sortableCloneOptions = {
      containment: '#sortable-container',
      containerPositioning: 'relative',
        clone: true,
        dragEnd: function(obj){
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
