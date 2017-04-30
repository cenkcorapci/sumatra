window.onload = function () {
  var sumatraApp = new Vue({
    el: '#DivMain',
    data: {
      loading: false,
      noContent: false,
      topic: "",
      url: "",
      topicLoading: false,
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
      },
      fetchAll: function () {
        //TODO
      },
      triggerAddTopic: function () {
        if (this.loggedIn) {
          $('#ModalAddTopic').modal('open');
        } else {
          $('#ModalLogIn').modal('open');
        }
      },
      addTopic: function () {
        var errorProtocol = function (error) {
          console.error(error);
          Materialize.toast('An Error Occured!', 4000);
          $('#ModalAddTopic').modal('close');
          this.loading = false;
        };
        try {
          var endpoint = '/v1/topics';
          this.loading = true;
          var payload = {
            'topic': this.topic,
            'url': this.url,
            'user': this.userName
          };
          this.$http.put(endpoint, payload)
            .then(function (response) {
              if (response.status == 200) {
                this.loading = false;
                $('#ModalAddTopic').modal('close');
                Materialize.toast('Topic created!', 4000);
                this.fetchAll();
              } else {
                errorProtocol(response.statusText);
              }
            }, function (error) {
              errorProtocol(error)
            });
        } catch (exp) {
          errorProtocol(exp);
        }
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
