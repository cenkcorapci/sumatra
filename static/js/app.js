window.onload = function () {
  var sumatraApp = new Vue({
    el: '#DivMain',
    data: {
      loading: false,
      noContent: false,
      userName: "",
      loggedIn: false,
      topics: []
    },
    methods: {
      logIn: function () {
        sessionStorage.setItem('user', this.userName);
        this.loggedIn = true;
        console.log('logged in as ' + this.userName);
      },
      logOut: function () {
        sessionStorage.removeItem('user');
        this.userName = null;
        this.loggedIn = false;
      }
    },
    mounted: function () {
      console.log("App loaded.");
      $('.modal').modal();

      var user = sessionStorage.getItem('user');
      if (user) {
        this.loggedIn = true;
        this.userName = user;
      }
    }
  });
};
