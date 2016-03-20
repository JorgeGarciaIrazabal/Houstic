import {Page, NavController, NavParams} from 'ionic-angular';
import {ButtonsGuide} from '../buttons-guide/buttons-guide';

@Page({
  templateUrl: 'build/pages/getting-started/getting-started.html'
})
export class GettingStartedPage {

  static get parameters() {
    return [[NavController], [NavParams]];
  }

  constructor(nav, navParams) {
    this.nav = nav;
    this.hubsApi = new HubsAPI('ws://127.0.0.1:9517/');
    this.conectarHub();
  }

  conectarHub() {
    this.hubsApi.connect().done(function () {
        console.log('Connected');
    }, function (error){
        console.error(error);
    });
  }

  desconectarHub() {
    console.log('Disconnected :(');
  }

  goButtonsGuide() {
    this.nav.push(ButtonsGuide);
  }

  sendToAll(value) {
    this.hubsApi.HouseHub.server.setActuatorValue(0, value).done(function (response){
      console.log(JSON.stringify(response));
    },function (message){
      console.log("Error " + message);
    }).finally(function () {
      console.log("I am in finnally");
    });
  }
}
