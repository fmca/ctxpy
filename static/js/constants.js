ifctt.constant("contextIngredients", [{
    name: "Liga��o",
	id: "Ligacao",
    option: {
      name: "N�mero",
      categories: ["=", "!="],
      value: true,
      now: {
        category: 0,
        value: "144"
      }
    },
    color: '#2ecc71',
    icon: 'glyphicon-earphone'
  }, {
    name: "Agenda",
	id: "Ocupado",
    option: {
      name: "Estiver",
      categories: ["ocupado", "livre"],
      value: false,
      now: {
        category: 0
      }
    },
    color: '#3498db',
    icon: 'glyphicon-calendar'
  }, {
    name: "Hor�rio",
	id: "Horario",
    option: {
      name: "Agora",
      categories: ["=", ">", "<"],
      value: true,
      now: {
        category: 0,
        value: "08:00"
      }
    },
    color: '#f39c12',
    icon: 'glyphicon-time'
  }, {
    name: "Localiza��o",
	id: "Localizacao",
    option: {
      name: "Estiver",
      categories: ["em casa", "fora de casa"],
      value: false,
      now: {
        category: 0
      }
    },
    color: '#e74c3c',
    icon: 'glyphicon-map-marker'
  }]);
  
  //
  //Action Ingredients
  //
  
  ifctt.constant("actionIngredients", [{
    name: "Ligar para",
	id: "Call",
    option: {
      name: "N�mero",
      categories: ["="],
      value: true,
      now: {
        category: 0,
        value: "144"
      }
    },
    color: '#2ecc71',
    icon: 'glyphicon-earphone'
  }, {
    name: "Agendar",
	id: "Calendar",
    option: {
      name: "Marcar",
      categories: ["ocupado", "livre"],
      value: false,
      now: {
        category: 0
      }
    },
    color: '#3498db',
    icon: 'glyphicon-calendar'
  }, {
    name: "Enviar Mensagem Facebook",
	id: "Facebook",
    option: {
      name: "Enviar para",
      categories: ["numero", "contato"],
      value: true,
      now: {
        category: 1,
        value: "Jos�"
      }
    },
    color: '#f39c12',
    icon: 'glyphicon-envelope'
  }]);
