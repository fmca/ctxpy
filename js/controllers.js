ifctt.controller('ContextCtrl', function ($scope, $rootScope){


  $scope.lists = {};
  $scope.lists.context = [
    {
      name: "Ligação",
      option: {name: "Número", categories: ["=", "!="], value: true, now: {category: 0, value: "144"}},
      color: '#2ecc71',
      icon: 'glyphicon-earphone'
    },
    {
      name: "Agenda",
      option: {name: "Estiver", categories: ["ocupado", "livre"], value: false, now: {category: 0}},
      color: '#3498db',
      icon: 'glyphicon-calendar'
    },
    {
      name: "Horário",
      option: {name: "Agora", categories: ["=", ">", "<"], value: true, now: {category: 0, value: "08:00"}},
      color: '#f39c12',
      icon: 'glyphicon-time'
    },
    {
      name: "Localização",
      option: {name: "Estiver", categories: ["em casa", "fora de casa"], value: false, now: {category: 0}},
      color: '#e74c3c',
      icon: 'glyphicon-map-marker'
    }
  ];

  $scope.removeItem = function(index){
    $scope.lists.context.splice(index, 1);
    $scope.reorganize();
  }

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
