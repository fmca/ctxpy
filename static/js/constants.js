ifctt.constant("contextIngredients", [{
    name: "Ligação",
	id: "Ligacao",
    option: {
      name: "Número",
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
    name: "Horário",
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
    name: "Localização",
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
      name: "Número",
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
        value: "José"
      }
    },
    color: '#f39c12',
    icon: 'glyphicon-envelope'
  }]);
