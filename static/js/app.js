window.onload = function () {
  var sumatraApp = new Vue({
    el: '#DivMain',
    data: {
      noContent: true,
      topic: "",
      url: "",
      loading: false,
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
        var errorProtocol = function (error) {
          console.error(error);
          Materialize.toast('An Error Occured!', 4000);
          this.loading = false;
        };
        try {
          var endpoint = '/v1/topics?offset=0&limit=20';
          this.loading = true;
          this.$http.get(endpoint)
            .then(function (response) {
              if (response.status == 200) {
                this.loading = false;
                this.topics = JSON.parse(response.bodyText);
                if (this.topics.length == 0) {
                  console.log(this.topics);
                  this.noContent = true;
                } else {
                  this.noContent = false;
                }
              } else {
                errorProtocol(response.statusText);
              }
            }, function (error) {
              errorProtocol(error)
            });
        } catch (exp) {
          errorProtocol(exp);
        }
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
          this.topicLoading = false;
        };
        if (this.topic == "") {
          Materialize.toast('Please enter a topic name...', 4000);
          $('#ModalAddTopic').modal('close');
          return;
        }
        try {
          var endpoint = '/v1/topics';
          this.topicLoading = true;
          var payload = {
            'topic': this.topic,
            'url': this.url,
            'user': this.userName
          };
          this.$http.put(endpoint, payload)
            .then(function (response) {
              if (response.status == 200) {
                this.topicLoading = false;
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
      },
      upVote: function (topic) {
        var errorProtocol = function (error) {
          console.error(error);
          Materialize.toast('An Error Occured!', 4000);
        };
        try {
          var endpoint = '/v1/up-vote';
          var payload = {
            'topic': topic.topic,
            'by': topic.userName
          };
          this.$http.post(endpoint, payload)
            .then(function (response) {
              if (response.status == 200) {
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
      },
      downVote: function (topic) {
        var errorProtocol = function (error) {
          console.error(error);
          Materialize.toast('An Error Occured!', 4000);
        };
        try {
          var endpoint = '/v1/down-vote';
          var payload = {
            'topic': topic.topic,
            'by': topic.userName
          };
          this.$http.post(endpoint, payload)
            .then(function (response) {
              if (response.status == 200) {
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
      this.fetchAll();
    }
  });
};
