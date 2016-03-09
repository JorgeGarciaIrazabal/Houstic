import {Page, NavController, NavParams} from 'ionic-angular';
import {ButtonsGuide} from '../buttons-guide/buttons-guide';
var api = new HubsAPI("ws://127.0.0.1:9517")
api.connect(2);
@Page({
  templateUrl: 'build/pages/getting-started/getting-started.html'
})
export class GettingStartedPage {

  static get parameters() {
    return [[NavController], [NavParams]];
  }

  constructor(nav, navParams) {
    this.nav = nav;
  }

  conectarHub() {
    api.HouseHub.server.getAllComponents(10).done(function () {
        console.log(arguments)
    }, function () {
        console.error(arguments);
    })
    console.log('HOLA');
  }

  desconectarHub() {
    console.log('ADIOS :(');
  }

  goButtonsGuide(){
    this.nav.push(ButtonsGuide);
  }
}
