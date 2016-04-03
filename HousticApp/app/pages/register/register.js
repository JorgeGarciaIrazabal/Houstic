import {Page, NavController, NavParams} from 'ionic-angular';
import {HubsAPIService} from '../../services/HubsAPI';

@Page({
  templateUrl: 'build/pages/login/login.html',
  providers: [HubsAPIService]
})
export class Login {

  static get parameters() {
      return [[NavController], [NavParams], [HubsAPIService]];
  }

  constructor(nav, navParams, _apiService) {
      this.api = _apiService.geApi();
      // the api is trying to reconnect every 1 second
      this.nav = nav;
  }

  login() {
      this.api.UserHub.server.login({email:"email"}).done(function() {
        console.log('succes');
      },function(err) {
        console.log('fail', err);
      })
  }
}
