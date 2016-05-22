import {Page, NavController, NavParams} from 'ionic-angular';
import {ComponentListPage} from '../components-list/components-list';
import {HubsAPIService} from '../../services/HubsAPI';

@Page({
    templateUrl: 'build/pages/houses-list/houses-list.html'
})
export class HouseListPage {
    static get parameters() {
        return [[NavController], [NavParams], [HubsAPIService]];
    }

    constructor(nav, navParams, _apiService) {
        var self = this;
        this.nav = nav;
        this.api = _apiService.getApi();
        // If we navigated to this page, we will have an item available as a nav param
        this.houses = [];

        this.api.HouseHub.server.listHouses()
            .then(function (houses) {
                self.houses = houses;
                self.houses.map(function (house) {
                    house.connectedIcon = house.connected ? "checkmark-circle-outline" : "close-circle";
                    house.name = house.name || "undefined";
                });
            });

        this.icons = ['home', 'home', 'home'];
    }

    vewComponent( house) {
        this.nav.push(ComponentListPage, {
            house: house
        })
    }
}
