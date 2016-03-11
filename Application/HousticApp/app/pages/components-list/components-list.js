import {Page, NavController, NavParams} from 'ionic-angular';


@Page({
  templateUrl: 'build/pages/components-list/components-list.html'
})
export class ComponentListPage {
  static get parameters() {
    return [[NavController], [NavParams]];
  }

  constructor(nav, navParams) {
    this.nav = nav;

    // If we navigated to this page, we will have an item available as a nav param
    this.selectedItem = navParams.get('item');

    this.icons = ['beaker', 'beer', 'bonfire'];

    this.items = [];
    for(let i = 0; i < 3; i++) {
      this.items.push({
        title: 'Componente ' + (i +1),
        note: '',
        icon: this.icons[i]
      });
    }
  }
}
