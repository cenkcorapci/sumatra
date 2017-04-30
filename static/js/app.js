var sumatraApp = new Vue({
  el: '#divNavBar',
  data: {
    loading: false,
    error: false,
    noContent: false,
    userName: "User Name",
    reddits: []
  },
  methods: {},
  mounted: function () {
    console.log("app loaded.")
  }
});
