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
  }

  conectarHub() {
    console.log('HOLA');
  }

  desconectarHub() {
    console.log('ADIOS :(');
  }

  goButtonsGuide(){
    this.nav.push(ButtonsGuide);
  }
}
