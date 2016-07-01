"use strict";

var app = angular.module('MapCreatorApp', ['ngRoute', 'ui.bootstrap', 'angularSpinner','ngCookies'])
.run(['$rootScope', '$location', 'loginSrv',
  function($rootScope, $location, loginSrv){
    $rootScope.$on('$routeChangeStart', function (event, next, current) {
      if (!next.access) return;
      if (next.access.restricted) {
        if (loginSrv.getToken() !== undefined) return;
        $location.path('login');
      }
    });
}]);;

app.constant("backendCfg", {
  "api_url": ""
})

app.config(['$routeProvider','$locationProvider',
function($routeProvider, $locationProvider) {
  $routeProvider.
    when('/', {
      templateUrl: 'static/templates/view_map.html',
      controller: 'MainMapCtl',
      reloadOnSearch:false,
      access: {restricted: true}
    }).
    when('/newpass', {
      templateUrl: 'static/templates/newpassword.html',
      controller: 'NewPasswordCtl'
    }).
    when('/login', {
      templateUrl: 'static/templates/login.html',
      controller: 'LoginCtl'
    }).
    otherwise({ redirectTo: '/'});
}
]);

app.service('loginSrv', ['$cookies','$location', function ($cookies, $location) {
    var currentUser={};
    var token;
    return {
        logout: function () {
          $cookies.remove('token');
          $cookies.remove('currentUser');
          $location.path('/login');
        },
        getCurrentUser: function () {
          return $cookies.getObject('currentUser');
        },
        setCurrentUser: function(value, expireDate) {
          $cookies.putObject('currentUser', value, {'expires': expireDate+'Z'});
        },
        getToken: function() {
          return $cookies.get('token');
        },
        setToken: function(value) {
          $cookies.put('token', value);
        }
    };
}]);

app.controller('LoginCtl', [ '$scope', '$http', 'loginSrv','backendCfg','$location','$uibModal',
  function ($scope, $http, loginSrv,backendCfg,$location,$uibModal) {
    var self = this;

    $scope.sumbit = function () {
      var form = $scope.loginForm
      $http.post(backendCfg.api_url + 'auth/login',
          {"login":$scope.login, "password": $scope.password}
        ).success(function(response) {
          loginSrv.setCurrentUser(response.user, response.expires);
          $location.path('/');
        })
        .error(function(data, status) {
          if (status === 490) {
            if(data.type=='inactif') $('#modalCompteInactif').modal({show:true});
            else form[data.type].$invalid = true;
          }
          else {
            form.$invalid = true;
          }
        })
    };

}]);

app.controller('NewPasswordCtl', [ '$scope', '$http', 'backendCfg','$location',
  function ($scope, $http, backendCfg,$location) {
    var self = this;
    $scope.newpassword = function () {
      var form = $scope.newPassForm
      $http.post(backendCfg.api_url + 'auth/generate_password',
          {"email":$scope.email}
        ).success(function(response) {
          $location.path('/login');
        })
        .error(function(data, status) {
          if (status === 490) {
            form[data.type].$invalid = true;
          }
          else {
            form.$invalid = true;
          }
        })
    };

}]);

app.controller('MainMapCtl',
['$scope', '$http','LeafletServices', '$rootScope', '$compile','$sce','usSpinnerService', 'loginSrv',

function ($scope, $http, LeafletServices, $rootScope, $compile,$sce, usSpinnerService, loginSrv) {
  $scope.baselayers = {};
  $scope.mainLayer = null;
  $scope.mainLayerData = null;


  $scope.currentUser = loginSrv.getCurrentUser();
  $('#info-popup').hide();

  $scope.map = L.map('mapc', { zoomControl:false ,attributionControl:false});

  //Chargement des données statiques
  $scope.contact_massifs= {};
  $http.get("pq/contact/massifs").then(
    function(results) {
      $scope.contact_massifs = results.data;
  });
  //Chargement des données statiques
  $scope.contact_dt= {};
  $http.get("pq/contact/dt").then(
    function(results) {
      $scope.contact_dt = results.data;
  });
  $scope.annee_etatdonnees = (new Date() > new Date((new Date().getFullYear())+'-05-15')) ? new Date().getFullYear() : new Date().getFullYear()-1;

  //Démarrage du spinner
  usSpinnerService.spin('spinner-1');

  $http.get("static/data/maps.json").then(
    function(results) {
      //----Fonds de carte
      angular.forEach(results.data.layers.baselayers, function(value, key) {
        var l = LeafletServices.loadData(value);
        $scope.baselayers[key] = l;
        if (value.active) {
          $scope.baselayers[key].map.addTo($scope.map);
        }
      });
      $scope.map.setView(new L.LatLng(results.data.center.lat, results.data.center.lng),results.data.center.zoom);

      $scope.mapOptions = results.data;

      //----Couche principale
      //options
      // Ajout
      var info = L.control({position:'topleft'});

      info.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML ='<strong>'+$scope.currentUser.commune+' et environs</strong>';
        return div;
      };

      info.addTo($scope.map);

      $scope.date_maj_donnees = $scope.mapOptions.layers.overlay.date_maj_donnees;
      var att = L.control.attribution().addAttribution("&copy;PnC mise à jour "+$scope.date_maj_donnees);
      att.addTo($scope.map);

      if (!$scope.mapOptions.layers.overlay.tooltip) $scope.mapOptions.layers.overlay.tooltip = {};
      if ($scope.mapOptions.layers.overlay.tooltip.display){
        info.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info');
            this.update();
            return this._div;
        };
        info.update = function (props) {
            this._div.innerHTML = (props ?
              eval($scope.mapOptions.layers.overlay.tooltip.content)
              : '');
        };
        info.addTo($scope.map);
      }

      $scope.mainLayerOptions = eval("("+(results.data.layers.overlay.options || {}) +")");
      $scope.mainLayerOptions.customOnEachFeature = $scope.mainLayerOptions.onEachFeature || function () {};

      $scope.mainLayerOptions.onEachFeature = function(feature, layer) {
        $scope.mainLayerOptions.customOnEachFeature(feature, layer);

        if ($scope.mapOptions.layers.overlay.tooltip.display){
          layer.on({
            mouseover : function(e) {
                info.update(layer.feature.properties);
            },
            mouseout : function(e) {
                info.update();
            }
          });
        }

        layer.on({
          click : function(e){
            $rootScope.$apply($rootScope.$broadcast("feature:click", layer))
          },
          popupclose: function() {
            $('#info-popup').hide();
            $scope.l_prev_sel.item.setStyle({color: $scope.l_prev_sel.color, fill: $scope.l_prev_sel.fill, fillColor: $scope.l_prev_sel.fillColor});
          }
        });
      };
      //Chargement des données et affichage sur la carte
      $http.get(results.data.layers.overlay.url).then(
        function(results) {
          $scope.mainLayerData = results.data;
          $scope.mainLayer = new L.geoJson(results.data,$scope.mainLayerOptions);
          $scope.map.addLayer($scope.mainLayer);
          //Arret du spinner
          usSpinnerService.stop('spinner-1');
          $('#modalCharteDonnees').modal({show:true});
        });

      //----Selecteur de localisation
      if (results.data.location) {
        $http.get(results.data.location.url).then(
          function(results) {
            $scope.locationData = results.data;
            $scope.selectedLocation = results.data.filter(function(d){if (d.code_insee==$scope.currentUser.code_insee) return d; })[0];
          }
        );
      }

      //Affichage d'un masque sur l'emprise de la commune

      $http.get('pq/maskcommunes/'+$scope.currentUser.code_insee).then(
        function(results) {
          // transform geojson coordinates into an array of L.LatLng
          var coordinates = results.data.geometry.coordinates[0][0];
          var latLngs = [];
          for (var i=0; i<coordinates.length; i++) {
              latLngs.push(new L.LatLng(coordinates[i][1], coordinates[i][0]));
          }

          L.mask(latLngs).addTo($scope.map);
        }
      );

    }
  );

  //Action selection d'un élément sur la carte
  $scope.$on('feature:click', function(ev, item){
    if($scope.l_prev_sel != null && $scope.l_prev_sel.item.feature.geometry.type != "Point"){
      $scope.l_prev_sel.item.setStyle({color: $scope.l_prev_sel.color, fill: $scope.l_prev_sel.fill , fillColor: $scope.l_prev_sel.fillColor});
    }
    var prev_color = null;
    var prev_fill = null;
    var prev_fillColor = null;
    if (item._layers) {
      var x;
      for(x in item._layers){
        prev_color = item._layers[x].options.color;
        prev_fill = item._layers[x].options.fill;
        prev_fillColor = item._layers[x].options.fillColor;
        break;
      }
    }
    else {
      prev_color = item.options.color;
      prev_fill = item.options.fill;
      prev_fillColor = item.options.fillColor;
    }
    $scope.l_prev_sel = {item: item, color: prev_color, fill:prev_fill, fillColor:prev_fillColor};
    if(item.feature.geometry.type != "Point"){
      item.setStyle({color: 'yellow', fillColor:'yellow'});
    }
    $scope.infoObj = item.feature.properties;
    $scope.isCollapsed = false;
    $('#info-popup').show();
  });

  //Action zoom sur une localisation
  $scope.$watch('selectedLocation', function (newvalue, oldvalue) {
    if (newvalue) {
      $scope.map.fitBounds([
        [newvalue.st_ymin, newvalue.st_xmin],
        [newvalue.st_ymax, newvalue.st_xmax]
      ], {zoom:17});
    }
  });

  //Action filtre d'un élément sur la carte
  $scope.dofilterOnMap= function () {
    $scope.map.removeLayer($scope.mainLayer);
    var options = angular.extend(
      $scope.mainLayerOptions,
      {
        filter: function(feature, layer) {
          var fil=0;
          angular.forEach($scope.mapOptions.layers.overlay.filters, function(arrayFilter, key) {
            if (feature.properties[key]) fil += arrayFilter.values[feature.properties[key]].visible;
          });
          return fil > 1 ? true : false ;
        }
      }
    );
    $scope.mainLayer = new L.geoJson($scope.mainLayerData,options);
    $scope.mainLayer.addTo($scope.map);
  }

  $scope.checkUncheckAll= function (filterType, val) {
    var toggleStatus = val;
    angular.forEach($scope.mapOptions.layers.overlay.filters[filterType].values, function(arrayFilter, key) {
      arrayFilter.visible = toggleStatus;
    });
    $scope.dofilterOnMap();
  }
}]
);

app.directive('dirFilterElement', function() {
  return {
    restrict: 'E',
    scope: {
      key: '=key',
      filterInfo: '=filter',
      onCheck:'&'
    },
    templateUrl: 'static/templates/directive-filterpanel.html',
    controller: function($scope){
      $scope.state = angular.isDefined($scope.state) ? Boolean($scope.state) : true;
    }
  };
});

app.factory('LeafletServices', ['$http', function($http) {
  return {
    layer : {},

    loadData : function(layerdata) {
      this.layer = {};
      this.layer.name = layerdata.name;
      this.layer.active = layerdata.active;

      if (layerdata.type == 'xyz' || layerdata.type == 'ign') {
        var url = layerdata.url;
        if ( layerdata.type == 'ign') {
          url = 'https://gpp3-wxs.ign.fr/' + layerdata.key + '/geoportail/wmts?LAYER='+layerdata.layer+'&EXCEPTIONS=text/xml&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}';
        }
        this.layer.map = new L.TileLayer(url,layerdata.options);
      }
      else if (layerdata.type == 'wms') {
        this.layer.map = L.tileLayer.wms(layerdata.url,layerdata.options);
      }
      return this.layer;
    }
  };
}]);

app.config(['$httpProvider',
  function ($httpProvider) {
    $httpProvider.interceptors.push(['$q','loginSrv', function ($q,loginSrv) {
      return {
        'request': function (config) {
          //do stuff
          return config || $q.when(config);
        },
        'requestError': function (rejection) {
          console.log('requestError');
          return $q.reject(rejection);
        },
        'response': function (response) {
          return response || $q.when(response);
        },
        'responseError': function (rejection) {
          console.log('responseError');
          console.log(rejection.status);
          if (rejection.status == "403") {
            loginSrv.logout();
          }
          if (rejection.status == "401") {
            console.log("no permission!");
          }
          return $q.reject(rejection);
        }
      };
    }]);
  }
]);
