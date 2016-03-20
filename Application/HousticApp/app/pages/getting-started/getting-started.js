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
  }

  conectarHub() {
    this.hubsApi.connect();
    console.log('Connected');
  }

  desconectarHub() {
    console.log('Disconnected :(');
  }

  goButtonsGuide() {
    this.nav.push(ButtonsGuide);
  }

  sendToAll() {
    this.hubsApi.HouseHub.server.getAllComponents(1).done(function (response){
      console.log(JSON.stringify(response));
    },function (message){
      console.log("Error " + message);
    }).finally(function () {
      console.log("I am in finnally");
    });
  }
}
