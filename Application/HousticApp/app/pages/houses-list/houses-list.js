import {Page, NavController, NavParams} from 'ionic-angular';
import {ComponentListPage} from '../components-list/components-list';

@Page({
  templateUrl: 'build/pages/houses-list/houses-list.html'
})
export class HouseListPage {
  static get parameters() {
    return [[NavController], [NavParams]];
  }

  constructor(nav, navParams) {
    this.nav = nav;

    // If we navigated to this page, we will have an item available as a nav param
    this.selectedItem = navParams.get('item');

    this.icons = ['home', 'home', 'home'];

    this.items = [];
    for(let i = 1; i < 4; i++) {
      this.items.push({
        title: 'Casa ' + i,
        note: 'Ver componentes',
        icon: this.icons[Math.floor(Math.random() * this.icons.length)]
      });
    }
  }

  itemTapped(event, item) {
    this.nav.push(ComponentListPage, {
      item: item
    })
  }
}
