import {Page, NavController, NavParams} from 'ionic-angular';
import {HubsAPIService} from '../../services/HubsAPI';

@Page({
  templateUrl: 'build/pages/register/register.html',
  providers: [HubsAPIService]
})
export class Register {

  static get parameters() {
      return [[NavController], [NavParams], [HubsAPIService]];
  }

  constructor(nav, navParams, _apiService) {
      this.api = _apiService.geApi();
      // the api is trying to reconnect every 1 second
      this.nav = nav;
  }

  register() {
      this.api.UserHub.server.register({
        email:"prueba@prueba.com",
        password:"password"
      }).then(function() {
        console.log('succes');
      },function(err) {
        console.log('fail', err);
      })
  }
}
